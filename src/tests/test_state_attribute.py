from __future__ import annotations

import logging

import pytest
from inline_snapshot import snapshot


def test_shared_state_key_and_assignment(ssa, st) -> None:
    """Attributes without unique_attribute are class-scoped."""

    class SomeWidget:
        some_attribute: str = ssa.StateAttribute(default="test")

    w = SomeWidget()
    w.some_attribute = "3"
    assert st.session_state == snapshot({"SomeWidget.some_attribute": "3"})


def test_shared_state_sync(ssa, st) -> None:
    """Attributes without unique_attribute are class-scoped."""

    class SomeWidget:
        some_attribute: str = ssa.StateAttribute(default="test")

    w = SomeWidget()
    v = SomeWidget()
    w.some_attribute = "5"
    assert v.some_attribute == w.some_attribute
    v.some_attribute = "3"
    assert v.some_attribute == w.some_attribute
    assert st.session_state == snapshot({"SomeWidget.some_attribute": "3"})


def test_per_instance_state_via_key_attr(ssa, st) -> None:
    """Each instance key gets its own namespace when unique_attribute='key'."""

    class SomeWidgetWithKey:
        key: str
        some_attribute: int = ssa.StateAttribute(default=0, unique_attribute="key")

        def __init__(self, key: str) -> None:
            self.key = key

    w = SomeWidgetWithKey("test")
    w.some_attribute = 4
    assert st.session_state == snapshot({"SomeWidgetWithKey.test.some_attribute": 4})


def test_per_multiple_instances_with_key(ssa, st) -> None:
    """Each instance key gets its own namespace when unique_attribute='key'."""

    class SomeWidgetWithKey:
        key: str
        some_attribute: int = ssa.StateAttribute(default=0, unique_attribute="key")

        def __init__(self, key: str) -> None:
            self.key = key

    w = SomeWidgetWithKey("test")
    v = SomeWidgetWithKey("other_key")
    x = SomeWidgetWithKey("third_key")
    w.some_attribute = 4
    v.some_attribute = 5
    x.some_attribute = w.some_attribute + 5
    assert st.session_state == snapshot(
        {
            "SomeWidgetWithKey.test.some_attribute": 4,
            "SomeWidgetWithKey.other_key.some_attribute": 5,
            "SomeWidgetWithKey.third_key.some_attribute": 9,
        }
    )


def test_per_multiple_instances_with_other_key(ssa, st) -> None:
    """Each instance key gets its own namespace when unique_attribute='key'."""

    class SomeWidgetWithKey:
        other_key: str
        some_attribute: int = ssa.StateAttribute(
            default=0, unique_attribute="other_key"
        )

        def __init__(self, key: str) -> None:
            self.other_key = key

    w = SomeWidgetWithKey("test")
    v = SomeWidgetWithKey("other_key")
    x = SomeWidgetWithKey("third_key")
    w.some_attribute = 4
    v.some_attribute = 5
    x.some_attribute = w.some_attribute + 5
    assert st.session_state == snapshot(
        {
            "SomeWidgetWithKey.test.some_attribute": 4,
            "SomeWidgetWithKey.other_key.some_attribute": 5,
            "SomeWidgetWithKey.third_key.some_attribute": 9,
        }
    )


def test_attribute_not_implemented(ssa) -> None:
    """Each instance key gets its own namespace when unique_attribute='key'."""

    class SomeWidgetWithKey:
        other_key: str
        some_attribute: int = ssa.StateAttribute(default=0, unique_attribute="key")

        def __init__(self, other_key: str) -> None:
            self.other_key = other_key

    w = SomeWidgetWithKey("test")

    with pytest.raises(AttributeError):
        w.some_attribute = 1


def test_default_initialization_when_missing(ssa, st) -> None:
    """Reading missing value initializes from default and stores it."""

    class C:
        val: int = ssa.StateAttribute(default=7)

    c = C()
    assert c.val == 7
    assert st.session_state == snapshot({"C.val": 7})


def test_default_factory_precedence(ssa, st) -> None:
    """default_factory is preferred over default."""

    class D:
        val: int = ssa.StateAttribute(default=1, default_factory=lambda: 2)

    d = D()
    print(d.val)
    assert d.val == 2
    assert st.session_state == snapshot({"D.val": 2})


@pytest.mark.parametrize(
    ("rerun_policy", "values", "expected_calls"),
    [
        ("never", [1, 1, 2], 0),
        ("on_change", [1, 1, 2, 2, 3], 3),  # only when value changes
        ("on_assignment", [1, 1, 2, 2], 4),  # every assignment
        ("on_assignment", [1, 1, 2, 2, 3], 5),  # every assignment
    ],
)
def test_rerun_policies(
    rerun_policy: str, values: list[int], expected_calls: int, ssa, st
) -> None:
    """Verify rerun behavior across policies."""

    class E:
        v: int = ssa.StateAttribute(
            default=0, rerun=rerun_policy, log_level=logging.CRITICAL
        )

    e = E()
    for v in values:
        e.v = v

    assert st.n_reruns() == expected_calls
