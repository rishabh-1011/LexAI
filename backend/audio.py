"""
backend/audio.py
Audio generation for LexAI.
Converts analysis text to speech using gTTS.
"""

import os
import re
from gtts import gTTS
from backend.config import SUPPORTED_LANGUAGES

AUDIO_FOLDER = "temp_audio"
os.makedirs(AUDIO_FOLDER, exist_ok=True)


def clean_text_for_speech(text: str) -> str:
    """Remove markdown symbols so audio sounds natural."""
    text = re.sub(r"#{1,6}\s*", "", text)
    text = re.sub(r"\*{1,2}(.*?)\*{1,2}", r"\1", text)
    text = re.sub(r"[-•]\s+", ". ", text)
    text = re.sub(r"\n{2,}", ". ", text)
    text = re.sub(r"\n", " ", text)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()


def generate_audio(text: str, language: str = "English") -> str:
    """Convert text to speech and save as MP3. Returns file path."""
    try:
        lang_code  = SUPPORTED_LANGUAGES.get(language, "en")
        clean_text = clean_text_for_speech(text)

        if not clean_text:
            return ""

        clean_text  = clean_text[:3000]
        output_path = os.path.join(AUDIO_FOLDER, "analysis_audio.mp3")

        tts = gTTS(text=clean_text, lang=lang_code, slow=False)
        tts.save(output_path)
        return output_path

    except Exception as e:
        print(f"Audio generation failed: {e}")
        return ""


# Alias for workspace import
text_to_speech = generate_audio