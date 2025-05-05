# Streamlit Session State Property (SSSP)

 * Autosuggestions
 * Type hints
 * Logging each state change (level = info)
 * Easily build Widgets which just need to handle their logic

```python
from st_state import StateProperty

class SomeWidget:
    some_attribute: str = StateProperty(default="test")


# Shared state between all instances
some_widget = SomeWidget()
some_widget.some_attribute = "3" # st.session_state["SomeWidget.some_attribute"]



class SomeWidgetWithKey:
    key: str
    some_attribute: str = StateProperty(default="test")

    def __init__(self, key: str) -> None:
        self.key=key

# Each key will have a separate State
other_widget = SomeWidgetWithKey(key="test")
other_widget.some_attribute = "4" # st.session_state["SomeWidgetWithKey.test.some_attribute"]
```


## Background
Made to play around with [descriptors](https://docs.python.org/3/howto/descriptor.html) after a [workshop about
them at Pycon2025](https://pretalx.com/pyconde-pydata-2025/talk/WJPEQH/).
