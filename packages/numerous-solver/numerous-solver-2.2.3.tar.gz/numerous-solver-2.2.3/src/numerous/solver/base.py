import logging
import numba as nb
import numpy as np
from numba.experimental import jitclass
from numba.core.types.misc import ClassInstanceType

logger = logging.getLogger(__name__)


class _Jitter(object):
    """
    The base class used for jitting models
    """
    _reserved: None
    _assignments: None
    _compiled_model: None

    def _jit(self, jit=False):

        python_model = self

        if not jit:
            object.__setattr__(self, '_compiled_model', python_model)
            return python_model

        if hasattr(self, '_compiled_model'):
            return self._compiled_model

        spec = []

        args = self._add_args(self._reserved['args'], jit=True)
        kwargs = self._add_kwargs(self._reserved["kwargs"], jit=True)

        spec_dict = {}
        for k, v in python_model.__dict__.items():
            if k in {'_reserved', '_interface_factory', '_time_events', '_assignments', '_initialized', '_interface'}:
                continue
            spec_dict.update(self._add_kwargs({k: v}, jit=jit))

        for k, v in spec_dict.items():
            nbtype = nb.typeof(v)
            if type(nbtype) == nb.types.Array:  # Array must be type 'A' -
                # by default the nb.typeof evaluates them to type 'C'
                spec.append((k, nb.types.Array(nbtype.dtype, nbtype.ndim, 'A')))
            else:
                spec.append((k, nbtype))

        class OuterWrapper(type(python_model)):
            pass

        OuterWrapper.__setattr__ = object.__setattr__

        @jitclass(spec=spec)
        class Wrapper(OuterWrapper):
            pass

        object.__setattr__(self, '_compiled_model', Wrapper(*args, **kwargs))
        if hasattr(self, '_assignments'):
            for k, v in self._assignments.items():
                setattr(self, k, v)
        return self._compiled_model

    def _add_args(self, args_: iter, jit=False):
        args__ = []
        for arg in args_:
            if not self._is_reserved_nested_type(arg):
                try:
                    _ = iter(arg)
                    if isinstance(arg, dict):
                        if jit:
                            raise TypeError(f"dicts are not allowed as arguments when jit=True {arg}")
                        args__.append(self._add_kwargs(arg, jit))
                    else:
                        args__.append(self._add_args(arg, jit))
                except TypeError as e:
                    if not "is not iterable" in e.__repr__():
                        raise
                    if isinstance(arg, _Jitter):
                        args__.append(arg._jit(jit=jit))
                    else:
                        args__.append(arg)
            else:
                args__.append(arg)
        return tuple(args__)

    def _add_kwargs(self, kwargs_: dict, jit=False):
        kwargs__ = {}
        for k, v in kwargs_.items():
            if not self._is_reserved_nested_type(v):
                try:
                    _ = iter(v)
                    if isinstance(v, dict):
                        if jit:
                            raise TypeError(f"dicts are not allowed as arguments when jit=True {v}")
                        kwargs__.update({k: self._add_kwargs(v, jit)})
                    else:
                        kwargs__.update({k: self._add_args(v, jit)})
                except TypeError as e:
                    if not "is not iterable" in e.__repr__():
                        raise
                    if isinstance(v, _Jitter):
                        kwargs__.update({k: v._jit(jit=jit)})
                    else:
                        kwargs__.update({k: v})
            else:
                kwargs__.update({k: v})
        return kwargs__

    def _is_reserved_nested_type(self, arg) -> bool:
        return isinstance(arg, (str, np.ndarray))

    def __setattr__(self, key, value):
        if not self.is_initialized():
            object.__setattr__(self, key, value)
            return

        if hasattr(self, '_compiled_model'):
            v_ = getattr(self._compiled_model, key)
            if isinstance(nb.typeof(v_), ClassInstanceType):
                logger.warning(f"cannot set property {key} on {self} to {value} as it is already compiled")
                return
            elif self._compiled_model == self:
                super().__setattr__(key, value)
                return
            object.__setattr__(self, key, value)
            self._compiled_model.__setattr__(key, value)
            return

        if not hasattr(self, "_assignments"):
            object.__setattr__(self, '_assignments', {})
        self._assignments.update({key: value})
        object.__setattr__(self, key, value)

    def is_initialized(self):
        if hasattr(self, "_initialized"):
            return True
        return False


