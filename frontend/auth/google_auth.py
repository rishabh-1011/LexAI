"""
frontend/auth/google_auth.py
Google OAuth authentication using streamlit-oauth.
"""

import requests
import streamlit as st
from streamlit_oauth import OAuth2Component
from backend.config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, REDIRECT_URI

AUTHORIZE_URL     = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL         = "https://oauth2.googleapis.com/token"
REFRESH_TOKEN_URL = "https://oauth2.googleapis.com/token"
REVOKE_TOKEN_URL  = "https://oauth2.googleapis.com/revoke"
SCOPE             = "openid email profile"


def show_google_login(key: str = "google_oauth"):
    """Render Google OAuth login button."""

    oauth2 = OAuth2Component(
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        authorize_endpoint=AUTHORIZE_URL,
        token_endpoint=TOKEN_URL,
        refresh_token_endpoint=REFRESH_TOKEN_URL,
        revoke_token_endpoint=REVOKE_TOKEN_URL,
    )

    try:
        result = oauth2.authorize_button(
            name="Continue with Google",
            icon="https://www.google.com/favicon.ico",
            redirect_uri=REDIRECT_URI,
            scope=SCOPE,
            key=key,
            use_container_width=True,
        )

        if result and "token" in result:
            id_token = result["token"].get("id_token", "")
            if id_token:
                user_info = verify_google_token(id_token)
                if user_info:
                    st.session_state["user"] = {
                        "email":  user_info.get("email"),
                        "name":   user_info.get("name"),
                        "photo":  user_info.get("picture"),
                        "method": "google",
                    }
                    st.session_state["logged_in"] = True
                    st.rerun()

    except Exception as e:
        if "STATE" in str(e) and "DOES NOT MATCH" in str(e):
            # Clear state and show button again
            for k in list(st.session_state.keys()):
                if "oauth" in k.lower() or "state" in k.lower():
                    del st.session_state[k]
            st.rerun()
        else:
            st.error(f"Google login error: {e}")


def verify_google_token(id_token: str) -> dict:
    """Verify Google ID token and return user info."""
    try:
        response = requests.get(
            f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}",
            timeout=10,
        )
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return {}