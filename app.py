import streamlit as st

st.set_page_config(
    page_title="LexAI — Legal Document Analyzer",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Load custom CSS
with open("frontend/styles/main.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

from frontend.utils.session  import init_session
from frontend.pages.landing  import show_landing
from frontend.pages.auth     import show_auth
from frontend.pages.workspace import show_workspace


def main():
    """Initialize session and route to correct page."""

    init_session()

    # Route to workspace if logged in
    if st.session_state.get("logged_in"):
        st.session_state["page"] = "workspace"

    # Check if user just logged in
    if st.session_state.get("user") and not st.session_state.get("logged_in"):
        st.session_state["logged_in"] = True
        st.session_state["page"] = "workspace"

    page = st.session_state.get("page", "landing")

    if page == "landing":
        show_landing()
    elif page == "auth":
        show_auth()
    elif page == "workspace":
        show_workspace()
    else:
        show_landing()


if __name__ == "__main__":
    main()