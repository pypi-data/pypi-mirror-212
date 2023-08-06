r"""
=============================================================
Solving a differential equation with state events
=============================================================

In the :ref:`time events <sphx_glr_auto_examples_time_events.py>` example we covered adding
:class:`~solver.events.TimeEvent`. Here, we shall cover the basics of :class:`~solver.events.StateEvent`. A state event
occurs when a certain condition is fulfilled. The condition may be anything we can state
mathematically as:

.. math::

    f(z(t_{event})) = 0

That is, a state event is considered triggered once as it crosses the zero-line.

In `numerous solver`, we distinguish between triggering the event if the zero line is crossed from the positive side
towards the negative side, or vice-verse. This means:

.. math::
   :nowrap:

   \begin{eqnarray}
    f(z(t)) & > & 0 & \ \text{AND}\ & f(z(t+dt)) & < & 0 & & \ \text{OR} \\
    f(z(t)) & < & 0 & \ \text{AND} & f(z(t+dt)) & > & 0 & &
   \end{eqnarray}

Therefore, when defining a state event, we must also specify the direction that the event is triggered. Finally once
triggered, the event calls the :meth:`~solver.events.Event.run_event_function`, which is customizable by the user.

In summary, there are 3 functions that must be specified by the user when specifying a
:class:`~solver.events.StateEvent`:

.. _events:

* get_event_directions: a method that returns the direction from negative to positive (+1) or from positive to
  negative (-1), that the event function must cross. If an event can occur for both directions, the user will have to
  specify two separate :class:`~solver.events.StateEvent`.
* run_event_action: the action that is triggered.
* get_event_results: the method that returns the value of the zero-crossing function that determines if an event
  occurs. `numerous solver` uses a iterative method to determine the exact time at which this happens if the
  get_event_directions condition is fulfilled, and the last value of the event function had an opposite sign.

Finally, as was the case with :ref:`time events <sphx_glr_auto_examples_time_events.py>`, the event must be decorated
using the :meth:`~solver.base.event` decorator.

The bouncing ball example of state events
-------------------------------------------

In this example, we model a ball that is released from a specific height. As the ball hits the ground it bounces back
up. This model demonstrates the use of :class:`~solver.events.StateEvent` to implement discrete behavior.

The bouncing ball analytical solution
--------------------------------------

The bouncing ball model calculates the position of a ball dropped from an initial height, at rest. The ball
bounces once it hits the ground, and looses some energy as it bounces back up. This continues until the ball comes
to a rest.

The equation of motion of the ball is:

.. math::

    \frac{d^2x}{dt^2} = -g

where :math:`x` is the position of the ball, and :math:`g` is the gravitational constant.


Integration yields:

.. math::

    x(t) = -\frac{1}{2} g t^2 + v_0 \cdot t + x_0


where :math:`v_0` is the initial velocity and :math:`x_0` is the initial height of the ball. The ball hits the ground
when :math:`x(t) = 0`, so we can solve the above equation to get the initial hit, since :math:`v_0=0` initially:

.. math::

    \Delta t_{hit,1} = \frac{-v_0 + \sqrt{v_0^2 +2gx_0}}{-g}

As the ball hits the ground it looses some momentum, because of the plasticity of the bounce. If we call that loss
:math:`f_{loss}` then the velocity just after the bounce is:

.. math::

    v_{0,1} = g \sqrt{\frac{2 x_0}{g}}(1-f_{loss})

where :math:`v_{0,1}` indicates that it's the initial velocity just after the plastic deformation following hit no. 1.
Entering this into the equation of motion, we may find the time between hit no. 1 and hit no. 2 as:

.. math::

    \Delta t_{hit,2} = 2\sqrt{\frac{2x_0}{g}}(1-f_{loss})

Therefore, the total time for two hits is:

.. math::

    t_{hit,2} = \Delta t_{hit,1} + \Delta t_{hit,2} = \sqrt{\frac{2x_0}{g}} (1+2(1-f_{loss}))

Continuing along, we can find the general expression for N hits:

.. math::

    t_{hit,N} = \sqrt{\frac{2 x_0}{g}} \left ( 2\sum_{i=1}^{N} (1-f_{loss})^{i-1} -1 \right )


Implementation into numerous solver
------------------------------------

~~~~~~~~~~~~~~~~~~~~~~
The equation of motion may also be written as two separate ODE's for implementation into numerous solver:

.. math::

    \frac{dv}{dt} = -g

.. math::

    \frac{dx}{dt} = v

This is implemented in the `BouncingBall` models :meth:`diff` function:

.. code-block::

    @model
    class BouncingBall(Model):
        ...

        def diff(self, t, y):
            dvdt = -self.g
            dxdt = y[1]

        return np.array([dxdt, dvdt], dtype='float')

Creating the event functions to catch the bounce
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Events were discussed in the :ref:`events section <event-classes>` and here we will show an example of adding such an
event. In the case of handling the bounce and momentum loss, the event to implement is a
:class:`~solver.events.StateEvent` as when the ball passes the zero crossing:

.. math::

    x(t) > 0 \rightarrow x(t+t_{event}) < 0

the event is triggered, and the discontinuous `event action` is run:

.. _`event action`:

    .. math::

        v(t_{event}) = -v(t_{event}) (1-f_{loss})

The implementation is as follows:

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

First, the event is decorated by the :meth:`~solver.base.event` decorator, then the state event is created by inherting
the :class:`~solver.events.StateEvent`, and the `three functions <#events>`_ are defined. For the bouncing ball, we want
to catch the event when the ball hits the ground (position = 0), by falling so the event directions are -1. Then, we
want to reduce the momentum of the ball so we return the `modified velocity <#event-action>`_.

Attaching the event to the model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As for the :ref:`time event example <sphx_glr_auto_examples_time_events.py>`, we need to attach the event to the model.
This is done by calling the :meth:`~solver.models.Model.add_state_event` function:

.. code-block::

    bounce = BounceEvent(id='bounce)
    model.add_state_event(bounce)

Specifying the interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The interface is constructed :ref:`as in the previous examples (e.g.
<sphx_glr_auto_examples_simple_differential_equation.py>`):

.. code-block::

    @interface
    class BoucingBallInterface(Interface):
        ...

which contains the usual callback functions to get derivatives, get and set states.

Examples
--------------------

Below is the result of running the bouncing ball model with numerous solver, and the analytical solution plotted on top.
For the first many hits, the time at which the bouncing ball hits the ground is very accurately found by the solver, but
as the solution time progresses, numerical errors build up and eventually the time becomes inaccurate. Tightening the
absolute tolerance, reduces this error, as can be seen from the figure.

"""
import logging

