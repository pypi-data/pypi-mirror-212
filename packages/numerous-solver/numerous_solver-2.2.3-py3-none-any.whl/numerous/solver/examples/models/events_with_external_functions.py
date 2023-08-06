r"""
================================================================================
Solving a differential equation with events and external action functions
================================================================================

In some cases, the event action function cannot be compiled by numba. This could be if an event triggers an external
API call, or some other function that is for some reason incompatible with numba. Fortunately, `numerous solver`
supports these types of events, both as :class:`~solver.events.TimeEvent` and :class:`~solver.events.StateEvent`, which
are called `external events`.

In this example, we use the :ref:`bouncing ball example <sphx_glr_auto_examples_time_events.py>` but modify the state
event, and set it as an external event. We then compare the results between each other, to validate that the solution is
the same.

Creating an external (state) event
------------------------------------------
For a brief reminder of how events are working, you can take a look at the :ref:`event sections <event-classes>`.
For the bouncing ball, we created the following event:

.. code-block::

    @event
    class BounceEvent(StateEvent):
        def run_event_action(self, interface: Interface, t: float, y: np.array) -> np.array:
            y[1] = -y[1] * (1 - interface.model.f_loss)
            return y
        def get_event_results(self, interface: Interface, t: float, y: np.array) -> float:
            return y[0]

        def get_event_directions(self, interface: Interface, t: float, y: np.array) -> int:
            return -1

We will re-use this event, with a simple modification for the action function, by performing an action otherwise
incompatible with numba, such as creating a new class inside a function scope:

.. code-block::

    def run_event_action(self, interface: Interface, t: float, y: np.array) -> np.array:
        y[1] = -y[1] * (1 - interface.model.f_loss)
        # This is not allowed by numba and will return an error
        class A:
            x = 1
        a = A()
        return y

When we create the event, we will set the `is_external` property to `True`:

.. code-block::

    bounce = BounceEvent(id='bounce', is_external=True)

"""

from numerous.solver.examples.models.discrete_events import BouncingBall, BounceEvent
from numerous.solver import event, NumerousSolver, Interface, StateEvent

import numpy as np
import plotly.graph_objects as go
import plotly
import logging
import traceback

@event
class ExternalBounceEvent(StateEvent):
    def run_event_action(self, interface: Interface, t: float, y: np.array) -> np.array:
        y[1] = -y[1] * (1 - interface.model.f_loss)
        # This is not allowed by numba and will return an error
        class A:
            x = 1
        a = A()
        return y

    def get_event_results(self, interface: Interface, t: float, y: np.array) -> float:
        return y[0]

    def get_event_directions(self, interface: Interface, t: float, y: np.array) -> int:
        return -1

def tb_str(e):
    s = traceback.format_exception(e, value=e, tb=e.__traceback__)
    es = [ss.strip() for ss in s]
    return "\n".join(es)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    use_jit = True

    model = BouncingBall()
    bounce_external = ExternalBounceEvent(id='bounce', is_external=True)

    model.add_state_event(bounce_external)

    numsol = NumerousSolver(model=model, use_jit=use_jit, atol=1e-6, rtol=1e-6)
    time = np.append(np.arange(0, 10, 0.1), 10)
    numsol.solve(time)
    t = np.array(numsol.solution.results).T[0, :]
    y = np.array(numsol.solution.results).T[1, :]
    state_events = np.array(numsol.solution.state_event_results).T  # get the events
    t_events = state_events[0, :]  # The time which the ball hits the ground
    y_events = state_events[1, :]  # The position (should be 0) when the ball hits the ground

    t_ = np.append(t, t_events)  # Append to solution time vector
    ix_sort = np.argsort(t_)  # Sort arguments and find indexes to apply sorting later
    y_ = np.append(y, y_events)  # Also append position to solution position vector

    fig = go.Figure()  # Create a plotly figure
    fig.add_trace(go.Scatter(x=t_[ix_sort], y=y_[ix_sort], name=f'bouncing ball - external event',
                             mode="lines+markers", marker=dict(size=10, symbol='circle-open-dot')))  # Add a trace
    fig.update_layout(xaxis_title='time', yaxis_title='height of ball')  # Add titles

    # Try again, but use internal events - we need to compile again, since the model changes:

    model = BouncingBall()
    bounce_internal = BounceEvent(id='bounce_internal')
    model.add_state_event(bounce_internal)

    numsol = NumerousSolver(model=model, use_jit=use_jit, atol=1e-6, rtol=1e-6)

    numsol.reset()
    numsol.solve(time)

    state_events = np.array(numsol.solution.state_event_results).T  # get the events
    t_events = state_events[0, :]  # The time which the ball hits the ground
    y_events = state_events[1, :]  # The position (should be 0) when the ball hits the ground
    t_ = np.append(t, t_events)  # Append to solution time vector
    ix_sort = np.argsort(t_)  # Sort arguments and find indexes to apply sorting later
    y_ = np.append(y, y_events)

    fig.add_trace(go.Scatter(x=t_[ix_sort], y=y_[ix_sort], name=f'bouncing ball - internal event',
                             mode="lines+markers", marker=dict(size=10, symbol='square-open-dot')))  # Add a trace

    # Finally attempt the same, but set the event to internal (default)
    model = BouncingBall()
    bounce_external_but_internal = ExternalBounceEvent(id='bounce')
    model.add_state_event(bounce_external_but_internal)

    try:
        numsol = NumerousSolver(model=model, use_jit=use_jit)
    except Exception as e:
        logging.error(f"as expected an error was thrown: {tb_str(e)}")

    plotly.io.show(fig)  # Plot figure


