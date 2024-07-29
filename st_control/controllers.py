import streamlit as st

from typing import Any, Callable, Dict, List, Optional

class ControlledWidget:
    """A class to control the value of a streamlit widget based on the value of other widgets.

    To better manage the state of the widgets, this class is used to control the value of a widget based on the value of other widgets.
    If the value of the trigger fields changes, the value of the controlled widget will be reset to the default value.
    Alternatively, a trigger function can be used to determine if the controlled widget should be reset to the default value.

    :param key: The key of the widget to be controlled.
    :type key: str

    :param default_value: The default value of the widget to be controlled.
    :type default_value: Any

    :param trigger_fields: The keys of the widgets that will trigger the controlled widget to reset to the default value if their values change.
    :type trigger_fields: List[str], optional

    :param trigger_func: A function that returns a boolean value to determine if the controlled widget should be reset to the default value.
    :type trigger_func: Callable[[], bool], optional
    """
    def __init__(self,
                 key: str,
                 default_value: Any,
                 trigger_fields: Optional[List[str]] = None,
                 trigger_func: Optional[Callable[[], bool]] = None):
        self.key = key
        self.default_value = default_value
        self.trigger_fields = trigger_fields
        self.trigger_func = trigger_func
        
        # Set Default Values Dictionary
        if '__default_values__' not in st.session_state:
            st.session_state.__default_values__ = {}

        # Set Widget Key to the default value
        if key not in st.session_state:
            st.session_state[key] = default_value
        st.session_state.__default_values__[key] = default_value

        # Set Controlled Widgets Dictionary
        if '__controlled_widgets__' not in st.session_state:
            st.session_state.__controlled_widgets__ = {}
        if self.key not in st.session_state.__controlled_widgets__:
            self.__update_trigger_fields_session_state()  

    def __update_trigger_fields_session_state(self) -> None:
        """Update the trigger fields in the session state."""
        st.session_state.__controlled_widgets__[self.key] = {
            'tracked_trigger_fields': {
                field: st.session_state.get(field) for field in self.trigger_fields or []
            },
        }
            
    def set_trigger_fields(self, trigger_fields: List[str]) -> None:
        """Set the trigger fields of the controlled widget."""
        self.trigger_fields = trigger_fields
        self.__update_trigger_fields_session_state()
        
    def set_trigger_func(self, trigger_func: Callable[[], bool]) -> None:
        """Set the trigger function of the controlled widget."""
        self.trigger_func = trigger_func

    @property
    def trigger_field_values(self) -> Dict[str, Any]:
        """Get the trigger field values of the controlled widget."""
        return st.session_state.__controlled_widgets__[self.key]['tracked_trigger_fields']
    
    @property
    def value(self) -> Any:
        """Get the value of the controlled widget."""
        return st.session_state.get(self.key)
    
    def reset(self) -> None:
        """Reset the controlled widget to the default value and update the trigger fields in the session state."""
        st.session_state[self.key] = self.default_value
        self.__update_trigger_fields_session_state()

    def has_triggered(self) -> bool:
        """Check if the controlled widget has been triggered.
        
        First checks if the trigger function is not None. If it is not None, the trigger function is called.
        If the trigger function is None, the trigger fields are checked to see if their values have changed.
        """
        if self.trigger_func is not None:
            return self.trigger_func()
        elif self.trigger_fields is not None:
            for trigger_field, value in self.trigger_field_values.items():
                if st.session_state.get(trigger_field) != value:
                    return True
            return False
        else:
            return True
        
    def __enter__(self):
        """Context manager Entrance to reset the controlled widget to the default value if it has been triggered."""
        if self.has_triggered():
            st.session_state[self.key] = self.default_value
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Context manager Exit to update the trigger fields in the session state."""
        self.__update_trigger_fields_session_state()