"""
Reads a single FOMC PDF, extracts its meeting date from the filename,
tokenizes and cleans the text, and returns (date, cleaned_text).
"""
import nltk
nltk.data.path.append(r"C:\Users\hargu\nltk_data")
import re
import os
from PyPDF2 import PdfReader
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from backend.config import DATE_PATTERN, COMMON_FIXES

STOP_WORDS = set(stopwords.words("english"))

def process_pdf(pdf_file):
    """
    pdf_file: full path to one PDF.
    Returns: (date_string, cleaned_text_string)
    This is your existing logic, unchanged — do not change the cleaning rules.
    """
    filename = os.path.basename(pdf_file)
    date_match = re.search(DATE_PATTERN, filename)
    date = date_match.group(0) if date_match else None

    reader = PdfReader(pdf_file)
    raw_text = ""
    for page in reader.pages:
        raw_text += page.extract_text() or ""

    tokens = word_tokenize(raw_text.lower())

    # Remove stopwords and punctuation-only tokens
    cleaned_tokens = [t for t in tokens if t.isalpha() and t not in STOP_WORDS]

    # Fix common OCR truncation errors, e.g. 'devel' -> 'development'
    cleaned_tokens = [COMMON_FIXES.get(t, t) for t in cleaned_tokens]

    cleaned_text = " ".join(cleaned_tokens)
    return date, cleaned_text

# Reminder for myself: Add ThreadPoolExecutor to process multiple PDFs in parallel when calling this function from the main script.