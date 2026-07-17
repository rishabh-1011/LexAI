"""
frontend/components/sidebar.py
Sidebar component for LexAI workspace.
"""

import streamlit as st
from frontend.utils.session import logout


def render_sidebar():
    """Render the workspace sidebar with user info and controls."""
    with st.sidebar:

        # Logo and branding
        st.markdown("""
            <div style='text-align: center; padding: 1rem 0;'>
                <h2>⚖️ LexAI</h2>
                <p style='color: #aaa; font-size: 0.8rem;'>
                    AI-Powered Legal Assistant
                </p>
            </div>
        """, unsafe_allow_html=True)

        st.divider()

        # User info
        user = st.session_state.get("user", {})
        if user:
            st.markdown(f"""
                <div style='
                    background: #1a1a2e;
                    padding: 0.75rem;
                    border-radius: 8px;
                    margin-bottom: 1rem;
                '>
                    <p style='margin: 0; font-weight: 600;'>
                        👤 {user.get('name', 'User')}
                    </p>
                    <p style='margin: 0; color: #aaa; font-size: 0.8rem;'>
                        {user.get('email', user.get('phone', ''))}
                    </p>
                    <p style='margin: 0; color: #00c851; font-size: 0.75rem;'>
                        🟢 AI Online
                    </p>
                </div>
            """, unsafe_allow_html=True)

        st.divider()

        # Stats
        st.markdown("### 📊 Session Stats")

        qa_count = len(st.session_state.get("qa_history", []))
        has_doc  = st.session_state.get("analyzed_text") is not None

        st.metric("Documents Analyzed", "1" if has_doc else "0")
        st.metric("Questions Asked", qa_count)

        st.divider()

        # Clear analysis button
        if st.session_state.get("analysis_result"):
            if st.button("🗑️ Clear Analysis", use_container_width=True):
                st.session_state["analyzed_text"]   = None
                st.session_state["analysis_result"] = None
                st.session_state["source_label"]    = None
                st.session_state["qa_history"]      = []
                st.session_state["qa_suggestions"]  = []
                st.rerun()

        st.divider()

        # Sign out
        if st.button("🚪 Sign Out", use_container_width=True):
            logout()
            st.rerun()