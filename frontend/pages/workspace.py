"""
frontend/pages/workspace.py

Main workspace page — document input, analysis,
pipeline visibility, voice output, and document Q&A.
"""

import streamlit as st

from frontend.utils.session      import go_auth, go_landing, logout
from frontend.components.ticker  import render_ticker
from frontend.components.pipeline import render_pipeline, STAGE_KEYS
from frontend.components.sidebar  import render_sidebar

try:
    from backend.llm_engine import (
        analyze_legal_text,
        answer_document_question,
        generate_qa_suggestions,
    )
    from backend.audio     import generate_audio
    from backend.extractor import (
        extract_text_from_pdf,
        extract_text_from_docx,
        extract_text_from_image,
    )
    BACKEND_AVAILABLE = True
    _BACKEND_ERROR    = ""
except Exception as _backend_err:
    BACKEND_AVAILABLE = False
    _BACKEND_ERROR    = str(_backend_err)


def show_workspace():
    """Render the full workspace page."""

    # Guard: redirect to auth if not logged in
    if not st.session_state.logged_in:
        go_auth("login")
        st.rerun()

    # Session state defaults
    if "source_label"    not in st.session_state:
        st.session_state.source_label    = None
    if "analyzed_text"   not in st.session_state:
        st.session_state.analyzed_text   = None
    if "qa_history"      not in st.session_state:
        st.session_state.qa_history      = []
    if "qa_suggestions"  not in st.session_state:
        st.session_state.qa_suggestions  = []
    if "qa_prefill"      not in st.session_state:
        st.session_state.qa_prefill      = ""

    # Sidebar
    render_sidebar()

    # Ticker
    render_ticker()

    # Topbar
    st.markdown("""
        <div style='display:flex; justify-content:space-between;
                    align-items:center; margin-bottom:1rem;'>
            <h2 style='margin:0;'>⚖️ LexAI Workspace</h2>
            <span style='color:#00c851; font-size:0.85rem;'>🟢 AI Online</span>
        </div>
    """, unsafe_allow_html=True)

    if not BACKEND_AVAILABLE:
        st.error(f"⚠️ Backend unavailable: {_BACKEND_ERROR}")
        return

    # --------------------------------------------------
    # DOCUMENT INPUT
    # --------------------------------------------------
    st.markdown("### 📄 Document Input")

    from backend.config import SUPPORTED_LANGUAGES
    language = st.selectbox(
        "Output language:",
        list(SUPPORTED_LANGUAGES.keys()),
        key="language_selector",
    )

    input_tab1, input_tab2 = st.tabs(["📝 Paste Text", "📁 Upload File"])

    raw_text     = ""
    source_label = None

    with input_tab1:
        raw_text = st.text_area(
            "Paste legal document text here:",
            height=200,
            placeholder="Paste contract, NDA, rental agreement, or any legal text...",
            key="paste_input",
        )
        if raw_text.strip():
            source_label = "Pasted Text"

    with input_tab2:
        uploaded = st.file_uploader(
            "Upload document:",
            type=["pdf", "docx", "txt", "png", "jpg", "jpeg"],
            key="file_uploader",
        )
        if uploaded:
            with st.spinner("Extracting text..."):
                ext = uploaded.name.lower()
                if ext.endswith(".pdf"):
                    raw_text = extract_text_from_pdf(uploaded)
                elif ext.endswith(".docx"):
                    raw_text = extract_text_from_docx(uploaded)
                elif ext.endswith(".txt"):
                    raw_text = uploaded.read().decode("utf-8", errors="ignore")
                else:
                    raw_text = extract_text_from_image(uploaded)
            source_label = uploaded.name
            if raw_text:
                st.success(f"✅ Extracted {len(raw_text):,} characters from {uploaded.name}")

    # --------------------------------------------------
    # ANALYZE BUTTON
    # --------------------------------------------------
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_clicked = st.button(
        "🔍 Analyze Document",
        type="primary",
        use_container_width=True,
        disabled=not raw_text.strip(),
    )

    if analyze_clicked and raw_text.strip():
        st.session_state.analyzed_text  = raw_text
        st.session_state.source_label   = source_label
        st.session_state.analysis_result = None
        st.session_state.qa_history     = []
        st.session_state.qa_suggestions = []

       # Pipeline progress
        st.markdown("### ⚙️ Processing Pipeline")

        progress_bar = st.progress(0)
        status_text  = st.empty()

        completed = []
        total     = len(STAGE_KEYS)

        for i, stage in enumerate(STAGE_KEYS):

            progress_bar.progress(i / total)
            status_text.markdown(f"**Processing: {stage.upper()}...**")

            render_pipeline(active_stage=stage, completed=completed)

            if stage == "generate":
                with st.spinner("🤖 Generating analysis..."):
                    result = analyze_legal_text(raw_text, language)
                st.session_state.analysis_result = result

            completed.append(stage)

        progress_bar.progress(1.0)
        status_text.markdown("**✅ Analysis Complete!**")

        render_pipeline(active_stage=None, completed=completed)

        with st.spinner("💡 Generating Q&A suggestions..."):
            st.session_state.qa_suggestions = generate_qa_suggestions(
                raw_text, st.session_state.analysis_result
            )

        st.rerun()

        # Generate suggestions
        with st.spinner("Generating Q&A suggestions..."):
            st.session_state.qa_suggestions = generate_qa_suggestions(
                raw_text, st.session_state.analysis_result
            )

        st.rerun()

    # --------------------------------------------------
    # ANALYSIS RESULT CARD
    # --------------------------------------------------
    if st.session_state.get("analysis_result"):
        st.markdown("---")
        st.markdown(f"""
            <div style='
                background: #1a1a2e;
                border: 1px solid #00d4ff;
                border-radius: 10px;
                padding: 1rem 1.5rem;
                margin-bottom: 1rem;
            '>
                <div style='display:flex; justify-content:space-between;
                            align-items:center; flex-wrap:wrap; gap:0.5rem;'>
                    <span style='font-weight:700; font-size:1rem;'>
                        📋 Paper Viewer
                        {f'— {st.session_state.source_label}'
                         if st.session_state.source_label else ''}
                    </span>
                    <div style='display:flex; gap:0.5rem; flex-wrap:wrap;'>
                        <span style='background:#0d3b66; color:#00d4ff;
                                     padding:2px 10px; border-radius:20px;
                                     font-size:0.75rem;'>
                            🌐 {language}
                        </span>
                        <span style='background:#0d3b66; color:#00c851;
                                     padding:2px 10px; border-radius:20px;
                                     font-size:0.75rem;'>
                            🧠 RAG Augmented
                        </span>
                        <span style='background:#0d3b66; color:#ffd700;
                                     padding:2px 10px; border-radius:20px;
                                     font-size:0.75rem;'>
                            ✅ AI Verified
                        </span>
                        <span style='background:#0d3b66; color:#ff6b6b;
                                     padding:2px 10px; border-radius:20px;
                                     font-size:0.75rem;'>
                            ⚖️ Legal Intelligence
                        </span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(st.session_state.analysis_result)

        # --------------------------------------------------
        # VOICE OUTPUT
        # --------------------------------------------------
        st.markdown("---")
        st.markdown("### 🔊 Voice Output")

        if st.button("🔊 Generate Audio Reading", use_container_width=True):
            with st.spinner("Synthesizing audio with gTTS..."):
                audio_path = generate_audio(
                    st.session_state.analysis_result, language
                )
            if audio_path:
                st.audio(audio_path, format="audio/mp3")
            else:
                st.error("Audio generation failed.")

        # --------------------------------------------------
        # Q&A SUGGESTION BUBBLES
        # --------------------------------------------------
        st.markdown("---")
        st.markdown("### 💬 Document Q&A")

        if st.session_state.qa_suggestions:
            st.markdown("**💡 Suggested questions — click to ask:**")
            cols = st.columns(len(st.session_state.qa_suggestions))
            for i, suggestion in enumerate(st.session_state.qa_suggestions):
                with cols[i]:
                    if st.button(
                        suggestion,
                        key=f"sug_{i}",
                        use_container_width=True,
                    ):
                        st.session_state.qa_prefill = suggestion
                        st.rerun()

        # Q&A Input
        st.markdown("<br>", unsafe_allow_html=True)
        qa_col1, qa_col2 = st.columns([5, 1])

        with qa_col1:
            user_question = st.text_input(
                "Ask a question",
                value=st.session_state.qa_prefill,
                placeholder="e.g. What is the deposit amount? What are my risks?",
                key="qa_input",
                label_visibility="collapsed",
            )

        with qa_col2:
            ask_clicked = st.button(
                "Ask ▶",
                key="qa_ask_btn",
                use_container_width=True,
            )

        # Handle Q&A submission
        if ask_clicked and user_question.strip():
            st.session_state.qa_prefill = ""

            if not BACKEND_AVAILABLE:
                st.error("Backend not available.")
            elif not st.session_state.analyzed_text:
                st.warning("⚠️ No document text available. Please analyze a document first.")
            else:
                with st.spinner("🔍 Searching document and retrieving answer..."):
                    answer = answer_document_question(
                        question=user_question.strip(),
                        document_text=st.session_state.analyzed_text,
                        language=language,
                        chat_history=st.session_state.qa_history,
                    )

                st.session_state.qa_history.append({
                    "question": user_question.strip(),
                    "answer":   answer,
                })
                st.rerun()

        # Clear chat
        if st.session_state.qa_history:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🗑️ Clear Chat", key="qa_clear"):
                st.session_state.qa_history = []
                st.session_state.qa_prefill = ""
                st.rerun()

        # Display chat history
        for turn in st.session_state.qa_history:
            with st.chat_message("user"):
                st.write(turn["question"])
            with st.chat_message("assistant"):
                st.write(turn["answer"])