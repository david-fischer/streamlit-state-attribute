import logging
from pathlib import Path

import streamlit as st

from streamlit_state_attribute import StateAttribute


class Counter:
    key: str
    value: int = StateAttribute(default=0, rerun="on_change")

    def __init__(self, key: str) -> None:
        self.key = key

    def write(self) -> int:
        """Render streamlit widgets for counter."""
        with st.container(border=True):
            st.text(self.key)
            left, _, mid, _, right = st.columns([1, 4, 1, 4, 1])
            with left:
                if st.button(
                    label="",
                    icon=":material/remove:",
                    key=self.key + "minus",
                    type="primary",
                ):
                    self.value -= 1

            with mid:
                st.text(self.value)
            with right:
                if st.button(
                    label="",
                    icon=":material/add:",
                    key=self.key + "plus",
                    type="primary",
                ):
                    self.value += 1
            return self.value


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    counter = Counter(key="counter_1")
    counter.write()
    counter2 = Counter(key="counter_2")
    counter2.write()


if __name__ == "__main__":
    main()
    with st.expander("Source Code"):
        with Path(__file__).open(encoding="utf-8") as f:
            code = f.read()
        st.code(code, language="python")
