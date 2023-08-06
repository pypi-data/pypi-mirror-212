from .interface import Interface
from .solve_states import SolveEvent
from .base import Solution

class EventHandler:
    """Event handler abstract class. Used to create event handlers for numerous solver.
    """

    def handle_solve_event(self, interface: Interface, event_id: SolveEvent, t: float):
        """Method called each time the solver exits its inner loop

        :param interface: model interface
        :type interface: :class:`solver.interface.Interface`
        :param event_id: Type of event that lead to the solver breaking its inner loop
        :type event_id: :class:`solver.solve_states.SolveEvent`
        :param t: current solver time
        :type t: float
        :param info: a named tuple containing information from the solver
        :return:
        """

        if event_id == SolveEvent.Historian:
            pass
        elif event_id == SolveEvent.ExternalDataUpdate:
            pass
        elif event_id == SolveEvent.HistorianAndExternalUpdate:
            pass
        elif event_id == SolveEvent.TimeEvent:
            pass
        elif event_id == SolveEvent.StateEvent:
            pass

    def reset_solution(self):
        """Method called when resetting the solution. Must be implemented by user.

        :return:
        """
        raise NotImplementedError

class DefaultEventHandler(EventHandler):
    def __init__(self):
        self.solution = Solution()

    def handle_solve_event(self, interface: Interface, event_id: SolveEvent, t: float):
        """Default method for handling solve events. Solution is saved at each historian timestep, time event, and state
        event

        :param interface: model interface
        :type interface: :class:`solver.interface.Interface`
        :param event_id: Type of event that lead to the solver breaking its inner loop
        :type event_id: :class:`solver.solve_states.SolveEvent`
        :param t: current solver time
        :type t: float
        :return:
        """
        if event_id == SolveEvent.Historian:
            self.solution.add_result(t, interface.get_states())
        elif event_id == SolveEvent.StateEvent:
            self.solution.add_state_event_result(t, interface.get_states())
        elif event_id == SolveEvent.TimeEvent:
            self.solution.add_time_event_result(t, interface.get_states())

    def reset_solution(self):
        """Default method for resetting solution

        :return:
        """
        self.solution.reset()