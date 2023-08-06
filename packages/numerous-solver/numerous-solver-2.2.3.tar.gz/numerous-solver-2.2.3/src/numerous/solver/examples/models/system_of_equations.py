r"""
===========================================
Solving a system of differential equations
===========================================

Numerous solver can be used to solve simple differential equations such as
:ref:`sphx_glr_auto_examples_simple_differential_equation.py`, but naturally it may also be used to solve systems of ODE´s.

Such an example is the Coupled tanks model. In the coupled tanks model, :math:`n_{tanks}` number of identical tanks are
connected through identical valves, which allow a liquid to flow from the initially full tank :math:`0`, to the final
tank, :math:`n_{tanks}`. The final tank has no outlet and all liquid stays there.

Coupled tanks model
----------------------------

The equation of mass conservation for tank :math:`i` is:

.. math::

    \frac{dm_i}{dt} = flow_{in,i} - flow_{out,i}


If tank :math:`i` is connected to tank :math:`i-1` at it's inlet and tank :math:`i+1` at it's outlet, and both inlet
and outlet are connected via identical valves with valve constant :math:`k_{valve}` then:

.. math::

    \frac{dm_i}{dt} = k (m_{i-1}) - m_{i})

The difference is for tank :math:`0` and tank :math:`n_{tanks}` where the inlet, respectively outlet is zero:

.. math::

    \frac{dm_0}{dt} = -k m_{1}

and

.. math::

    \frac{dm_{n_{tanks}}}{dt} = k m_{n_{tanks}-1}


Implementation in numerous solver
------------------------------------
The model :class:`CoupledTanks` is derived from the :class:`~solver.models.Model` class, and decorated by the
:meth:`~solver.base.model` decorator. There, we specify a method for calculating the derivatives of the states:

.. code-block::

    @model
    class CoupledTanks(Model)
    ...
        def diff(self, y: np.array) -> np.array:
            y_dot = np.zeros_like(y)
            for tank in range(len(y)):
                if tank == 0:
                    inlet = 0
                else:
                    inlet = self.k * y[tank - 1]

                if tank == len(self.y) - 1:
                    outlet = 0
                else:
                    outlet = self.k * y[tank]

                diff = inlet - outlet
                y_dot[tank] = diff
            return y_dot

The model requires an :class:`Interface` derived from the :class:`~solver.interface.Interface`, decorated by the
 :meth:`~solver.base.interface` decorator, and using type annotations for the linking :class:`Model` to
 :class:`Interface`:

.. code-block::

    @interface
    class CoupledTanksInterface(Interface):
        model: CoupledTanks


The interface needs to specify the following methods:

* :meth:`get_deriv`
* :meth:`get_states`,
* :meth:`set_states`,

which have been implemented in the :class:`CoupledTanksInterface` below.

Examples
--------------
Below is an example code that runs the model, and creates a plot for `n_tanks=5`.

"""
import logging

import numpy as np
import plotly.graph_objects as go
import plotly

from numerous.solver import model, interface, Model, Interface, NumerousSolver


@model
class CoupledTanks(Model):

    def __init__(self, n_tanks=10, start_volume=10.0, k=1.0):
        self.n_tanks = n_tanks
        self.start_volume = start_volume
        self.y = np.zeros(self.n_tanks, dtype='float')
        self.y[0] = start_volume
        self.k = k

    def diff(self, y: np.array) -> np.array:
        """This method calculates the derivative of the volume in each tank

        :param y: current states
        :type y: :class:`numpy.ndarray`
        :return: an array of the derivatives of the volume in each tank
        :rtype: :class:`numpy.ndarray`
        """
        y_dot = np.zeros_like(y)
        for tank in range(len(y)):
            if tank == 0:
                inlet = 0
            else:
                inlet = self.k * y[tank - 1]

            if tank == len(self.y) - 1:
                outlet = 0
            else:
                outlet = self.k * y[tank]

            diff = inlet - outlet
            y_dot[tank] = diff
        return y_dot

    def reset(self):
        self.y = np.zeros(self.n_tanks, dtype='float')
        self.y[0] = self.start_volume


@interface
class CoupledTanksInterface(Interface):
    model: CoupledTanks

    def get_deriv(self, t: float, y: np.array) -> np.array:
        return self.model.diff(y)

    def set_states(self, y):
        self.model.y = y

    def get_states(self):
        return self.model.y


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    n_tanks = 5
    model = CoupledTanks(n_tanks=n_tanks)
    numsol = NumerousSolver(model=model, use_jit=False)
    time = np.append(np.arange(0, 20, 0.1), 20)

    numsol.solve(time)

    t = np.array(numsol.solution.results).T[0, :]  # Extract the solution time from the solution object
    results = np.array(numsol.solution.results).T  # Extract the results from the solution object

    fig = go.Figure()  # Create a plotly figure
    for i in range(n_tanks):
        fig.add_trace(go.Scatter(x=t, y=results[i+1], name=f'tank no {i+1}'))  # Add a trace
    fig.update_layout(xaxis_title='time', yaxis_title='liquid volume')  # Add titles

    plotly.io.show(fig)  # Plot figure

