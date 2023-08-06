import time
import logging
from collections import namedtuple

from numba import njit
import numpy as np
from copy import deepcopy
from typing import Union, Optional

from .solver_methods import BaseMethod, RK45, Euler, BDF, NoDiff
from .base import Solution
from .interface import Interface
from .handlers import DefaultEventHandler, EventHandler
from .models import Model
from .solve_states import SolveEvent, SolveStatus


solver_methods = {'RK45': RK45, 'Euler': Euler, 'BDF': BDF, 'NoDiff': NoDiff}

SolverInfo = namedtuple('Info', ['status', 'event_id', 'step_info', 'initial_step', 'dt', 't', 'y', 'order_', 'roller',
                            'solve_state', 'ix_eval', 'g', 'step_converged', 'event_trigger', 'direction'])

try:
    FEPS = np.finfo(1.0).eps
except AttributeError:
    FEPS = 2.220446049250313e-16

logger = logging.getLogger(__name__)


class NumerousSolver:
    """Initialization method of Numerous solver.

    :param model: an instance of the model
    :type model: :class:object
    :param use_jit: bool: Use numba jit. Default is False.
    :type use_jit: bool
    :param event_handler: event handler :class:`solver.interface.EventHandler`
    :param options: Additional options to pass to the solver. Allowed values are
    * :attr:`rtol`: The relative tolerance
    * :attr:`atol`: the absolute tolerance
    * :attr:`meth`: the solver method. Possible choices are 'RK45' :meth:`~solver.solver_methods.RK45`, \
        'BDF': :meth:`~solver.solver_methods.BDF` and 'Euler' :meth:`~solver.solver_methods.Euler`.

    """

    def __init__(self, model: Model,
                 use_jit: bool = False, event_handler=None,
                 **options):

        if not event_handler:
            event_handler = DefaultEventHandler()
        self.event_handler: EventHandler = event_handler

        self.use_jit = use_jit
        self.model = model
        self.options = {}
        interface, time_events, external_time_events, state_events, \
            external_state_events = model.generate_interface(use_jit)

        time_events_ = [time_event._compiled_model for time_event in time_events]
        state_events_ = [state_event._compiled_model for state_event in state_events]

        self.time_events = tuple(time_events_)
        self.state_events = tuple(state_events_)

        time_events_dict = {time_event.id: time_event._compiled_model for time_event in time_events}
        external_time_events_dict = {time_event.id: time_event for time_event in external_time_events}

        state_events_dict = {state_event.id: state_event._compiled_model for state_event in state_events}

        external_state_events_dict = {state_event.id: state_event for state_event in external_state_events}

        self.events = dict(time_events_dict, **state_events_dict)
        self.external_events = dict(external_time_events_dict, **external_state_events_dict)

        self.interface: Interface = interface._compiled_model

        if not hasattr(self.interface, '_numba_type_') and use_jit:
            raise TypeError("when requesting a jitted solver, the interface must also be jitted")

        self._set_options(options)

        y0 = self.interface.get_states()
        #self.g = np.array([1.0])
        self.g = self.interface.get_state_event_results(0, y0, self.state_events)

        self.info = None
        self.y0 = y0

        # Generate the solver
        if self.use_jit:
            self._non_compiled_solve = njit(self._generate_solver())
            self._solve = self._compile_solver()
        else:
            self._solve = self._generate_solver()
    def _set_options(self, options):
        y0 = self.interface.get_states()
        f0 = self.interface.get_deriv(0, y0)

        self.options.update(options)
        odesolver_options = {
            'longer': self.options.get('longer', 1.2), 'shorter': self.options.get('shorter', 0.8),
            'min_step': self.options.get('min_step', 10 * FEPS), 'strict_eval': True,
            'max_step': self.options.get('max_step', np.inf), 'first_step': self.options.get('first_step', None),
            'atol': self.options.get('atol', 1e-6), 'rtol': self.options.get('rtol', 1e-3),
            'submethod': self.options.get('submethod', None),
        }
        self.method_options = odesolver_options
        method = self.options.get('method', 'RK45')
        if f0 is None or len(f0) == 0:
            logger.debug("Using no derivatives solver. If this is not intended, make sure you specify the 'get_deriv' "
                         "method for the model")
            method = "NoDiff"

        try:
            self.method = solver_methods[method]
        except KeyError:
            raise ValueError(f"Unknown method {self.options.get('method', 'RK45')}, "
                             f"allowed methods: {list(solver_methods.keys())}")
        self._method = self.method(self.interface, self.use_jit, **self.method_options)
        assert issubclass(self.method, BaseMethod), f"{self.method} is not a BaseMethod"

    def _generate_solver(self):
        def _solve(interface, time_events, state_events, _solve_state, initial_step, dt_0, order,
                   order_, roller, strict_eval, min_step, max_step, step_integrate_, g,
                   step_converged, event_trigger, t0=0.0, t_end=1000.0, t_eval=np.linspace(0.0, 1000.0, 100), ix_eval=1,
                   event_tolerance=1e-6) -> SolverInfo:

            # Init t to t0
            imax = int(100)
            step_info = 0
            t = t0
            t_start = t0
            dt = dt_0
            interface.pre_step(t, interface.get_states())
            y = interface.get_states()
            failed_steps = 0
            failed_events = 0
            warned = False
            warned_event = False

            solve_status = SolveStatus.Running
            solve_event_id = SolveEvent.NoneEvent

            t_previous = t0
            y_previous = np.copy(y)

            # Define event derivatives, values and event guess times
            te_array = np.zeros(3)

            def is_internal_historian_update_needed(t_next_eval, t):
                if abs(t_next_eval - t) < 100 * FEPS:
                    return True
                return False

            def handle_converged(t, y, dt, ix_eval, t_next_eval):

                solve_event_id = SolveEvent.NoneEvent

                if is_internal_historian_update_needed(t_next_eval, t):
                    solve_event_id = interface.historian_update(t, y)
                    if strict_eval:
                        te_array[1] = t_next_eval = t_eval[ix_eval + 1] if ix_eval + 1 < len(t_eval) else t_eval[-1]
                    else:
                        t_next_eval = t_eval[ix_eval + 1] if ix_eval + 1 < len(t_eval) else t_eval[-1]
                    ix_eval += 1
                    te_array[0] = t + dt

                t_start = t
                t_new_test = min(te_array)

                return solve_event_id, ix_eval, t_start, t_next_eval, t_new_test

            def add_ring_buffer(t_, y_, rb, o):

                if o == order:
                    y_temp = rb[2][:, :]
                    t_temp = rb[1]
                    rb[1][0:order - 1] = t_temp[1:order]
                    rb[2][0:order - 1, :] = y_temp[1:order, :]

                o = min(o + 1, order)
                rb[1][o - 1] = t_
                rb[2][o - 1, :] = y_

                return o

            def get_order_y(rb, order):
                y = rb[2][0:order, :]
                return y

            # 0 index is used to keep next time step defined by solver
            te_array[0] = t
            # 1 index is used to keep next time to eval/save the solution

            te_array[1] = t_eval[ix_eval] + dt if strict_eval else np.inf
            t_next_eval = t_eval[ix_eval]

            event_ix = -1
            direction = 0
            t_event = t
            y_event = y
            t_event_previous = -1
            t_next_time_event, has_time_events = interface.get_next_time_event(t, time_events)

            if has_time_events:
                te_array[2] = t_next_time_event
            else:
                te_array[2] = max(te_array)

            while solve_status != SolveStatus.Finished:
                # updated events time estimates
                # # time acceleration
                if not step_converged:
                    if min_step > dt:
                        raise ValueError('dt shortened below min_dt')
                    te_array[0] = t_previous + dt
                elif step_converged and not event_trigger:
                    dt = min(max_step, dt)
                    te_array[0] = t + dt
                else:  # event
                    te_array[0] = t_event

                # Determine new test - it should be the smallest value requested by events, eval, step
                t_new_test = min(te_array)

                # Determine if rollback is needed
                # check if t_new_test is forward
                # no need to roll back if time-step is decreased, as it's not a failed step
                if (t_new_test < t) or (not step_converged):
                    # Need to roll back!
                    t_start = t_previous
                    y = y_previous

                    if t_new_test < t_start:
                        # t_new_test = t_rollback
                        # TODO: make more specific error raising here!
                        raise ValueError('Cannot go back longer than rollback point!')

                dt_ = min([t_next_eval - t_start, t_new_test - t_start])

                if order_ == 0:
                    order_ = add_ring_buffer(t, y, roller, order_)

                # solve from start to new test by calling the step function
                t, y, step_converged, step_info, _solve_state, factor = step_integrate_(interface,
                                                                                        t_start,
                                                                                        dt_, y,
                                                                                        get_order_y(roller, order_),
                                                                                        order_,
                                                                                        _solve_state)

                dt = min(dt * factor, t_end)

                event_trigger = False
                if not step_converged:
                    failed_steps += 1
                    if failed_steps > 100 and not warned:
                        print("slow convergence", dt)
                        warned = True

                if step_converged:
                    failed_steps = 0
                    warned = False
                    t_next_time_event, has_time_events = interface.get_next_time_event(t, time_events)
                    if has_time_events:
                        te_array[2] = t_next_time_event
                    else:
                        te_array[2] = max(te_array)


                    t_event, y_event, g, event_trigger, direction = interface.get_state_events(g, state_events, roller,
                                                                                               order, event_tolerance,
                                                                                               imax, t_previous,
                                                                                               y_previous, t, y)

                if not event_trigger and step_converged:
                    y_previous = y
                    t_previous = t

                    if has_time_events and abs(t - t_next_time_event) < event_tolerance:
                        interface.set_states(y)
                        
                        external, y_previous = interface.run_events(0, t, y, time_events)

                        interface.set_states(y_previous)
                        if external:
                            solve_event_id = SolveEvent.TimeEvent
                            break

                        solve_event_id = interface.post_time_event(t, y_previous)
                        if solve_event_id != SolveEvent.NoneEvent:
                            break

                if event_trigger:
                    # Improve detection of event

                    if abs(t_event - t_event_previous) > event_tolerance:
                        failed_events += 1
                        if failed_events > 100 and not warned_event:
                            print("event searching is slow. Try tightening absolute tolerance.",
                                  abs(t_event - t_event_previous), ">", event_tolerance)
                            warned_event = True
                        t_event_previous = t_event
                        step_converged = False  # roll back and refine search
                        dt = initial_step
                        g = interface.get_state_event_results(t, y_previous, state_events)
                        interface.unset_events(state_events)
                    else:
                        t_event_previous = t_event
                        failed_events = 0
                        warned_event = False
                        interface.set_states(y_event)
                        external, y_previous = interface.run_events(direction, t_event, y_event, state_events)
                        interface.set_states(y_previous)
                        step_converged = False

                        if external:
                            solve_event_id =  SolveEvent.StateEvent
                            t = t_event
                            y = y_event
                            break

                        interface.set_states(y_previous)

                        t_previous = t_event

                        # TODO: Update solve in solver_methods with new solve state after changing states due to events

                        solve_event_id = interface.post_state_event(t_event, y_previous, "dummy")
                        # Immediate rollback in case of exit
                        t = t_previous
                        y = y_previous

                        if solve_event_id != SolveEvent.NoneEvent:
                            break
                    

                if step_converged:
                    interface.set_states(y)
                    solve_event_id = interface.post_step(t, y)
                    if solve_event_id != SolveEvent.NoneEvent:
                        break

                    order_ = add_ring_buffer(t, y, roller, order_)

                    solve_event_id, ix_eval, t_start, t_next_eval, t_new_test = \
                        handle_converged(t, y, dt, ix_eval, t_next_eval)

                    if abs(t - t_end) < 100 * FEPS:
                        solve_status = SolveStatus.Finished
                        break

                    if solve_event_id != SolveEvent.NoneEvent:
                        break

            return SolverInfo(status=solve_status, event_id=solve_event_id, step_info=step_info,
                        dt=dt, t=t, y=np.ascontiguousarray(y), order_=order_, roller=roller, solve_state=_solve_state,
                        ix_eval=ix_eval, g=g, initial_step=initial_step, step_converged=step_converged,
                        event_trigger=event_trigger, direction=direction)

        return _solve

    def _compile_solver(self):

        logger.info("Compiling Numerous Solver")
        generation_start = time.time()

        argtypes = []

        max_step = self.method_options.get('max_step')
        min_step = self.method_options.get('min_step')

        strict_eval = self.method_options.get('strict_eval', True)

        order = self._method.order
        initial_step = min_step

        step_integrate_ = self._method.step_func
        roller = self._init_roller(order)
        order_ = 0

        args = (self.interface,
                self.time_events,
                self.state_events,
                self._method.get_solver_state(),
                initial_step,
                initial_step,
                order,
                order_,
                roller,
                strict_eval,
                min_step,
                max_step,
                step_integrate_,
                self.g,
                False,
                False,
                0.0,
                0.1,
                np.array([0.0, 0.1]),
                1,
                self.method_options.get('atol')
                )
        for a in args:
            argtypes.append(self._non_compiled_solve.typeof_pyval(a))
        # Return the solver function

        _solve = self._non_compiled_solve.compile(tuple(argtypes))

        generation_finish = time.time()
        logger.info(f"Solver compiled, compilation time: {generation_finish - generation_start}")

        return _solve

    def _init_roller(self, order):
        n = order + 2
        rb0 = np.zeros((n, len(self.y0)))
        roller = (n, np.zeros(n), rb0)
        return roller

    def _init_solve(self, time: np.array, info=None, delta_t=None):

        max_step = self.method_options.get('max_step')
        min_step = self.method_options.get('min_step')
        atol = self.method_options.get('atol')
        rtol = self.method_options.get('rtol')
        strict_eval = self.method_options.get('strict_eval')
        step_integrate_ = self._method.step_func
        order = self._method.order

        if not info:
            self.interface.init_solver(time[0], self.y0)
            self.interface.pre_step(time[0], self.y0)
            solve_event_id = self.interface.historian_update(time[0], self.y0)
            self.event_handler.handle_solve_event(interface=self.interface, event_id=solve_event_id, t=time[0])

            # Call the solver

            y0 = deepcopy(self.y0)

            # Set options

            initial_step = self._method.initial_step

            dt = initial_step if len(y0) > 0 else time[1]-time[0]

            # figure out solve_state init
            solve_state = self._method.get_solver_state()

            roller = self._init_roller(order)
            order_ = 0
            g = self.interface.get_state_event_results(time[0], y0, self.state_events)

            #g = self.interface.get_event_results(time[0], y0)
            step_converged = False
            event_trigger = False
        else:

            dt = delta_t  # internal solver step size
            order_ = self.info.order_
            roller = self.info.roller
            solve_state = self.info.solve_state
            g = self.info.g
            initial_step = self.info.initial_step
            step_converged = self.info.step_converged
            event_trigger = self.info.event_trigger

        return dt, strict_eval, step_integrate_, solve_state, roller, order_, order, initial_step, min_step, \
               max_step, atol, rtol, g, step_converged, event_trigger

    def reset(self):
        """Resets the solution and calls the model reset method.

        :return: None
        """
        self.event_handler.reset_solution()
        self.model.reset()
        for event in self.events.values():
            event.reset()
        for external_event in self.external_events.values():
            external_event.reset()

        self.info = None

    def solve(self, t_eval: np.array, y0: Optional[np.array] = None, **options):
        """Solves the model.

        :param: t_eval: Input array of all timestamps for which solution is to be evaluated
        :param y0: States to set as initial states (optional)
        :return: None

        """
        if y0 is not None:  # Sets the initial states and resets the solution
            self.event_handler.reset_solution()
            self.interface.set_states(y0)
            self.info = None

        if options:
            self._set_options(options)

        t_eval = t_eval.astype('float')
        logger.info('Solve started')

        self._solver(t_eval)
        logger.info("Solve ended")

    def solver_step(self, t: float, delta_t: float):
        """Performs a single step in the solver time.

        :param t: Current time
        :param delta_t: The timestep to perform
        :return: tuple: next timestep and actual internal solver step time (should match).
        """

        t_eval = np.linspace(t, t+delta_t, 2, dtype=np.float64)
        t_end = t_eval[-1]

        info = self._solver(t_eval, info=self.info, delta_t=delta_t)
        self.info = info

        return t_end, self.info.t

    def _solver(self, t_eval, info=None, delta_t=None):

        dt, strict_eval, step_integrate_, solve_state, roller, order_, order, initial_step, min_step, max_step, \
            atol, rtol, g, step_converged, event_trigger = self._init_solve(t_eval, info, delta_t)

        t_start = t_eval[0]
        t_end = t_eval[-1]

        info = self._solve(self.interface,
                           self.time_events,
                           self.state_events,
                           solve_state,
                           initial_step,
                           dt,
                           order,
                           order_,
                           roller,
                           strict_eval,
                           min_step,
                           max_step,
                           step_integrate_,
                           g,
                           step_converged,
                           event_trigger,
                           t_start,
                           t_end,
                           t_eval,
                           1,
                           atol * 1000)

        while info.status == SolveStatus.Running:
            self._trigger_external_events(info.direction, info.t, self.interface.get_states())
            self.event_handler.handle_solve_event(self.interface, info.event_id, info.t)

            info = self._solve(self.interface,
                               self.time_events,
                               self.state_events,
                               info.solve_state,
                               initial_step,
                               info.dt,
                               order,
                               info.order_,
                               info.roller,
                               strict_eval,
                               min_step,
                               max_step,
                               step_integrate_,
                               info.g,
                               info.step_converged,
                               info.event_trigger,
                               info.t,
                               t_end,
                               t_eval,
                               info.ix_eval,
                               atol * 1000)

        self.event_handler.handle_solve_event(self.interface, info.event_id, info.t)
        return info


    def _trigger_external_events(self, direction: int, t: float, y: np.array):
        external_events = [event for event in self.events.values() if event.is_external()]
        for event in external_events:
            if event.is_triggered():
                external_event = self.external_events[event.id]
                y = external_event.run_event_action(self.interface, t, y)
                external_event.post_event(self.interface, direction, t, y)
                event.clear()
                self.interface.set_states(y)

    def register_endstep(self, __end_step):
        """Unused method

        :param __end_step: n/a
        :return:
        """
        self.__end_step = __end_step

    @property
    def solution(self) -> Union[Solution, str, None]:
        """Contains the solution

        :return: The solution object
        :rtype: Union[:class:`solver.interface.Solution`, str, None]
        """
        if hasattr(self.event_handler, 'solution'):
            return self.event_handler.solution
        else:
            return "no solution object in event handler"
