"""
frontend/pages/auth.py
Authentication page for LexAI.
"""

import streamlit as st
from frontend.utils.session import go_landing
from frontend.auth.google_auth import show_google_login
from frontend.auth.email_auth import show_email_login
from frontend.auth.phone_auth import show_phone_login


def show_auth():
    """Render authentication page."""

    # Reset Google widget state
    st.session_state.pop("_google_rendered", None)

    col_left, col_right = st.columns([1, 1])

    # ---------------- LEFT ---------------- #
    with col_left:
        st.markdown("""
        <div style='padding:2rem 1rem;'>
            <h1 style='font-size:2.5rem;'>⚖️ LexAI</h1>
            <h3 style='color:#00d4ff;'>Your AI Legal Assistant</h3>
            <p style='color:#aaa;'>
            Analyze contracts, NDAs, rental agreements,
            and legal notices instantly.
            </p>
        </div>
        """, unsafe_allow_html=True)

        highlights = [
            ("🧠", "RAG-powered analysis grounded in Indian law"),
            ("📄", "Supports PDF, DOCX, TXT, PNG, JPG"),
            ("🌐", "4 output languages"),
            ("🔊", "Voice output"),
            ("💬", "Interactive legal Q&A"),
            ("🛡️", "Secure Firebase authentication"),
        ]

        for icon, text in highlights:
            st.markdown(
                f"""
                <div style='display:flex;gap:10px;margin-bottom:10px;'>
                    <span>{icon}</span>
                    <span>{text}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ---------------- RIGHT ---------------- #
    with col_right:

        st.markdown("""
        <div style='background:#1a1a2e;
                    padding:25px;
                    border-radius:12px;
                    border:1px solid #333;'>
        """, unsafe_allow_html=True)

        login_tab, signup_tab = st.tabs(["🔑 Log In", "✍️ Sign Up"])

        # ---------------- LOGIN ---------------- #
        with login_tab:

            st.subheader("Sign in to LexAI")

            show_google_login(key="google_login")

            st.markdown(
                "<center>— OR —</center>",
                unsafe_allow_html=True,
            )

            login_method = st.radio(
                "Choose method:",
                ["Email Magic Link", "Phone OTP"],
                horizontal=True,
                key="login_method",
                label_visibility="collapsed",
            )

            if login_method == "Email Magic Link":
                show_email_login("login")
            else:
                show_phone_login("login")

        # ---------------- SIGNUP ---------------- #
        with signup_tab:

            st.subheader("Create your LexAI account")

            st.info("Sign up using Email or Phone. No password required!")

            signup_method = st.radio(
                "Choose method:",
                ["Email Magic Link", "Phone OTP"],
                horizontal=True,
                key="signup_method",
                label_visibility="collapsed",
            )

            if signup_method == "Email Magic Link":
                show_email_login("signup")
            else:
                show_phone_login("signup")

        st.markdown("</div>", unsafe_allow_html=True)

        if st.button(
            "← Back to Home",
            use_container_width=True,
            key="back_home",
        ):
            go_landing()
            st.rerun()