# Streamlit Session State Attribute (SSSA)

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Contents**

- [Goal](#goal)
- [Background](#background)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Goal


 * Autosuggestions
 * Type hints
 * Logging each state change (level = info)
 * Easily build Widgets which just need to handle their logic

```python
from streamlit_state_attribute import StateProperty


class SomeWidget:
    some_attribute: str = StateProperty(default="test")


# Shared state between all instances
some_widget = SomeWidget()
some_widget.some_attribute = "3"  # st.session_state["SomeWidget.some_attribute"]


class SomeWidgetWithKey:
    key: str
    some_attribute: str = StateProperty(default="test")

    def __init__(self, key: str) -> None:
        self.key = key


# Each key will have a separate State
other_widget = SomeWidgetWithKey(key="test")
other_widget.some_attribute = "4"  # st.session_state["SomeWidgetWithKey.test.some_attribute"]
```


## Background
Made to play around with [descriptors](https://docs.python.org/3/howto/descriptor.html) after a [workshop descriptors
at Pycon2025](https://pretalx.com/pyconde-pydata-2025/talk/WJPEQH/).
