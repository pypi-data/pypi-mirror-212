r"""

================================================
Solving a differential equation with time events
================================================
Earlier we introduced :ref:`events <event-classes>`. Part of these are the :class:`~solver.events.TimeEvent`.
Time-events are events that occur at a specified time, like `t=[0.5, 1, 1.5 ...]`. An example of a time-event could be
control logic, which is executed on a different timescale than the physics which is modelled.

Numerous solver contains two types of :class:`~solver.events.TimeEvent` s to support different time events:

* :class:`~solver.events.PeriodicTimeEvent`: for periodic time events, i.e. events that trigger with a fixed period
* :class:`~solver.events.TimestampedEvent` for events that trigger at a specific time, without any particular
  periodicity.

Furthermore, events must be decorated using the :meth:`~solver.base.event` decorator.

In this example, we shall use the :class:`~solver.events.PeriodicTimeEvent` to trigger a noisy inlet flow, and to
trigger the control logic of a PID controller as it attempts to regulate the liquid level of a continuously stirred tank
reactor.

==========================
Example model description
==========================

In this model, liquid flows in and out of a continuously stirred tank. The input flow rate varies, but the level of the
tank is desired to be the same, so the outlet valve is controlled using a PID controller. The model demonstrates the
use of solver time events.

This model also illustrates how to generate more advanced object-oriented models using the
:meth:`~solver.base.component` decorator.


Model of a continuously stirred tank
------------------------------------

The non-steady state mass-balance for a continuously stirred tank reactor (or CSTR) to which a homogeneous liquid  with
constant density, flows is:

.. math::

    \frac{dV}{dt} = \dot{Q}_{in}-\dot{Q}_{out}

where :math:`\dot{Q}_i` is the volumetric flow coming in to, or going out from, the tank. We wish to control the tank
level so that the liquid height :math:`h` of the tank remains approximately constant, in spite of disturbances to the
inlet flow rate :math:`\dot{Q}_{in}`. First we re-write the equation in terms of liquid column height :math:`h`:

.. math::

    \frac{dh}{dt} = \frac{1}{A} \left ( \dot{Q}_{in} - \dot{Q}_{out} \right )

where :math:`A` is the cross-sectional area of the tank.

To control the liquid height, a PID controller is implemented that controls the outlet flow-rate by adjusting the
outlet valve following the `control law`_:

.. _`control law`:

    .. math::

        K_v = k_p (h-h_{set}) + k_i \int (h-h_{set}) dt + k_d \frac{dh}{dt}


where :math:`K_v` is the lumped flow-coefficient of the valve. The flow-rate out follows `Toricelli's law`_:

.. math::

    \dot{Q}_{out} = K_v \sqrt{V}

when the flow is driven by the static pressure inside the tank, and the valve is located at the bottom of the tank.

The inlet flow-rate is assumed to be:

.. math::

    \dot{Q}_{in} = \dot{Q}_{in, nom} \cdot \left ( 1+f_N \cdot N(t) \right )

where :math:`\dot{Q}_{in, nom}` is the nominal flow-rate, :math:`N(t)` is the gaussian white noise (i.e. :math:`\mu=0`,
:math:`\sigma=1`), and :math:`f_N` is the noise level as a fraction of the nominal inlet flow-rate.

A perfect controller of this tank would simply set :math:`\dot{Q}_{out} = \dot{Q}_{in}`, but we are assuming that in a
practical implementation this is not possible, due to difficulties in measuring the flow-rate exactly. This would cause
small errors to eventually build up as large deviations. We shall later show this to be the case, by looking at the case
where we do not control the liquid level, but simply set :math:`\dot{Q}_{out} = \dot{Q}_{in, nom}`.


Implementation in numerous solver
--------------------------------------

To add noise to the inlet flow-rate, and to create an  outlet flow controller that adjusts the outlet valve opening, we
implemented two 'Component' classes, which decorated using the :meth:`~solver.base.component` decorator. The first
:class:`InletNoise` class is constructed like this:

.. code-block::

    @component
    class InletNoise(Component):
        ...

This class contains a :meth:`add_noise` method for adding white noise on the inlet flow-rate:

.. code-block::

    def add_noise(self, t):
        self.actual_flow = self.nominal_flow * (1 + self.noise_level * np.random.normal())

Later, we shall write the trigger to this function, using a :class:`~solver.events.PeriodicTimeEvent`.

The second class is the :class:`OutletFlowController` which is constructed in the same way:

.. code-block::

    @component
    class OutletFlowController(Component):
        ...

The controller contains the control logic that is triggered when the controller is applied. The control logic is a
simple PID controller, that given the liquid column height, adjusts the valve opening trying to keep the set-point
height inside the tank. As for the :class:`InletNoise` class, we shall write a trigger using a
:class:`~solver.events.PeriodicTimeEvent` here as well to trigger the controller.

As mentioned `earlier <#Solving a differential equation with time events>`_, a time event must be decorated using the :meth:`~solver.base.event` decorator
and must inherit one of the two :class:`~solver.events.TimeEvent` classes: periodic, or timestamped.

We want to examine the effect of updating the outlet flow controller on the liquid height. Therefore we add two
:class:`~solver.events.PeriodicTimeEvent`, decorate them using the :meth:`~solver.base.event` decorator, and implement
the missing :meth:`~solver.events.Event.run_event_action` function

.. code-block::

    @event
    class AddInletNoiseTimeEvent(PeriodicTimeEvent):
        def run_event_action(self, interface: Interface, t: float, y: np.array) -> np.array:
            interface.model.inlet_with_noise.add_noise(t)
            return y

    @event
    class OutletControllerTimeEvent(PeriodicTimeEvent):
        def run_event_action(self, interface: Interface, t: float, y: np.array) -> np.array:
            vol = y[0]
            h = vol / interface.model.a
            dt = self.period
            interface.model.outlet_flow_controller.trigger_controller(t, h, dt)
            return y

The two components were then added to the main :class:`Tank` model, which implements the
`Model of a continuously stirred tank`_:

.. code-block::

    @model
    class Tank(Model):

        def __init__(self, v0: float = 1.0, a: float = 1.0,
                 inlet_with_noise: InletNoise = None, outlet_flow_controller: OutletFlowController = None):

The physics of the tank was implemented in the :meth:`diff` method.

The model :class:`Tank` takes the following inputs:

======================         ======================================================================
Parameter                      Description
======================         ======================================================================
v0                             The initial volume of the tank
a                              The cross-sectional area of the tank
inlet_with_noise               An instance of the :class:`InletNoise` component
outlet_flow_controller         An instance of the :class:`OutletFlowController` component
======================         ======================================================================

The component :class:`InletNoise` takes the following inputs:

==================  ======================================================================
Parameter           Description
==================  ======================================================================
noise_level         The white noise level as a percentage of the input flow
nominal_flow        The inlet flow-rate without any noise
==================  ======================================================================

While the component :class:`OutletFlowController` takes the following inputs:

==================  ====================================================================
Parameter           Description
==================  ====================================================================
k_p                 P-part of the PID controller, i.e. proportional gain
k_i                 I-part of the PID controller, i.e. integral gain
k_d                 D-part of the PID controller, i.e. differential gain
h_set               Liquid height set-point
==================  ====================================================================

The two triggers :class:`AddInletNoiseTimeEvent` and :class:`OutletControllerTimeEvent` take the following inputs:

.. _time_event_table:

===================  ====================================================================
Parameter            Description
===================  ====================================================================
id                   a unique identifier for that trigger (name)
period               The time-period for which the event is triggered
===================  ====================================================================

The interface class :class:`TankInterface` is constructed by inheriting the :class:`~solver.interface.Interface` class,
and decorated by the :meth:`~solver.base.interface` decorator:

.. code-block::

    @interface
    class TankInterface(Interface):
        ...

It contains the following methods:

* :meth:`~solver.interface.Interface.get_deriv`
* :meth:`~solver.interface.Interface.set_states`
* :meth:`~solver.interface.Interface.get_states`

Most of these methods have already been discussed elsewhere e.g.
:ref:`sphx_glr_auto_examples_simple_differential_equation.py`.

Generating the model
----------------------------

The tank model is created after first generating the two model components: the outlet flow controller and the inlet
noise component:

.. code-block::  python

    outlet_flow_controller = OutletFlowController(h_set=h_set_0)
    inlet_noise = InletNoise(noise_level=0.0, nominal_flow=flow_in_0)

    model = Tank(inlet_with_noise=inlet_noise,
                                        outlet_flow_controller=outlet_flow_controller,
                                        v0=0.5)  # Create Tank model

Adding time events to model
------------------------------
Once created, the :class:`Tank` model contains a method called :meth:`~solver.models.Model.add_time_events`, which
allows events, such as :class:`~solver.events.PeriodicTimeEvent` to be registered on the model. To add them,
first the events are created with their respective inputs (id and period, see the `table <#time-event-table>`_), and
then added:

.. code-block::  python

    inlet_trigger = AddInletNoiseTimeEvent(id='inlet_trigger', period=1)
    outlet_trigger = OutletControllerTimeEvent(id='outlet_trigger', period=1)

    model.add_time_events([inlet_trigger, outlet_trigger])


Examples
--------------
We solved the cases where we use a PID controller, and examined the effect of the update frequency.
Below is an example code that runs the model, and creates a plot of the tank height for these two cases, with increasing
noise on the inlet flow-rate (disturbance). Initially the liquid height is assumed to be at it's desired set-point,
then depending on the noise level of the inlet flow, the liquid height starts to vary around the desired set point.
In the case of a slower controller, this variation becomes greater as the noise level increases, while the variation is
much smaller even for high noise levels, whenever a PID controller is used.

.. _`Toricelli's law`:
    https://en.wikipedia.org/wiki/Toricelli%27s_law


"""
import logging

