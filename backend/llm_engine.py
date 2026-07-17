from litellm import completion

from litellm import completion
from backend.config import GROQ_API_KEY, DEFAULT_MODEL

from backend.rag import retrieve_relevant_knowledge, retrieve_for_qa

MAX_TEXT_CHARS    = 12000
MAX_CONTEXT_CHARS = 3000


def analyze_legal_text(text: str, language: str = "English") -> str:
    original_length = len(text)
    if len(text) > MAX_TEXT_CHARS:
        text = (
            text[:MAX_TEXT_CHARS]
            + "\n\n[... Document truncated for analysis. "
            "Showing first section only due to length limits ...]"
        )

    try:
        retrieved_context = retrieve_relevant_knowledge(text)
        if len(retrieved_context) > MAX_CONTEXT_CHARS:
            retrieved_context = retrieved_context[:MAX_CONTEXT_CHARS] + "..."
    except Exception:
        retrieved_context = "No additional legal context retrieved."

    truncation_notice = ""
    if original_length > MAX_TEXT_CHARS:
        truncation_notice = (
            f"\n\n⚠️ NOTE: The original document was {original_length:,} characters long. "
            f"Only the first {MAX_TEXT_CHARS:,} characters were analysed.\n"
        )

    prompt = f"""You are an expert AI Legal Assistant specialized in legal document analysis.

Your task is to analyze the provided text as a legal document.
{truncation_notice}
==============================================
INSTRUCTIONS
==============================================

Be INCLUSIVE — analyze anything that contains legal terminology or obligations.
Only decline if the text is clearly a recipe, poem, news article, or casual chat.
When in doubt — ANALYZE IT as legal content.

Generate your response entirely in {language} language.

==============================================
OUTPUT FORMAT
==============================================

## 📋 1. SUMMARY
- Clear summary of the document
- Purpose of the agreement/document
- Parties involved and overall objective

## 🔑 2. KEY CLAUSES & THEIR MEANING
For each important clause:
- **Clause name**: Explanation in simple language
- Why it matters

## ⚠️ 3. RISKS
- Legal, financial, operational, or compliance risks
- Consequences if applicable

## 💡 4. ADVICE
- Practical recommendations
- What to review carefully
- Clauses that may need negotiation or legal consultation

==============================================
RULES
==============================================
- Do NOT generate false legal information
- Keep explanations beginner-friendly

==============================================
LEGAL KNOWLEDGE CONTEXT
==============================================
{retrieved_context}

==============================================
DOCUMENT TO ANALYZE
==============================================
{text}"""

    try:
        response = completion(
            model=DEFAULT_MODEL,
            api_key=GROQ_API_KEY,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional legal analyst. "
                        "Always analyze text as legal content unless obviously non-legal. "
                        "When in doubt, treat it as legal and analyze it."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            max_tokens=2000,
        )
        return response["choices"][0]["message"]["content"]

    except Exception as e:
        error_msg = str(e)
        if "ContextWindowExceeded" in error_msg or "context_length_exceeded" in error_msg:
            try:
                shorter_text = text[:MAX_TEXT_CHARS // 2] + "\n\n[... Further truncated ...]"
                short_prompt = prompt.replace(text, shorter_text)
                response = completion(
                    model=DEFAULT_MODEL,
                    api_key=OPENAI_API_KEY,
                    messages=[{"role": "user", "content": short_prompt}],
                    max_tokens=2000,
                )
                return (
                    "⚠️ Document was very large — analysis based on first portion only.\n\n"
                    + response["choices"][0]["message"]["content"]
                )
            except Exception as retry_error:
                return f"❌ Document too large to analyse. Error: {retry_error}"
        return f"❌ Analysis failed: {error_msg}"


def answer_document_question(
    question: str,
    document_text: str,
    language: str = "English",
    chat_history: list = None,
) -> str:
    chat_history = chat_history or []

    doc_context, kb_context = retrieve_for_qa(question, document_text)

    system_prompt = """You are LexAI — an expert AI Legal Assistant answering questions about a legal document.
Answer questions related to the document, its clauses, parties, terms, risks, and legal topics.
Keep answers clear, accurate, and beginner-friendly.
Never make up legal facts."""

    doc_section = f"""
==============================================
DOCUMENT CONTENT (relevant sections)
==============================================
{doc_context if doc_context else "No specific section found."}
""" if doc_context else ""

    kb_section = f"""
==============================================
LEGAL KNOWLEDGE CONTEXT
==============================================
{kb_context}
""" if kb_context and "No closely" not in kb_context else ""

    user_prompt = f"""
{doc_section}
{kb_section}
==============================================
USER QUESTION
==============================================
{question}

Answer based on the document and legal knowledge above.
Be specific, clear, and beginner-friendly."""

    messages = [{"role": "system", "content": system_prompt}]

    # Fix: use correct keys "question" and "answer"
    for turn in chat_history[-6:]:
        messages.append({"role": "user",      "content": turn.get("question", turn.get("user", ""))})
        messages.append({"role": "assistant", "content": turn.get("answer",   turn.get("assistant", ""))})

    messages.append({"role": "user", "content": user_prompt})

    try:
        response = completion(
            model=DEFAULT_MODEL,
            api_key=GROQ_API_KEY,
            messages=messages,
            max_tokens=800,
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Could not answer question: {e}"


def generate_qa_suggestions(document_text: str, analysis_result: str) -> list:
    doc_preview      = document_text[:3000]  if document_text  else ""
    analysis_preview = analysis_result[:1000] if analysis_result else ""

    prompt = f"""Based on this legal document and its analysis, generate exactly 5 short specific questions a user would want to ask.

DOCUMENT PREVIEW:
{doc_preview}

ANALYSIS PREVIEW:
{analysis_preview}

RULES:
- Questions must be specific to THIS document
- Each question must be under 12 words
- Return ONLY the 5 questions, one per line, no numbering, no bullets"""

    try:
        response = completion(
            model=DEFAULT_MODEL,
            api_key=GROQ_API_KEY,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
        )
        raw = response["choices"][0]["message"]["content"]
        questions = [q.strip() for q in raw.strip().split("\n") if q.strip()]
        return questions[:5] if questions else _default_suggestions()
    except Exception:
        return _default_suggestions()


def _default_suggestions() -> list:
    return [
        "What are the key obligations in this document?",
        "Are there any penalty clauses?",
        "What are my termination rights?",
        "When does this agreement expire?",
        "What are the payment terms?",
    ]