"""
Email Magic Link Authentication
"""

import requests
import streamlit as st

from backend.config import _get_secret

FIREBASE_API_KEY = _get_secret("FIREBASE_API_KEY")


def send_magic_link(email: str):

    url = (
        "https://identitytoolkit.googleapis.com/v1/"
        f"accounts:sendOobCode?key={FIREBASE_API_KEY}"
    )

    payload = {
        "requestType": "EMAIL_SIGNIN",
        "email": email,
        "continueUrl": _get_secret(
            "REDIRECT_URI",
            "http://localhost:8501/",
        ),
    }

    try:
        r = requests.post(url, json=payload, timeout=10)
        return r.status_code == 200
    except Exception:
        return False


def show_email_login(key_prefix="login"):

    st.markdown("#### 📧 Email Magic Link")

    email = st.text_input(
        "Enter your email",
        placeholder="you@example.com",
        key=f"{key_prefix}_email_input",
    )

    if st.button(
        "Send Magic Link",
        key=f"{key_prefix}_email_button",
        use_container_width=True,
    ):

        if not email:

            st.error("Please enter an email.")

            return

        with st.spinner("Sending..."):

            ok = send_magic_link(email)

        if ok:

            st.success(
                f"Magic link sent to **{email}**"
            )

            st.session_state[f"{key_prefix}_email_sent"] = True

        else:

            st.error("Failed to send Magic Link.")