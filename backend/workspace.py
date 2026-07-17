"""
backend/workspace.py

Main workspace logic for LexAI.
Handles document input, pipeline execution, and Q&A chat.
"""

import streamlit as st
from backend.extractor import extract_text
from backend.llm_engine import (
    analyze_legal_text,
    answer_document_question,
    generate_qa_suggestions,
)
from backend.audio import generate_audio


def run_workspace():
    """Main workspace page logic."""

    st.markdown("## 📄 LexAI Workspace")
    st.markdown("Upload a legal document or paste text below to analyze it.")

    # --------------------------------------------------
    # DOCUMENT INPUT
    # --------------------------------------------------
    input_method = st.radio(
        "Choose input method:",
        ["📁 Upload File", "📝 Paste Text"],
        horizontal=True,
    )

    document_text = ""

    if input_method == "📁 Upload File":
        uploaded_file = st.file_uploader(
            "Upload your legal document",
            type=["pdf", "docx", "txt", "png", "jpg", "jpeg"],
        )
        if uploaded_file:
            with st.spinner("Extracting text from document..."):
                document_text = extract_text(uploaded_file)
            if document_text:
                st.success("✅ Text extracted successfully!")
                with st.expander("Preview extracted text"):
                    st.text(document_text[:1000] + "..." if len(document_text) > 1000 else document_text)

    else:
        document_text = st.text_area(
            "Paste your legal document text here:",
            height=200,
            placeholder="Paste contract, agreement, or any legal text here...",
        )

    # --------------------------------------------------
    # LANGUAGE SELECTION
    # --------------------------------------------------
    from backend.config import SUPPORTED_LANGUAGES
    language = st.selectbox("Select output language:", list(SUPPORTED_LANGUAGES.keys()))

    # --------------------------------------------------
    # ANALYZE BUTTON
    # --------------------------------------------------
    if st.button("🔍 Analyze Document", type="primary", disabled=not document_text):
        with st.spinner("Analyzing document through 5-stage pipeline..."):

            progress = st.progress(0)

            progress.progress(20, "Stage 1: Extracting text...")
            progress.progress(40, "Stage 2: Retrieving legal knowledge...")
            progress.progress(60, "Stage 3: Building prompt...")
            progress.progress(80, "Stage 4: Generating analysis...")

            result = analyze_legal_text(document_text, language)

            progress.progress(100, "Stage 5: Finalizing...")
            progress.empty()

        # Store in session state
        st.session_state["analysis_result"] = result
        st.session_state["document_text"]   = document_text
        st.session_state["chat_history"]    = []
        st.session_state["suggestions"]     = generate_qa_suggestions(document_text, result)

    # --------------------------------------------------
    # DISPLAY RESULTS
    # --------------------------------------------------
    if "analysis_result" in st.session_state:
        result = st.session_state["analysis_result"]

        st.markdown("---")
        st.markdown("## 📊 Analysis Result")
        st.markdown(result)

        # Voice output
        if st.button("🔊 Listen to Analysis"):
            with st.spinner("Generating audio..."):
                audio_path = generate_audio(result, language)
            if audio_path:
                st.audio(audio_path, format="audio/mp3")

        # --------------------------------------------------
        # Q&A CHAT
        # --------------------------------------------------
        st.markdown("---")
        st.markdown("## 💬 Ask Questions About Your Document")

        # Show suggestions
        if "suggestions" in st.session_state:
            st.markdown("**Suggested questions:**")
            cols = st.columns(len(st.session_state["suggestions"]))
            for i, suggestion in enumerate(st.session_state["suggestions"]):
                if cols[i].button(suggestion, key=f"sug_{i}"):
                    st.session_state["current_question"] = suggestion

        # Chat input
        question = st.chat_input("Ask anything about your document...")
        if "current_question" in st.session_state:
            question = st.session_state.pop("current_question")

        if question:
            with st.spinner("Finding answer..."):
                answer = answer_document_question(
                    question=question,
                    document_text=st.session_state["document_text"],
                    language=language,
                    chat_history=st.session_state.get("chat_history", []),
                )

            st.session_state["chat_history"].append({
                "user": question,
                "assistant": answer,
            })

        # Display chat history
        for turn in st.session_state.get("chat_history", []):
            with st.chat_message("user"):
                st.write(turn["user"])
            with st.chat_message("assistant"):
                st.write(turn["assistant"])