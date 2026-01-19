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
            # Create a styled Google button using markdown and link
            st.markdown(f"""
                <a href="{google_url}" target="_self" style="text-decoration: none;">
                    <button style="
                        width: 100%;
                        padding: 10px 20px;
                        background-color: #4285F4;
                        color: white;
                        border: none;
                        border-radius: 5px;
                        cursor: pointer;
                        font-size: 16px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        gap: 10px;
                    ">
                        <svg width="18" height="18" viewBox="0 0 18 18" xmlns="http://www.w3.org/2000/svg">
                            <path fill="#fff" d="M17.64 9.2c0-.637-.057-1.251-.164-1.84H9v3.481h4.844c-.209 1.125-.843 2.078-1.796 2.717v2.258h2.908c1.702-1.567 2.684-3.874 2.684-6.615z"/>
                            <path fill="#fff" d="M9 18c2.43 0 4.467-.806 5.956-2.18l-2.908-2.259c-.806.54-1.837.86-3.048.86-2.344 0-4.328-1.584-5.036-3.711H.957v2.332A8.997 8.997 0 0 0 9 18z"/>
                            <path fill="#fff" d="M3.964 10.71A5.41 5.41 0 0 1 3.682 9c0-.593.102-1.17.282-1.71V4.958H.957A8.996 8.996 0 0 0 0 9c0 1.452.348 2.827.957 4.042l3.007-2.332z"/>
                            <path fill="#fff" d="M9 3.58c1.321 0 2.508.454 3.44 1.345l2.582-2.58C13.463.891 11.426 0 9 0A8.997 8.997 0 0 0 .957 4.958L3.964 7.29C4.672 5.163 6.656 3.58 9 3.58z"/>
                        </svg>
                        Continue with Google
                    </button>
                </a>
            """, unsafe_allow_html=True)
    else:
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