import numpy as np
from numerous.solver import Interface, Model, NumerousSolver, interface, model, StateEvent, event
import plotly.graph_objects as go
import plotly


@model
class BouncingBall(Model):

    def __init__(self, x0=1, v0=0, f_loss=0.05, g=9.81):
        self.x0 = x0
        self.v0 = v0
        self.y = np.array([x0, v0], dtype='float')
        self.f_loss = f_loss
        self.g = g

    def analytical_solution(self, max_hits) -> np.array:
        t_hits = np.zeros(max_hits, dtype='float')
        summation = 0
        for i in range(max_hits):
            summation += (2 * (1 - self.f_loss) ** (i))
            t_hit = np.sqrt(2 * self.x0 / self.g) * (summation - 1)
            t_hits[i] = t_hit

        return t_hits

    def diff(self, t, y):
        dvdt = -self.g
        dxdt = y[1]

        return np.array([dxdt, dvdt], dtype='float')

    def reset(self):
        self.y = np.array([self.x0, self.v0], dtype='float')

@interface
class BouncingBallInterface(Interface):
    model: BouncingBall

    def get_deriv(self, t: float, y: np.array) -> np.ascontiguousarray:
        return self.model.diff(t, y)

    def get_states(self) -> np.array:
        return self.model.y

    def set_states(self, y: np.array) -> None:
        self.model.y = y

@event
class BounceEvent(StateEvent):
    def run_event_action(self, interface: Interface, t: float, y: np.array) -> np.array:
        y[1] = -y[1] * (1 - interface.model.f_loss)
        return y
    def get_event_results(self, interface: Interface, t: float, y: np.array) -> float:
        return y[0]

    def get_event_directions(self, interface: Interface, t: float, y: np.array) -> int:
        return -1


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    model = BouncingBall()
    bounce = BounceEvent(id='bounce')
    model.add_state_event(bounce)
    ATOL = 1e-6
    numsol = NumerousSolver(model=model, use_jit=True, rtol=1e-6, atol=ATOL)
    time = np.append(np.arange(0, 10, 0.1), 10)
    numsol.solve(time)
    t = np.array(numsol.solution.results).T[0, :]
    y = np.array(numsol.solution.results).T[1, :]
    state_events = np.array(numsol.solution.state_event_results).T  # get the events
    t_events = state_events[0,:]  # The time which the ball hits the ground
    y_events = state_events[1,:]  # The position (should be 0) when the ball hits the ground
    num_hits = len(t_events)
    t_analytical = model.analytical_solution(num_hits)

    t_ = np.append(t, t_events)  # Append to solution time vector
    ix_sort = np.argsort(t_)  # Sort arguments and find indexes to apply sorting later
    y_ = np.append(y, y_events)  # Also append position to solution position vector

    fig = go.Figure()  # Create a plotly figure
    fig.add_trace(go.Scatter(x=t_[ix_sort], y=y_[ix_sort], name=f'bouncing ball - tolerance {ATOL}',
                             mode="lines+markers", marker=dict(size=10, symbol='circle-open-dot')))  # Add a trace
    fig.add_trace(go.Scatter(x=t_analytical, y=np.zeros(num_hits), name='analytical solution', mode="markers",
                             marker=dict(size=10, symbol="star-dot")))
    fig.update_layout(xaxis_title='time', yaxis_title='height of ball')  # Add titles

    # Try again, but tighten the tolerance
    numsol.reset()
    numsol.solve(time, atol=ATOL/100)

    state_events = np.array(numsol.solution.state_event_results).T  # get the events
    t_events = state_events[0, :]  # The time which the ball hits the ground
    y_events = state_events[1, :]  # The position (should be 0) when the ball hits the ground
    t_ = np.append(t, t_events)  # Append to solution time vector
    ix_sort = np.argsort(t_)  # Sort arguments and find indexes to apply sorting later
    y_ = np.append(y, y_events)

    fig.add_trace(go.Scatter(x=t_[ix_sort], y=y_[ix_sort], name=f'bouncing ball - tolerance {ATOL/100}',
                             mode="lines+markers", marker=dict(size=10, symbol='square-open-dot')))  # Add a trace
    plotly.io.show(fig)  # Plot figure




