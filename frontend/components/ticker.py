"""
frontend/components/ticker.py
Scrolling ticker component for LexAI workspace topbar.
"""

import streamlit as st


TICKER_ITEMS = [
    "⚖️ RAG-Powered Legal Analysis",
    "📄 Supports PDF, DOCX, TXT, PNG, JPG",
    "🌐 4 Languages: English, Hindi, Telugu, Odia",
    "🔑 Key Clause Extraction",
    "⚠️ Risk & Red Flag Detection",
    "💡 Plain-Language Legal Advice",
    "🔊 Voice Output via gTTS",
    "💬 Document Q&A Chat",
    "🛡️ Firebase Authentication",
    "☁️ Deployed on Streamlit Cloud",
]


def render_ticker():
    """Render a scrolling ticker with feature highlights."""
    ticker_text = "  &nbsp;&nbsp;&nbsp;•&nbsp;&nbsp;&nbsp;  ".join(TICKER_ITEMS)

    st.markdown(
        f"""
        <style>
        .ticker-wrapper {{
            width: 100%;
            overflow: hidden;
            background: linear-gradient(90deg, #1a1a2e, #16213e);
            padding: 8px 0;
            border-radius: 6px;
            margin-bottom: 1rem;
        }}
        .ticker-content {{
            display: inline-block;
            white-space: nowrap;
            animation: ticker-scroll 40s linear infinite;
            color: #00d4ff;
            font-size: 0.85rem;
            font-weight: 500;
        }}
        @keyframes ticker-scroll {{
            0%   {{ transform: translateX(100vw); }}
            100% {{ transform: translateX(-100%); }}
        }}
        </style>
        <div class="ticker-wrapper">
            <span class="ticker-content">{ticker_text}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )