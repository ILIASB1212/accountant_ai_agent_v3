import os
import tempfile
from pathlib import Path

import streamlit as st
import os
import base64
import mimetypes
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


# ============================================================
# IMAGE OCR
# ============================================================



load_dotenv()


def encode_image(image_path: str) -> tuple[str, str]:
    """Return a Base64 string and its MIME type."""
    path = Path(image_path)

    if not path.is_file():
        raise FileNotFoundError(f"Image not found: {path}")

    mime_type, _ = mimetypes.guess_type(path.name)

    supported_types = {
        "image/jpeg",
        "image/png",
        "image/webp",
        "image/gif",
    }

    if mime_type not in supported_types:
        raise ValueError(f"Unsupported image type: {mime_type}")

    image_base64 = base64.b64encode(
        path.read_bytes()
    ).decode("utf-8")

    return image_base64, mime_type


def read_image(
    image_path: str,
    
) -> str:
    """Analyze an image using OpenAI or Groq vision."""
    prompt = (
            "Read this invoice. Extract the supplier, invoice number, "
            "date, currency, subtotal, tax, and total. "
            "Mark any unreadable field as uncertain; do not guess. or extract eny other or usefull information you can "
            "find in the invoice."
        )
    try:
        model = "qwen/qwen3.8-27b"
        api_key = os.getenv("GROQ_API_KEY")
        base_url = "https://api.groq.com/openai/v1"
        if not model:
            raise ValueError(
                "Pass a currently supported Groq vision model."
            )

    except ValueError as e:
        raise ValueError("Provider must be 'openai' or 'groq'.")


    image_base64, mime_type = encode_image(image_path)

    client = OpenAI(
        api_key=api_key,
        **({"base_url": base_url} if base_url else {}),
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": (
                                f"data:{mime_type};base64,"
                                f"{image_base64}"
                            )
                        },
                    },
                ],
            }
        ],
    )

    return response.choices[0].message.content or ""



# ============================================================
# PDF OCR
# ============================================================

import os
import fitz  # PyMuPDF


def ocr_pdf(pdf_path: str) -> str | None:
    """
    Extract text from a PDF using PyMuPDF's native text layer.
    No OCR / image rendering involved.
    """
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    page_results = []

    try:
        with fitz.open(pdf_path) as document:

            if document.page_count == 0:
                return None

            for page_number, page in enumerate(document, start=1):
                # "text" = plain reading-order text.
                # Alternatives: "blocks", "words", "dict", "rawdict", "html", "xml"
                page_text = page.get_text("text").strip()

                if page_text:
                    page_results.append(
                        f"--- Page {page_number} ---\n{page_text}"
                    )

        if not page_results:
            return None

        return "\n\n".join(page_results)

    except Exception as e:
        raise RuntimeError(
            f"Error during PDF text extraction: {e}"
        ) from e


# ============================================================
# GENERAL OCR FUNCTION
# ============================================================

def ocr_document(file_path: str):
    try:
        suffix = Path(file_path).suffix.lower()

        if suffix in (".png", ".jpg", ".jpeg"):

            return  read_image(image_path=file_path)

        elif suffix == ".pdf":
            return ocr_pdf(file_path)
    
    except Exception as e:
        raise ValueError(
            f"Unsupported file type: {suffix or 'unknown'}"
        )