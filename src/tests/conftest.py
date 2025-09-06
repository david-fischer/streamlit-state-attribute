import importlib
import sys
from types import SimpleNamespace
from unittest.mock import patch

import pytest


@pytest.fixture
def st() -> SimpleNamespace:
    calls: list[str] = []

    def rerun() -> None:
        calls.append("rerun")

    def n_reruns() -> int:
        return len(calls)

    return SimpleNamespace(session_state={}, rerun=rerun, n_reruns=n_reruns)


@pytest.fixture
def ssa(st: SimpleNamespace):
    with patch.dict(sys.modules, {"streamlit": st}):
        import streamlit_state_attribute as ssa  # noqa: PLC0415

        importlib.reload(ssa)  # ensure fresh bind
        yield ssa
