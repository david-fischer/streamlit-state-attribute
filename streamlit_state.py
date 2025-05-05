from enum import EnumMeta, Enum
import inspect

from state_property import StateProperty


class StateEnumMeta(EnumMeta):
    def __new__(mcs, name, bases, namespace, **kwargs):
        cls = super().__new__(mcs, name, bases, namespace, **kwargs)
        # Validate the values immediately when the class is defined
        for member in cls:
            value = member.value
            if callable(value):
                sig = inspect.signature(value)
                if len(sig.parameters) > 0:
                    raise TypeError(
                        f"Factory for {member.name} must not take any arguments "
                        f"(got {len(sig.parameters)} parameters)."
                    )
        return cls


class AbstractStateEnum(Enum, metaclass=StateEnumMeta):
    """Base class that uses StateEnumMeta for validation and dynamic property creation."""

    def __call__(self):
        value = self.value
        if callable(value):
            return StateProperty(key=self.name, default_factory=value)
        else:
            return StateProperty(key=self.name, default=value)
