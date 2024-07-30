import streamlit as st
from auth import register_user

def render_register_page():
    st.title("Register")

    new_username = st.text_input("New Username", key="register_username")
    new_password = st.text_input("New Password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")

    if st.button("Register", key="register_submit"):
        if new_password != confirm_password:
            st.error("Passwords do not match")
        elif new_username and new_password:
            register_user(new_username, new_password)
            st.success("User registered successfully")

            # Set the registration flag and rerun to trigger the login page
            st.session_state['registration_successful'] = True
            st.session_state['show_register_page'] = False
            st.experimental_rerun()
