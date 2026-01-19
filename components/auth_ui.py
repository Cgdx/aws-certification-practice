import streamlit as st
from auth import AuthManager, User
from auth.google_oauth import (
    get_google_oauth_url,
    handle_google_callback,
    is_google_oauth_configured,
    render_google_oauth_setup_instructions,
    get_redirect_uri
)
from typing import Optional


def render_auth_page(auth_manager: AuthManager) -> Optional[User]:
    """
    Render the authentication page with Sign In and Sign Up options.
    Returns the authenticated user or None.
    """
    # First, check for Google OAuth callback
    google_user = handle_google_callback()
    if google_user:
        email, name, picture = google_user
        # Login or register the user via OAuth
        success, message, user = auth_manager.login_or_register_oauth(email, name, "google")
        if success and user:
            st.success(f"Welcome, {name}!")
            return user
        else:
            st.error(message)

    st.title("AWS Solutions Architect Exam Trainer")
    st.markdown("---")

    # Center the auth form
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.subheader("Welcome! Please sign in to continue.")

        # Tabs for Sign In and Sign Up
        tab1, tab2 = st.tabs(["Sign In", "Sign Up"])

        with tab1:
            user = render_sign_in(auth_manager)
            if user:
                return user

        with tab2:
            user = render_sign_up(auth_manager)
            if user:
                return user

    return None


def render_google_button(button_key: str):
    """Render the Google Sign-In button."""
    if is_google_oauth_configured():
        redirect_uri = get_redirect_uri()
        google_url = get_google_oauth_url(redirect_uri)

        if google_url:
            # Use st.link_button for reliable redirect
            st.link_button("🔐 Continue with Google", google_url, use_container_width=True)
        else:
            st.error("Failed to generate Google OAuth URL")
    else:
        # Debug info
        st.warning("Google OAuth not configured - secrets not found")
        # Show setup button that expands instructions
        if st.button("Continue with Google", key=button_key, use_container_width=True):
            st.session_state.show_google_setup = True

        if st.session_state.get("show_google_setup", False):
            render_google_oauth_setup_instructions()


def render_sign_in(auth_manager: AuthManager) -> Optional[User]:
    """Render the sign in form."""
    st.markdown("#### Sign in with your account")

    with st.form("sign_in_form"):
        email = st.text_input("Email", key="signin_email")
        password = st.text_input("Password", type="password", key="signin_password")

        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("Sign In", use_container_width=True)

        if submit:
            if not email or not password:
                st.error("Please fill in all fields")
                return None

            success, message, user = auth_manager.login(email, password)

            if success:
                st.success(message)
                return user
            else:
                st.error(message)

    # Google OAuth
    st.markdown("---")
    st.markdown("##### Or sign in with")
    render_google_button("google_signin")

    return None


def render_sign_up(auth_manager: AuthManager) -> Optional[User]:
    """Render the sign up form."""
    st.markdown("#### Create a new account")

    with st.form("sign_up_form"):
        email = st.text_input("Email", key="signup_email")
        username = st.text_input("Username", key="signup_username")
        password = st.text_input("Password", type="password", key="signup_password")
        password_confirm = st.text_input("Confirm Password", type="password", key="signup_password_confirm")

        st.caption("Password must be at least 8 characters with uppercase, lowercase, and a digit.")

        submit = st.form_submit_button("Sign Up", use_container_width=True)

        if submit:
            if not email or not username or not password:
                st.error("Please fill in all fields")
                return None

            if password != password_confirm:
                st.error("Passwords do not match")
                return None

            success, message, user = auth_manager.register(email, username, password)

            if success:
                st.success(message)
                st.info("You can now sign in with your new account.")
                return user
            else:
                st.error(message)

    # Google OAuth
    st.markdown("---")
    st.markdown("##### Or sign up with")
    render_google_button("google_signup")

    return None


def render_user_info(user: User):
    """Render user info in the sidebar."""
    st.sidebar.markdown("---")

    # Show provider badge
    provider_badge = ""
    if user.auth_provider == "google":
        provider_badge = " (Google)"

    st.sidebar.markdown(f"**Logged in as:** {user.username}{provider_badge}")
    st.sidebar.markdown(f"*{user.email}*")

    if st.sidebar.button("Sign Out", use_container_width=True):
        # Clear user from session
        if 'user' in st.session_state:
            del st.session_state['user']
        if 'user_id' in st.session_state:
            del st.session_state['user_id']
        st.rerun()
