import streamlit as st
from st_control import ControlledWidget

# Initialize controlled widgets
field1 = ControlledWidget(key='field1', default_value='')
field2 = ControlledWidget(key='field2', default_value='')
controlled_text_input = ControlledWidget(key='my_text_input',
                                         default_value='initial value',
                                         trigger_fields=['field1', 'field2'])

# Create input fields that will trigger the reset
field1 = st.text_input("Field 1", value=st.session_state['field1'], key='field1')
field2 = st.text_input("Field 2", value=st.session_state['field2'], key='field2')

# Use the context manager to manage the widget reset
with controlled_text_input as ctrl:
    text1 = st.text_input("My Text Input", value=ctrl.value, key=ctrl.key)

# Additional widget
another_controlled_widget = ControlledWidget(key='another_widget',
                                             default_value='another initial value',
                                             trigger_func=lambda: st.session_state['field1'] == 'reset')
with another_controlled_widget as w:
    text2 = st.text_input("Another Widget", value=w.value, key=w.widget_key)

st.write(st.session_state)