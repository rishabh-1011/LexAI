"""
backend/extractor.py
Document text extraction for LexAI.
Supports PDF, DOCX, TXT, and images.
"""

import os
import pytesseract
from PIL import Image
from docx import Document

try:
    from pdf2image import convert_from_bytes
    PDF2IMAGE_AVAILABLE = True
except ImportError:
    PDF2IMAGE_AVAILABLE = False

try:
    pytesseract.get_tesseract_version()
    TESSERACT_AVAILABLE = True
except Exception:
    TESSERACT_AVAILABLE = False

try:
    from pypdf import PdfReader
except ImportError:
    from PyPDF2 import PdfReader

# --------------------------------------------------
# IMAGE EXTRACTION
# --------------------------------------------------
def extract_text_from_image(uploaded_file) -> str:
    """Extract text from image using Tesseract OCR."""
    try:
        img = Image.open(uploaded_file)
        return pytesseract.image_to_string(img).strip()
    except Exception as e:
        return f"Could not extract text from image: {e}"

# --------------------------------------------------
# TXT EXTRACTION
# --------------------------------------------------
def extract_text_from_txt(uploaded_file) -> str:
    """Extract text from plain text file."""
    try:
        return uploaded_file.read().decode("utf-8", errors="ignore").strip()
    except Exception as e:
        return f"Could not read text file: {e}"

# --------------------------------------------------
# DOCX EXTRACTION
# --------------------------------------------------
def extract_text_from_docx(uploaded_file) -> str:
    """Extract text from Word document."""
    try:
        doc = Document(uploaded_file)
        return "\n".join([para.text for para in doc.paragraphs]).strip()
    except Exception as e:
        return f"Could not extract text from DOCX: {e}"

# --------------------------------------------------
# PDF EXTRACTION (digital text + OCR fallback)
# --------------------------------------------------
def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extract text from a PDF file.
    - First tries PyPDF2 for digital PDFs (fast).
    - If little/no text is found, falls back to Tesseract OCR
      via pdf2image (handles scanned/image-based PDFs).
    """
    try:
        from io import BytesIO
        file_bytes = uploaded_file.read()

        # Step 1: Try digital text extraction
        pdf_reader = PdfReader(BytesIO(file_bytes))
        text = ""
        for page in pdf_reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

        text = text.strip()

        # If meaningful text found, return it
        if len(text) > 100:
            return text

        # Step 2: OCR fallback for scanned PDFs
        if PDF2IMAGE_AVAILABLE and TESSERACT_AVAILABLE:
            return _ocr_pdf_bytes(file_bytes)
        elif not PDF2IMAGE_AVAILABLE:
            return (
                "⚠️ This appears to be a scanned PDF. "
                "pdf2image is not installed.\n\n"
                "Tip: Copy the text from the PDF and paste it directly into the text box."
            )
        else:
            return (
                "⚠️ This appears to be a scanned PDF. "
                "Tesseract OCR is not available.\n\n"
                "Tip: Copy the text from the PDF and paste it directly into the text box."
            )

    except Exception as e:
        return f"Could not extract text from PDF: {e}"

def _ocr_pdf_bytes(file_bytes: bytes) -> str:
    """Convert PDF pages to images and run Tesseract OCR on each page."""
    try:
        images = convert_from_bytes(file_bytes, dpi=200)
        text = ""
        for img in images:
            text += pytesseract.image_to_string(img) + "\n"
        return text.strip()
    except Exception as e:
        return f"OCR failed: {e}"

# --------------------------------------------------
# MAIN ROUTER
# --------------------------------------------------
def extract_text(uploaded_file) -> str:
    """Route file to correct extractor based on extension."""
    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    elif filename.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)
    elif filename.endswith(".txt"):
        return extract_text_from_txt(uploaded_file)
    elif filename.endswith((".png", ".jpg", ".jpeg")):
        return extract_text_from_image(uploaded_file)
    else:
        return "❌ Unsupported file format. Please upload PDF, DOCX, TXT, or image files."