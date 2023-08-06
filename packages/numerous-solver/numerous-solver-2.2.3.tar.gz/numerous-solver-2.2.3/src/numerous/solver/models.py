import logging

import numpy as np
from typing import List
from .base import _Jitter, event as _event
from .interface import Interface
from .events import TimeEvent, StateEvent, Event, MockTimeEvent, MockStateEvent


logger = logging.getLogger(__name__)

class _Model(_Jitter):
    """
    The base model class that contains the hidden methods
    """
    _interface: None
    _interface_factory: None
    def generate_interface(self, jit=False) -> (Interface, List[TimeEvent], List[TimeEvent], List[StateEvent],
                                                List[StateEvent]):
        logger.info("compiling interface")
        interface_factory = getattr(self, '_interface_factory', None)

        if not interface_factory:
            raise AttributeError("no interface assigned to model")

        if hasattr(self, '_interface'): # Do not create new interface if one exists already
            interface = self._interface
        else:
            interface = interface_factory(model=self)
            object.__setattr__(self, '_interface', interface)

        interface._jit(jit=jit)

        time_events, external_time_events = self._compile_events(jit, MockTimeEvent, '_time_events')#self._compile_time_events(jit)
        state_events, external_state_events = self._compile_events(jit, MockStateEvent, '_state_events')#self._compile_state_events(jit)

        return interface, time_events, external_time_events, state_events, external_state_events

    def _compile_events(self, jit: bool, mockclass: type(Event), event_type: str) -> (List[Event], List[Event], bool):
        """
        Compiles events and returns a list of all events used internally in the solver loop, and the
        external ones used outside the loop.
        :param jit: True if jitting
        """

        all_events = []
        external_events = []

        def copy_event(event):
            @_event
            class EventCopy(type(event)):
                def run_event_action(self, interface: Interface, t:float, y: np.array) -> np.array:
                    return y
            return EventCopy(*event._reserved['args'], **event._reserved['kwargs'])

        if hasattr(self, event_type):
            events = getattr(self, event_type)
            for event in events:
                external_event = None
                event_ = event
                if event.is_external():
                    external_event = event_
                    event_ = copy_event(event_)
                event_._jit(jit=jit)
                if external_event:
                    # Link the compiled models
                    object.__setattr__(external_event, '_compiled_model', event_._compiled_model)
                    external_events.append(external_event)
                all_events.append(event_)
        else:
            mock_event = mockclass(id='mock', is_external=False)
            mock_event._jit(jit=jit)
            all_events.append(mock_event)

        return all_events, external_events


class Model(_Model):
    """
    The model class from which models must be derived
    """
    _state_events: None
    _time_events: None
    def add_time_event(self, event: TimeEvent):
        """
        Adds a time event to the model

        :param event: a :class:`~solver.events.TimeEvent`
        :return:
        """
        if not issubclass(type(event), TimeEvent):
            raise ValueError("expected a TimeEvent")
        if not hasattr(self, '_time_events'):
            object.__setattr__(self, '_time_events', [])
        self._time_events.append(event)

    def add_state_event(self, event: StateEvent):
        """
        Adds a state event to the model

        :param event: a :class:`~solver.events.StateEvent`
        :return:
        """

        if not issubclass(type(event), StateEvent):
            raise ValueError("expected a StateEvent")
        if not hasattr(self, '_state_events'):
            object.__setattr__(self, '_state_events', [])
        self._state_events.append(event)

    def add_time_events(self, events: List[TimeEvent]):
        """
        Adds a list of time events to the model
        :param events: a list of :class:`~solver.events.TimeEvent`
        :return:
        """
        for event in events:
            self.add_time_event(event)

    def add_state_events(self, events: List[StateEvent]):
        """
        Adds a list of state events to the model

        :param events: a list of :class:`~solver.events.StateEvent`
        :return:
        """
        for event in events:
            self.add_state_event(event)

    def reset(self):
        """
        Methods for resetting the model. Must be implemented if the
        :meth:`~solver.numerous_solver.NumerousSolver.reset` method is called

        :return:
        """
        raise NotImplementedError

class Component(_Jitter):
    """
    The base class for components
    """
    pass