import numpy as np
import pandas as pd

from numerous.solver import Interface, Model, interface, model, PeriodicTimeEvent, component, NumerousSolver, \
    Component, event
import plotly.graph_objects as go
import plotly
import itertools
import plotly.express as px


@component
class OutletFlowController(Component):

    def __init__(self, k_p=1.0, k_i=0.1, k_d=1, h_set=0.5):
        self.k_p = k_p
        self.k_i = k_i
        self.k_d = k_d
        self.i_max = 1000.0
        self.e = 0.0
        self.h_set = h_set
        self.y = np.array([0], dtype='float')
        self.valve_max = np.array([10.0], dtype='float')
        self.initial = True
        self.k_valve = 0.0

    def control_valve(self, t, h, dt):
        e = h - self.h_set
        if self.initial:
            e_old = e
            self.initial = False
        else:
            e_old = self.e
        valve_sp = self.k_p * e + self.k_i * self.y + self.k_d * (e-e_old)/dt
        if valve_sp < 0:
            valve_sp = np.array([0.0], dtype='float')
        if valve_sp > self.valve_max:
            valve_sp = self.valve_max

        self.e = e
        return valve_sp

    def diff(self, y):
        if y <= self.i_max:
            return self.e
        else:
            return 0

    def trigger_controller(self, t, h, dt):
        self.k_valve = self.control_valve(t, h, dt)

    def reset(self):
        self.initial = True


