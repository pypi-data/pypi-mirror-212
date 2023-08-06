## A jitable object-oriented ODE solver for numerical simulations

## Overview:
Numerous solver is a fast, jitable, highly customizable, and object-oriented ODE (ordinary differential equations) 
solver. 

## How to get started

Install the package via `pip install numerous-solver`, or clone the 
[git repository](https://gitlab.com/numerous/numerous-solver) and install using the `setup.py` 
file.

## Documentation
Please see the [gitlab pages](https://numerous.gitlab.io/numerous-solver/) site for documentation.

### Design philosophy
The `numerous solver` is the choice of ODE (ordinary differential equations) solver for `numerous engine` 
(https://github.com/fossilfree/numerous). It is developed following a set of principles:

- **Object-oriented**: A python-based solver should take advantage of the class structure of python. Numerous solver uses 
"models" and "interfaces" to manage the state-flow between the numerical model and the numerical solver.
- **Customizable**: Using "solver events", the solver can be customized to break the solver loop in order to read external
data, save outputs to database, print status messages etc. This allows a great degree of customization.
- **Support time- and state-events**: Built-in support for time- and state-events to support advanced models, controllers 
and physics discontinuities.
- **Jitable**: `Numerous solver` may be compiled with numba (https://numba.pydata.org/) to, in some cases, increase speed. 
The build-in toolchain can assist the user to write (njit) compilable models. 
- **Extendable**: Numerous solver currently supports 3 methods (RK45, BDF, Euler) and can be extended with new solve 
methods.
- **Open-source**: The code base is open for contributions.