class _Factory:
    """
    The base factory for capturing arguments and keyword arguments.
    """
    class_type: type
    _initialized: bool = False

    def __call__(self, *args, **kwargs):
        new_class = self.create_class(*args, **kwargs)
        self.post_create_class(new_class)
        return new_class

    def create_class(self, *args, **kwargs) -> object:
        raise NotImplementedError

    def post_create_class(self, new_class: object):
        object.__setattr__(new_class, '_initialized', True)


class DefaultFactory(_Factory):
    def create_class(self, *args, **kwargs):
        new_class = self.class_type(*args, **kwargs)
        object.__setattr__(new_class, '_reserved', {'args': args, 'kwargs': kwargs})
        return new_class


def model(model_class: type):
    """
    Decorator for model classes. Contains the ModelFactory, which creates the model object and its interface.
    Sets the interface_factory
    :param model_class: the :class:`~solver.model.Model` to decorate
    :return: returns the :class:`~solver.decorators.model.ModelFactory`
    """

    class ModelFactory(_Factory):
        interface_factory: type = None
        class_type = model_class

        def create_class(self, *args, **kwargs):
            new_class = self.class_type(*args, **kwargs)
            new_class._reserved = {'args': args, 'kwargs': kwargs}
            new_class._interface_factory = self.interface_factory
            return new_class

    return ModelFactory()


def interface(interface_class: type):
    """
    Decorator of interfaces. Contains the InterfaceFactory which creates the interface. Sets the interface_factory
    property on the ModelFactory, using the annotation 'model' on the :class:`~solver.interface.Interface`.
    :param interface_class: the :class:`~solver.interface.Interface` to decorate
    :return: returns the :class:`~solver.decorators.interface.InterfaceFactory`
    """
    model_factory = interface_class.__annotations__.get('model')
    if not model_factory:
        raise AttributeError(f"No model property specified for interface {interface_class}")
    if not issubclass(type(interface_class.__annotations__['model']), _Factory):
        raise AttributeError(f"model {model_factory} must be a Factory type")

    class InterfaceFactory(DefaultFactory):
        class_type = interface_class

    model_factory.interface_factory = InterfaceFactory()
    return model_factory.interface_factory


def event(event_class):
    """
    Decorator of events. Contains the EventFactory, which creates the events.
    :param event_class: the :class:`~solver.interface.Event` to decorate
    :return: returns the :class:`~solver.decorators.event.EventFactory`
    """

    class EventFactory(DefaultFactory):
        class_type = event_class

    return EventFactory()


def component(component_class):
    class ComponentFactory(DefaultFactory):
        class_type = component_class

    return ComponentFactory()


class Solution:
    """Default class which holds the solution in arrays.
    """

    def __init__(self):
        self.results = []
        self.state_event_results = []
        self.time_event_results = []

    def add_result(self, t, states):
        """
        Add model states to `results` list

        :param t: time
        :type t: float
        :param states: states to save in `results` list. Can be solver states, can be model states. The user decides
            by specifying in the :class:`~solver.interface.EventHandler`.
        :type states: any
        :return: None
        """
        self.results.append(np.append(t, states))

    def add_state_event_result(self, t_event, states):
        """
        Add model states to ´event_results` list after a state-event.

        :param t_event: time of state event
        :param states: states to save in `event_results` list. Can be solver states, can be model states. The user
            decides by specifying in the :class:`~solver.interface.EventHandler`.
        :return:
        """
        self.state_event_results.append(np.append(t_event, states))

    def add_time_event_result(self, t_event, states):
        """
        Add model states to ´time_event_results` list after a time-event.

        :param t_event:  time of time-event
        :param states: states to save in `time_event_results` list. Can be solver states, can be model states. The user
            decides by specifying in the :class:`~solver.interface.EventHandler`.
        :return:
        """
        self.time_event_results.append(np.append(t_event, states))

    def reset(self):
        self.__init__()
