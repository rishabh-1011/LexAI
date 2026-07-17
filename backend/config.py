import os
from dotenv import load_dotenv

load_dotenv()

def _get_secret(key: str, default: str = "") -> str:
    """Read from Streamlit secrets first, then env vars."""
    try:
        import streamlit as st
        return st.secrets[key]
    except Exception:
        return os.getenv(key, default)

# OpenAI
GROQ_API_KEY = _get_secret("GROQ_API_KEY")

# Google OAuth
GOOGLE_CLIENT_ID     = _get_secret("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = _get_secret("GOOGLE_CLIENT_SECRET")
REDIRECT_URI         = _get_secret("REDIRECT_URI", "http://localhost:8501/")

# Firebase
FIREBASE_API_KEY     = _get_secret("FIREBASE_API_KEY")
FIREBASE_AUTH_DOMAIN = _get_secret("FIREBASE_AUTH_DOMAIN")
FIREBASE_PROJECT_ID  = _get_secret("FIREBASE_PROJECT_ID")

FIREBASE_CONFIG = {
    "apiKey":    FIREBASE_API_KEY,
    "authDomain": FIREBASE_AUTH_DOMAIN,
    "projectId": FIREBASE_PROJECT_ID,
}

# Twilio
TWILIO_ACCOUNT_SID = _get_secret("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN  = _get_secret("TWILIO_AUTH_TOKEN")
TWILIO_VERIFY_SID  = _get_secret("TWILIO_VERIFY_SID")

# Supported languages
SUPPORTED_LANGUAGES = {
    "English": "en",
    "Hindi":   "hi",
    "Telugu":  "te",
    "Odia":    "or"
}

# LiteLLM model
DEFAULT_MODEL = "groq/llama-3.3-70b-versatile"