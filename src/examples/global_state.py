import logging
import math
from pathlib import Path

import streamlit as st

from streamlit_state_attribute import StateAttribute


class GlobalState:
    name: str = StateAttribute(default="Test User")
    age: int = StateAttribute(default=99)
    some_float: float = StateAttribute(default=math.pi, log_level=logging.CRITICAL)
    just_saved: bool = StateAttribute(default=False)


def main() -> None:
    state = GlobalState()

    name = st.text_input("Name", value=state.name)
    age = st.number_input("Age", value=state.age)
    some_float = st.number_input("Some Float", value=state.some_float)

    if st.button(
        label="Save",
        disabled=state.some_float == some_float
        and state.age == age
        and name == state.name,
    ):
        state.some_float = some_float
        state.age = age
        state.name = name
        state.just_saved = True
        st.rerun()

    if state.just_saved:
        st.info("Saving succeeded!")
        state.just_saved = False


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
    with st.expander("Source Code"):
        with Path(__file__).open(encoding="utf-8") as f:
            code = f.read()
        st.code(code, language="python")
