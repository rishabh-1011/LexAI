"""
frontend/utils/session.py
Session state management for LexAI.
"""

import streamlit as st


def init_session():
    """Initialize all session state defaults."""
    defaults = {
        "logged_in":      False,
        "user":           None,
        "analyzed_text":  None,
        "analysis_result": None,
        "source_label":   None,
        "qa_history":     [],
        "qa_suggestions": [],
        "qa_prefill":     "",
        "language":       "English",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def go_auth(mode: str = "login"):
    """Navigate to auth page."""
    st.session_state["auth_mode"] = mode
    st.session_state["page"] = "auth"


def go_landing():
    """Navigate to landing page."""
    st.session_state["page"] = "landing"


def go_workspace():
    """Navigate to workspace."""
    st.session_state["page"] = "workspace"


def logout():
    """Clear session and go to landing."""
    st.session_state.clear()
    st.session_state["page"] = "landing"