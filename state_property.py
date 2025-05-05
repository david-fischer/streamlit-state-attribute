# file: state_enum.py

from enum import Enum
from typing import Any, Callable, Optional, Union, TypeVar, Generic
import inspect
import streamlit as st

T = TypeVar("T")


class StateProperty(Generic[T]):
    """Descriptor that holds a default value or creates one via default_factory."""

    def __init__(
        self,
        key: str,
        default: Optional[T] = None,
        default_factory: Optional[Callable[[], T]] = None,
    ):
        self.key: str = key
        self.default: Optional[T] = default
        self.default_factory: Optional[Callable[[], T]] = default_factory
        self._value: Optional[T] = None

    def __get__(self, instance, owner) -> T:
        if self.key in st.session_state:
            return st.session_state[self.key]
        if self.default_factory is not None:
            value = self.default_factory()
        else:
            value = self.default
        self.__set__(instance, value)
        return value

    def __set__(self, instance, value: T):
        st.session_state[self.key] = value


class AbstractStateEnum(Enum):
    """Abstract base class for defining state keys with default values or factories."""

    def __call__(self) -> StateProperty[Any]:
        value = self.value
        if callable(value):
            # Factory (must be 0-arg)
            sig = inspect.signature(value)
            if len(sig.parameters) > 0:
                raise TypeError(f"Factory for {self.name} must not take any arguments.")
            return StateProperty(key=self.name, default_factory=value)
        else:
            # Static value
            return StateProperty(key=self.name, default=value)

    def __init_subclass__(cls) -> None:
        """Validate all enum values when a subclass is created."""
        super().__init_subclass__()
        for member in cls:
            value = member.value
            if callable(value):
                sig = inspect.signature(value)
                if len(sig.parameters) > 0:
                    raise TypeError(
                        f"Factory for {member.name} must not take any arguments "
                        f"(got {len(sig.parameters)} parameters)."
                    )
