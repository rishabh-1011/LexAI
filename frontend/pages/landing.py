"""
frontend/pages/landing.py
Landing page for LexAI.
"""

import streamlit as st
from frontend.utils.session import go_auth


def show_landing():
    """Render the LexAI landing page."""

    # Hero section
    st.markdown("""
        <div style='text-align:center; padding:3rem 0 2rem;'>
            <h1 style='font-size:3rem; margin-bottom:0.5rem;'>⚖️ LexAI</h1>
            <h3 style='color:#00d4ff; margin-bottom:1rem;'>
                AI-Powered Legal Document Analyzer
            </h3>
            <p style='color:#aaa; font-size:1.1rem; max-width:600px; margin:0 auto;'>
                Upload any legal document and instantly get structured analysis,
                risk assessment, and plain-language explanations — powered by
                RAG and GPT-4o-mini.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Stats row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
            <div style='text-align:center; background:#1a1a2e;
                        padding:1rem; border-radius:10px;
                        border:1px solid #00d4ff;'>
                <h2 style='color:#00d4ff; margin:0;'>🧠</h2>
                <p style='margin:0; font-weight:600;'>RAG Powered</p>
                <p style='margin:0; color:#aaa; font-size:0.8rem;'>
                    28 Legal KB Files
                </p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div style='text-align:center; background:#1a1a2e;
                        padding:1rem; border-radius:10px;
                        border:1px solid #00c851;'>
                <h2 style='color:#00c851; margin:0;'>🌐</h2>
                <p style='margin:0; font-weight:600;'>4 Languages</p>
                <p style='margin:0; color:#aaa; font-size:0.8rem;'>
                    EN, HI, TE, OR
                </p>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div style='text-align:center; background:#1a1a2e;
                        padding:1rem; border-radius:10px;
                        border:1px solid #ffd700;'>
                <h2 style='color:#ffd700; margin:0;'>📄</h2>
                <p style='margin:0; font-weight:600;'>5+ File Types</p>
                <p style='margin:0; color:#aaa; font-size:0.8rem;'>
                    PDF, DOCX, TXT, PNG, JPG
                </p>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
            <div style='text-align:center; background:#1a1a2e;
                        padding:1rem; border-radius:10px;
                        border:1px solid #ff6b6b;'>
                <h2 style='color:#ff6b6b; margin:0;'>💡</h2>
                <p style='margin:0; font-weight:600;'>4 Insights</p>
                <p style='margin:0; color:#aaa; font-size:0.8rem;'>
                    Summary, Clauses, Risks, Advice
                </p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Feature cards
    st.markdown("### ✨ Key Features")
    f1, f2, f3, f4 = st.columns(4)

    features = [
        ("📋", "Smart Summary",
         "Get a clear, concise overview of any legal document in seconds."),
        ("🔑", "Key Clause Extraction",
         "Identify the most important clauses and understand what they mean."),
        ("⚠️", "Risk Detection",
         "Spot potential risks, red flags, and unfair terms automatically."),
        ("💬", "Document Q&A",
         "Ask questions about your document and get instant grounded answers."),
    ]

    for col, (icon, title, desc) in zip([f1, f2, f3, f4], features):
        with col:
            st.markdown(f"""
                <div style='background:#1a1a2e; padding:1.25rem;
                            border-radius:10px; border:1px solid #333;
                            height:160px;'>
                    <div style='font-size:2rem;'>{icon}</div>
                    <p style='font-weight:600; margin:0.5rem 0 0.25rem;'>
                        {title}
                    </p>
                    <p style='color:#aaa; font-size:0.82rem; margin:0;'>
                        {desc}
                    </p>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # CTA buttons
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        if st.button(
            "🚀 Get Started — Log In",
            use_container_width=True,
            type="primary",
        ):
            go_auth("login")
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button(
            "✍️ Sign Up",
            use_container_width=True,
        ):
            go_auth("signup")
            st.rerun()