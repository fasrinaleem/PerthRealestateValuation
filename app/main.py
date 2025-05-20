import streamlit as st

# Set page config
st.set_page_config(
    page_title="Perth Real Estate AI App",
    layout="wide",
    initial_sidebar_state="expanded"
)

from components import home, prediction, budget_explorer, login, register, insights, compare_models, train_models, smart_recommender, trend_forecaster  
from streamlit_option_menu import option_menu
import os

# Load custom styles
with open("app/style/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Early redirect from registration page ---
if st.session_state.get("redirect_to_login", False):
    st.session_state.auth_option = "Login"
    st.session_state.redirect_to_login = False
    st.rerun()

# --- Show toast (register) ---
if st.session_state.get("show_toast", False):
    msg, level = st.session_state.get("toast_message", ("", "info"))
    if level == "success":
        st.success(msg)
    elif level == "warning":
        st.warning(msg)
    else:
        st.error(msg)
    st.session_state.show_toast = False

# --- Show toast (login) ---
if st.session_state.get("show_toast_login", False):
    msg, level = st.session_state.get("toast_message_login", ("", "info"))
    if level == "success":
        st.success(msg)
    elif level == "warning":
        st.warning(msg)
    else:
        st.error(msg)
    st.session_state.show_toast_login = False

# --- SIDEBAR ---
with st.sidebar:
    st.image("assets/estate.png", width=200)

    if st.session_state.get("auth_status") not in ["authenticated", "guest"]:
        st.markdown("## 🔐 User Access")

        auth_option = option_menu(
            menu_title="Login/Register",
            options=["Login", "Register", "Continue as Guest"],
            icons=["box-arrow-in-right", "person-plus", "person-circle"],
            menu_icon="person-lines-fill",
            default_index=["Login", "Register", "Continue as Guest"].index(
                st.session_state.get("auth_option", "Login") if "auth_option" in st.session_state else "Login"
            ),
            key="auth_option"
        )

        # ✅ Guest confirmation flow
        if auth_option == "Continue as Guest":
            if not st.session_state.get("guest_confirmed", False):
                st.warning("👋 Are you sure you want to continue as a guest?")
                if st.button("✅ Yes, continue as Guest"):
                    st.session_state.auth_status = "guest"
                    st.session_state.current_user = "Guest"
                    st.session_state.guest_confirmed = True
                    st.rerun()
            else:
                st.session_state.auth_status = "guest"
                st.session_state.current_user = "Guest"
                st.rerun()

    else:
        st.markdown(f"""
            <div style="padding:1rem 0;">
                👋 <b>Welcome, {st.session_state.get("current_user", "Guest")}!</b>
            </div>
        """, unsafe_allow_html=True)

        # ✅ Full logout: clears session
        if st.button("Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

# --- MAIN PANEL LOGIC ---
if st.session_state.get("auth_status") not in ["authenticated", "guest"]:
    if st.session_state.get("auth_option", "Login") == "Login":
        login.render()
    elif st.session_state.get("auth_option") == "Register":
        register.render()
else:
    # Authenticated or guest UI
    with st.sidebar:
        st.markdown("## 📍 Navigation")
        selection = option_menu(
                menu_title="Navigation",
                    options=[
                        "Home",
                        "Train Models",
                        "Predict",
                        "Explore by Budget",
                        "Smart Recommender",
                        "Trend Forecaster",    
                        "Insights",
                        "Model Comparison"
                    ],
                    icons=[
                        "house-door",
                        "cpu",
                        "cash-coin",
                        "geo-alt",
                        "map",
                        "graph-up",                  
                        "bar-chart-line",
                        "clipboard-data"
                    ],
                    menu_icon="columns-gap",
                    default_index=0,
                    key="nav_option"
                )

    st.markdown(f"""
        <div class="hero">
            <h1>🏠 Perth Real Estate AI App</h1>
            <p>Welcome, {st.session_state.get("current_user", "Guest")}! Navigate using the sidebar.</p>
        </div>
    """, unsafe_allow_html=True)

    if selection == "Home":
        home.render()
    elif selection == "Train Models":
        train_models.render()
    elif selection == "Predict":
        prediction.render()
    elif selection == "Explore by Budget":
        budget_explorer.render()
    elif selection == "Smart Recommender":
        smart_recommender.render()
    elif selection == "Trend Forecaster":
        trend_forecaster.render()
    elif selection == "Insights":
        insights.render()
    elif selection == "Model Comparison":
        compare_models.render()



# --- Footer ---
st.markdown("""
    <div class="footer">
        © 2025 Perth Real Estate AI — Fasrin, Khushiben, Rabindra
    </div>
""", unsafe_allow_html=True)
