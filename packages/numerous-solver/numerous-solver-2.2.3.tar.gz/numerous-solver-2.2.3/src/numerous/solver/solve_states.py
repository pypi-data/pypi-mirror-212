from enum import IntEnum, unique

@unique
class SolveStatus(IntEnum):
    """
    Internal class. Sets the solver status, to either continue or break solver inner- and outer-loop. Used for
    :meth:`~solver.numerous_solver.NumerousSolver.solver_step` and :meth:`~solver.numerous_solver.NumerousSolver.solve`
    Should not be modified by user.
    """
    Running = 0
    Finished = 1


@unique
class SolveEvent(IntEnum):
    """
    Holds the solver events, which can be used to control the solver flow. The different names are just placeholders
    that can be used in whatever way the user wants. The only thing in common is that except for a `NoneEvent`, all
    other events causes the solver to break the inner loop and call the :class:`~solver.interface.EventHandler`.

    Nevertheless, here's the intended use of the events, and as they are used in the default
    :class:`~solver.interface.Interface` and :class:`~solver.interface.DefaultEventHandler`

    :param NoneEvent: Do nothing. Similar to pass.
    :param Historian: After convergence, upon reaching the next time evaluation, exit the solver inner loop and save
        the solution in a dataframe, list, dict etc.
    :param ExternalDataUpdate: After convergence, exit the solver inner loop and load input data from a dataframe or
        database (currently not implemented).
    :param HistorianAndExternalUpdate: After convergence, upon reaching the next time evaluation, exit the solver inner
        loop, save the solution, and load input data from a dataframe etc. (currently not implemented).
    :param StateEvent: After reaching a state event, exit the solver inner loop and save the states to the solution.
    :param TimeEvent: After reaching a time event, exit the solver inner loop and save the states to the solution.

    The user may add more events if they so wish.

    """
    NoneEvent = 0
    Historian = 1
    ExternalDataUpdate = 2
    HistorianAndExternalUpdate = 3
    StateEvent = 4
    TimeEvent = 5





