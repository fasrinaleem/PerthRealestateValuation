import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import streamlit as st
import pandas as pd
from scripts.auth_utils import register_user

# Load styles
with open("app/style/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def render():
    st.markdown("""
    <div class="hero">
        <h1>📝 Register</h1>
        <p>Create a new account to begin exploring property insights and predictions.</p>
    </div>
    """, unsafe_allow_html=True)

    # Only show form if registration hasn't succeeded yet
    if not st.session_state.get("registration_success", False):
        with st.form("register_form"):
            username = st.text_input("Choose a Username")
            email = st.text_input("Email Address")
            password = st.text_input("Create Password", type="password")
            confirm = st.text_input("Confirm Password", type="password")
            submitted = st.form_submit_button("Register")

        if submitted:
            if password != confirm:
                st.error("❗ Passwords do not match.")
            elif not username or not email or not password:
                st.warning("⚠️ Please fill in all fields.")
            else:
                success, message = register_user(username, email, password)
                if success:
                    st.session_state.registration_success = True
                    st.session_state.toast_message = message
                    st.rerun()  # rerun to refresh UI without form
                else:
                    st.error("❌ " + message)
    else:
        # Show success message and button
        st.success("🎉 Registration successful! Please proceed to login.")
        if st.button("🔐 Continue to Login"):
            st.session_state.redirect_to_login = True  # ✅ safe handoff
            st.session_state.registration_success = False
            st.rerun()

    st.markdown("<div class='footer'>Registration secured with SHA-256 encryption | Perth Real Estate AI</div>", unsafe_allow_html=True)
