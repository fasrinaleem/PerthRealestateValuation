import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import streamlit as st
import pandas as pd
from scripts.auth_utils import authenticate_user

# Load styles
with open("app/style/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def render():
    st.markdown("""
    <div class="hero">
        <h1>🔐 Login</h1>
        <p>Enter your credentials to access the AI-powered prediction platform.</p>
    </div>
    """, unsafe_allow_html=True)

    # Show notification at the top if present
    if st.session_state.get("show_toast_login", False):
        msg, level = st.session_state.get("toast_message_login", ("", "info"))
        if level == "success":
            st.success(msg)
        elif level == "warning":
            st.warning(msg)
        else:
            st.error(msg)
        st.session_state.show_toast_login = False  # Reset

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        if authenticate_user(username, password):
            st.session_state.toast_message_login = ("✅ Logged in successfully!", "success")
            st.session_state.show_toast_login = True
            st.session_state.auth_status = "authenticated"
            st.session_state.current_user = username
            st.rerun()  # ✅ Instant refresh after successful login
        else:
            st.session_state.toast_message_login = ("❌ Invalid username or password", "error")
            st.session_state.show_toast_login = True
            st.rerun()  # ✅ Instant refresh after failed login

    st.markdown("<div class='footer'>Secure login using SHA-256 | Perth Real Estate AI</div>", unsafe_allow_html=True)