@component
class InletNoise(Component):
    def __init__(self, noise_level: float = 0.0, nominal_flow: float = 0.1):
        self.noise_level = noise_level
        self.nominal_flow = nominal_flow
        self.actual_flow = nominal_flow

    def add_noise(self, t):
        self.actual_flow = self.nominal_flow * (1 + self.noise_level * np.random.normal())

    def reset(self):
        self.actual_flow = self.nominal_flow


@model
class Tank(Model):
    def __init__(self, v0: float = 1.0, a: float = 1.0,
                 inlet_with_noise: InletNoise = None, outlet_flow_controller: OutletFlowController = None):

        self.a = a  # cross-sectional area of tank
        self.v0 = v0
        self.h0 = v0/a
        self.inlet_with_noise = inlet_with_noise
        self.outlet_flow_controller = outlet_flow_controller

        self.initialize()

    def initialize(self):
        self.y = np.array([self.v0, self.h0, self.v0, self.h0], dtype='float')

    def diff(self, t, y) -> np.array:

        dydt = np.empty_like(y, dtype='float')
        vol = y[0]
        h = vol / self.a
        flow_out = self.outlet_flow_controller.k_valve * np.sqrt(h) if h>0 else 0.0

        flow_in = self.inlet_with_noise.actual_flow
        diff_flow = flow_in - flow_out * (flow_out >= 0)
        diff_flow_no_controller = flow_in - self.inlet_with_noise.nominal_flow
        dydt[0] = diff_flow
        dydt[1] = dydt[0] / self.a
        dydt[2] = diff_flow_no_controller
        dydt[3] = dydt[2] / self.a
        return dydt

    def reset(self):
        self.inlet_with_noise.reset()
        self.outlet_flow_controller.reset()
        self.initialize()

