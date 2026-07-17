# LexAI — AI Powered Legal Document Analyzer

LexAI is an AI-powered legal document analysis web application built with Streamlit. It takes any legal document — contract, NDA, rental agreement, employment letter, or legal notice — and breaks it down into clear, structured insights that anyone can understand.

## Features

- Smart Summary — Clear overview of any legal document in seconds
- Key Clause Extraction — Important clauses explained in simple language
- Risk Detection — Flags potential risks, unfair terms, and red flags
- Legal Advice — Practical recommendations for the user
- Voice Output — Audio reading of analysis via gTTS
- Document Q&A — Ask questions about your document and get grounded answers
- 4 Languages — English, Hindi, Telugu, Odia
- Secure Authentication — Firebase, Twilio OTP, Google OAuth

## Architecture

5-Stage RAG Pipeline:
1. Extract — Supports PDF, DOCX, TXT, PNG, JPG with OCR fallback
2. Retrieve — TF-IDF + cosine similarity over 28 Indian legal knowledge base files
3. Augment — Retrieved legal context injected into the prompt
4. Generate — LLM analysis via LiteLLM + Groq (LLaMA 3.3)
5. Finalise — Result card, voice output, Q&A chat, suggestions

## Tech Stack

- Frontend: Streamlit
- AI/LLM: LiteLLM + Groq LLaMA 3.3 70B
- RAG: TF-IDF + Cosine Similarity (scikit-learn)
- Authentication: Firebase + Twilio Verify + streamlit-oauth
- OCR: Tesseract + pdf2image + Pillow
- Voice: gTTS

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Environment Variables

Create a .env file in the project root:
GROQ_API_KEY=your_groq_key
FIREBASE_API_KEY=your_firebase_key
FIREBASE_AUTH_DOMAIN=your_auth_domain
FIREBASE_PROJECT_ID=your_project_id
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
REDIRECT_URI=http://localhost:8501/
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_VERIFY_SID=your_verify_sid

## System Dependencies
tesseract-ocr
poppler-utils