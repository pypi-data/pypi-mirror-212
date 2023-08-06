import numpy as np
from typing import Any, Optional, Tuple

from .base import _Jitter
from numba import literal_unroll
import logging

from numerous.solver.solve_states import SolveEvent

logger = logging.getLogger(__name__)

class _Interface(_Jitter):
    """
    The base interface which contains methods that should **not** be overwritten.
    """
    def __init__(self, model):
        self.model = model

    def get_next_time_event(self, t, time_events) -> Tuple[float, bool]:
        """
        Function that is called after each converged solver step. Returns a tuple which contains an index of the next
        time event action function to be trigged, and the value of the time-step when the function is triggered. Should
        not be overridden. Lots of loops are needed because numba doesn't support fancy indexing on numpy arrays.

        :param t: current time
        :type t: float
        :return: next time event (if any), and bool if time events exist or not

        :rtype: Tuple[float, bool]
        """
        ix = 0
        t_next_event = t
        for time_event in literal_unroll(time_events):
            t_next_event_ = time_event.get_next_event_time(self, t)
            if t_next_event_ < 0:
                continue
            if ix == 0:
                t_next_event = t_next_event_
            t_next_event = min(t_next_event, t_next_event_)
            ix += 1

        if ix == 0:
            return t, False


        for time_event in literal_unroll(time_events):
            if abs(time_event.get_next_event_time(self, t) - t_next_event) < 1e-6:
                time_event.set()

        return t_next_event, True

    def run_events(self, direction: int, t: float, y: np.array, events) -> Tuple[bool, np.array]:
        """
        Called from the solver when time events need to be run
        :param direction: indicating the direction of which the event took place (if state event, else 0)
        :param t: time
        :param y: vector of states
        :param events: the list of events
        :return: a tuple of bool and new states
        """
        external = False
        for event_ in literal_unroll(events):
            if not event_.is_external() and event_.is_triggered():
                y = event_.run_event_action(self, t, y)
                event_.post_event(self, direction, t, y)
                event_.clear()
            elif event_.is_external() and event_.is_triggered():
                external = True
        return external, y

    def get_state_event_results(self, t: float, y: np.array, state_events: Tuple[Any]) -> np.array:
        """
        Returns an array of the state events results
        :param t: current time
        :param y: current states
        :param state_events: a tuple containing all state events
        :return:
        """
        g = np.zeros(len(state_events), dtype='float')
        ix = 0
        for state_event in literal_unroll(state_events):
            g[ix] = state_event.get_event_results(self, t, y)
            ix += 1

        return g

    def get_state_events(self, g, state_events, roller, order, event_tolerance, imax, t_previous, y_previous,
                         t, y) -> Tuple[float, np.array, np.array, bool, int]:
        """
        Function called from :class:`~solver.numerous_solver.NumerousSolver` when step has converged to check if a
        state event occurs between last time and this time.

        :param g: last values of the state event results vector from :meth:`~solver.events.StateEvent.get_event_result`
        :param g_new: current value of the state event results vector
        :param state_events: a tuple containing all :class:`~solver.events.StateEvent` objects
        :param roller: a list of states and times kept up to :param order:
        :param order: the order of :param roller:
        :param event_tolerance: tolerance of the event detection
        :param imax: maximum iteration internally for an event
        :param t_previous: last value of the converged time
        :param y_previous: last values of the converged states
        :param t: current value of the converged time
        :param y: current values of the converged states
        :return:
        """

        g_new = self.get_state_event_results(t, y, state_events)

        directions = np.zeros(len(state_events), dtype='int')
        t_events = np.zeros(len(state_events)) + t
        y_events = np.zeros((len(y), len(state_events)))
        t_event = -1
        y_event = y
        direction = 0
        event_trigger = False

        ix = 0
        for state_event in literal_unroll(state_events):
            directions[ix] = state_event.get_event_directions(self, t, y)
            ix += 1

        up = (g <= 0) & (g_new >= 0) & (directions >= 0)
        down = (g >= 0) & (g_new <= 0) & (directions <= 0)

        ix_trigger = np.concatenate((np.argwhere(up), np.argwhere(down)))

        ix_event = 0
        for state_event in literal_unroll(state_events): # have to unroll to access the event in the tuple
            if ix_event in ix_trigger:
                eps = 1e-6
                status, t_event, y_event = state_event.locate_event(self, event_tolerance/10, imax, t_previous,
                                                                   y_previous, t, y, roller, order)
                t_events[ix_event] = t_event - eps
                y_events[:, ix_event] = y_event
            ix_event += 1

        bidirectional = False
        event_ix = -1
        if min(t_events) < t:
            event_trigger = True
            event_ix = np.argmin(t_events)
            t_event = t_events[event_ix]
            y_event = y_events[:, event_ix]
            direction = np.sign((g_new - g)).astype('int')[event_ix]
            g_new = self.get_state_event_results(t_event, y_event, state_events)
            bidirectional = directions[event_ix] == 0

        ix = 0
        for state_event in literal_unroll(state_events): # have to unroll to access the event in the tuple
            if not event_trigger: # no event triggered -> out
                break

            if bidirectional and ix == event_ix and state_event._direction != direction and \
                    abs(t_event - state_event._last_event) < state_event._debounce:
                event_trigger = False
                break
            elif ix == event_ix:
                state_event.set()

            ix += 1

        return t_event, y_event, g_new, event_trigger, direction

    def unset_events(self, events):
        for event in literal_unroll(events):
            event.clear()


