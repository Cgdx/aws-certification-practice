import os
import json
import streamlit as st
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from typing import Optional, Tuple
from urllib.parse import urlencode

# OAuth configuration - check st.secrets first (Streamlit Cloud), then os.environ
def get_secret(key: str, default: str = "") -> str:
    """Get secret from Streamlit secrets or environment variables."""
    try:
        return st.secrets.get(key, os.environ.get(key, default))
    except Exception:
        return os.environ.get(key, default)

GOOGLE_CLIENT_ID = get_secret("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = get_secret("GOOGLE_CLIENT_SECRET")

# Scopes for Google OAuth
SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile"
]


def get_google_oauth_url(redirect_uri: str) -> Optional[str]:
    """
    Generate the Google OAuth authorization URL.
    """
    if not GOOGLE_CLIENT_ID:
        return None

    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "access_type": "offline",
        "prompt": "consent"
    }

    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
    return auth_url


def exchange_code_for_token(code: str, redirect_uri: str) -> Optional[dict]:
    """
    Exchange the authorization code for tokens.
    """
    import requests

    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        return None

    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri
    }

    try:
        response = requests.post(token_url, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Token exchange failed: {response.text}")
            return None
    except Exception as e:
        st.error(f"Token exchange error: {str(e)}")
        return None


def get_user_info(access_token: str) -> Optional[dict]:
    """
    Get user info from Google using the access token.
    """
    import requests

    userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get(userinfo_url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to get user info: {response.text}")
            return None
    except Exception as e:
        st.error(f"User info error: {str(e)}")
        return None


def verify_id_token(token: str) -> Optional[dict]:
    """
    Verify a Google ID token and return the user info.
    """
    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            google_requests.Request(),
            GOOGLE_CLIENT_ID
        )
        return idinfo
    except Exception as e:
        st.error(f"Token verification failed: {str(e)}")
        return None


def handle_google_callback() -> Optional[Tuple[str, str, str]]:
    """
    Handle the Google OAuth callback.
    Returns (email, name, picture_url) if successful, None otherwise.
    """
    # Check for authorization code in query params
    query_params = st.query_params

    if "code" not in query_params:
        return None

    code = query_params.get("code")

    # Get the redirect URI (current page without query params)
    # For Streamlit, this is typically the root URL
    redirect_uri = get_redirect_uri()

    # Exchange code for tokens
    tokens = exchange_code_for_token(code, redirect_uri)

    if not tokens:
        return None

    # Get user info
    access_token = tokens.get("access_token")
    if access_token:
        user_info = get_user_info(access_token)
        if user_info:
            email = user_info.get("email", "")
            name = user_info.get("name", user_info.get("given_name", "User"))
            picture = user_info.get("picture", "")

            # Clear the query params after handling
            st.query_params.clear()

            return email, name, picture

    return None


def get_redirect_uri() -> str:
    """
    Get the redirect URI for OAuth callback.
    """
    # Use st.secrets (Streamlit Cloud) or environment variable
    redirect_uri = get_secret("OAUTH_REDIRECT_URI")

    if not redirect_uri:
        # Default to localhost for development
        redirect_uri = "http://localhost:8502"

    return redirect_uri


def is_google_oauth_configured() -> bool:
    """Check if Google OAuth is properly configured."""
    return bool(GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET)


def render_google_oauth_setup_instructions():
    """Render instructions for setting up Google OAuth."""
    st.markdown("""
    ### Google OAuth Setup Required

    To enable Google Sign-In, follow these steps:

    1. **Go to Google Cloud Console**: https://console.cloud.google.com/

    2. **Create a new project** (or select an existing one)

    3. **Enable the Google+ API**:
       - Go to "APIs & Services" > "Library"
       - Search for "Google+ API" and enable it

    4. **Create OAuth 2.0 Credentials**:
       - Go to "APIs & Services" > "Credentials"
       - Click "Create Credentials" > "OAuth client ID"
       - Choose "Web application"
       - Add authorized redirect URIs:
         - `http://localhost:8501` (for development)
         - `http://localhost:8502` (alternate port)
         - Your production URL

    5. **Set Environment Variables**:
       ```
       set GOOGLE_CLIENT_ID=your_client_id_here
       set GOOGLE_CLIENT_SECRET=your_client_secret_here
       set OAUTH_REDIRECT_URI=http://localhost:8502
       ```

    6. **Restart the application**
    """)