@interface
class TankInterface(Interface):
    model: Tank

    def set_states(self, y: np.array) -> None:
        y_cstr = y[:4]
        y_controller = y[4]
        self.model.y = y_cstr
        self.model.outlet_flow_controller.y = np.array([y_controller])

    def get_states(self) -> np.array:
        y = np.empty(5, dtype='float')
        y[:4] = self.model.y
        y[4] = self.model.outlet_flow_controller.y[0]
        return y

    def get_deriv(self, t: float, y: np.array) -> np.array:
        dydt = np.empty(5, dtype='float')
        dydt[:4] = self.model.diff(t, y[:4])
        dydt[4] = self.model.outlet_flow_controller.diff(y[4])
        return dydt

@event
class AddInletNoiseTimeEvent(PeriodicTimeEvent):
    def run_event_action(self, interface: Interface, t: float, y: np.array) -> np.array:
        interface.model.inlet_with_noise.add_noise(t)
        return y

@event
class OutletControllerTimeEvent(PeriodicTimeEvent):
    def run_event_action(self, interface: Interface, t: float, y: np.array) -> np.array:
        vol = y[0]
        h = vol / interface.model.a
        dt = self.period
        interface.model.outlet_flow_controller.trigger_controller(t, h, dt)
        return y

if __name__ == "__main__":
    #  Some plotly stuff to generate the figures
    logging.basicConfig(level=logging.INFO)
    col_pal = px.colors.qualitative.Safe
    lines = ["solid", "dot", "dash", "longdash", "dashdot", "longdashdot"]
    col_pal_iterator = itertools.cycle(col_pal)
    lines_iterator = itertools.cycle(lines)
    fig = go.Figure()

    time = np.append(np.arange(0, 1000, 1), 1000)  # Time to solve - used also as input to tank model to add white noise
    flow_in_0 = 0.1  # The nominal flow-rate without any noise
    noise_levels = [ 10, 50, 75]  # Levels of white noise to simulate - percentage of desired input flow-rate

    h_set_0 = 0.5  # Set-point height of liquid column in tank
    h_set = np.ones_like(time) * h_set_0  # Just a line to show later

    # Create controller and set refresh rate
    outlet_flow_controller = OutletFlowController(h_set=h_set_0)

    # Create controller that is never updated

    inlet_noise = InletNoise(noise_level=0.0, nominal_flow=flow_in_0)
    model = Tank(inlet_with_noise=inlet_noise,
                                        outlet_flow_controller=outlet_flow_controller,
                                        v0=0.5)  # Create Tank model
    inlet_trigger = AddInletNoiseTimeEvent(id='inlet_trigger', period=1)
    outlet_trigger = OutletControllerTimeEvent(id='outlet_trigger', period=1)

    model.add_time_events([inlet_trigger, outlet_trigger])

    numsol = NumerousSolver(model=model, use_jit=True)

    # The compiled model object is available after compiling the solver

    y0 = model.y  # save the initial states when resetting later
    periods = [1, 5, 10]
    summary = []

    for noise_level in noise_levels:
        new_color = next(col_pal_iterator)  # make sure to get the color of the plotly line
        model.inlet_with_noise.noise_level = noise_level / 100 # Set the noise level
        for period in periods:
            line = next(lines_iterator)
            numsol.reset()
            outlet_trigger.period = period

            numsol.solve(time)  # When providing the state vector y0, the interface is reset as well

            t = np.array(numsol.solution.results).T[0, :]  # Extract the solution time from the solution object
            results = np.array(numsol.solution.results).T[2]  # Extract the results from the solution object

            fig.add_trace(go.Scatter(x=t, y=results, name=f"noise level {noise_level} w update period {period}",
                                     line=dict(dash=line, color=new_color)))  # Add a trace with controller

            summary.append({'noise_level': noise_level, 'update period': period, 'std height': np.std(results)})


    df = pd.DataFrame(summary)
    df = df.set_index('noise_level')

    fig.add_trace(go.Scatter(x=time, y=h_set, name='setpoint'))
    fig.update_layout(xaxis_title='time', yaxis_title='liquid height')  # Add titles

    plotly.io.show(fig)  # Plot figure
    print(df)

