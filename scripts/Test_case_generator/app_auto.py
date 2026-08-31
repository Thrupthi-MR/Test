# app_auto.py

import streamlit as st

from auto_test_generator import generate_test_cases
from verifier import verify_bluetooth_connection


st.title("Bluetooth Test Case Generator")

test_cases = generate_test_cases()

for tc in test_cases:

    st.markdown(f"### {tc['TC_ID']}")
    st.write(f"**Scenario:** {tc['Scenario']}")
    st.write(f"**Expected Result:** {tc['Expected']}")

    user_input = st.text_input(
        f"Enter Pairing Code for {tc['TC_ID']}",
        key=tc["TC_ID"]
    )

    if st.button(
        f"Run {tc['TC_ID']}",
        key=f"BTN_{tc['TC_ID']}"
    ):

        actual = verify_bluetooth_connection(user_input)

        st.write(f"**Actual Result:** {actual}")

        if actual == tc["Expected"]:
            st.success("PASS")
        else:
            st.error("FAIL")

    st.divider()