class Interface(_Interface):
    """
    The interface is used to connect a :class:`~solver.models.Model` to the solver. Some methods must be implemented
    by the user.
    """
    def get_states(self) -> np.array:
        """Function to get states and return to solver. Must be implemented by user.

        :return: array of states
        :rtype: :class:`numpy.ndarray`
        """
        raise NotImplementedError

    def set_states(self, y: np.array) -> None:
        """Function called by solver to overwrite states. Must be implemented by user.

        :param y: current solver states
        :type y: :class:`numpy.ndarray`
        :return: None
        """
        raise NotImplementedError

    def get_deriv(self, t: float, y: np.array) -> Optional[np.ascontiguousarray]:
        """Function to return derivatives of state-space model. Must be implemented by user if model contains
        derivatives.

        :param t: time
        :type t: float
        :param y: states in numpy format
        :type y: :class:`numpy.ndarray`
        :return: derivatives as array (if any, otherwise None or empty array)
        :rtype: :class:`numpy.ndarray`
        """
        return

    def historian_update(self, t: float, y: np.array) -> SolveEvent:
        """Function called each time the desired solution time evaluation is reached (after convergence)

        :param t: time
        :type t: float
        :return: SolveEvent that can be used to break solver loop for external updates
        :rtype: :class:`~solver.solve_states.SolveEvent`
        """
        return SolveEvent.Historian

    def pre_step(self, t: float, y: np.array) -> None:
        """Function called once every time solver is started, also called when solve resumes after exiting due to
        SolveEvent

        :param t: time
        :type t: float
        :param y: states in numpy format
        :type y: :class:`numpy.ndarray`
        :return: None
        """
        pass

    def init_solver(self, t: float, y: np.array) -> None:
        """Function called at once beginning of solve (normal, or step) method.

        :param t:
        :param y:
        :return:
        """
        pass

    def post_step(self, t: float, y: np.array) -> SolveEvent:
        """Function called every time step has converged, and there was no event step in between.

        :param t: time
        :type t: float
        :param y: current solver and model states in numpy format
        :type y: :class:`numpy.ndarray`
        :return: SolveEvent that can be used to break solver loop for external updates
        :rtype: :class:`~solver.solve_states.SolveEvent`
        """
        return SolveEvent.NoneEvent

    def post_state_event(self, t: float, y: np.array, event_id: str) -> SolveEvent:
        """Function called every time solver has converged to an state event step.

        :param t: time
        :type t: float
        :param y: current solver and model states in numpy format
        :type y: :class:`numpy.ndarray`
        :param event_id: the id of the state event function that was triggered
        :type event_id: str
        :return: SolveEvent that can be used to break solver loop for external updates
        :rtype: :class:`~solver.solve_states.SolveEvent`
        """
        return SolveEvent.StateEvent

    def post_time_event(self, t: float, y: np.array) -> SolveEvent:
        """Function called each time a time event has been reached.

        :param t: time
        :type t: float
        :param y: current solver and model states in numpy format
        :type y: :class:`numpy.ndarray`
        :return: SolveEvent that can be used to break solver loop for external updates
        :rtype: :class:`~solver.solve_states.SolveEvent`
        """

        return SolveEvent.TimeEvent



    def get_jacobian(self, t):
        """
        Method for calculating the jacobian matrix.

        :param t: time
        :type t: float
        :return: should return jacobian matrix

        """
        raise NotImplementedError


