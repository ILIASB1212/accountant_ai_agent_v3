import os
import tempfile
from pathlib import Path

import streamlit as st
import fitz
import torch

from transformers import LightOnOcrForConditionalGeneration, LightOnOcrProcessor


from transformers import (
    AutoProcessor,
    GlmOcrForConditionalGeneration
)


# ============================================================
# RECSIZE LAYER 
# ============================================================


from PIL import Image
import tempfile
from pathlib import Path


import io
import tempfile
from PIL import Image

def resize_image_for_ocr(image_path: str, target_kb: int = 250,
                         min_quality: int = 30,
                         min_scale: float = 0.15) -> str:
    image = Image.open(image_path).convert("RGB")
    target_bytes = target_kb * 1024

    scale = 1.0
    quality = 85
    best_bytes = None

    while True:
        w = max(1, int(image.width * scale))
        h = max(1, int(image.height * scale))

        buf = io.BytesIO()
        image.resize((w, h), Image.Resampling.LANCZOS).save(
            buf, "JPEG", quality=quality, optimize=True
        )
        best_bytes = buf.getvalue()

        if (len(best_bytes) <= target_bytes
                or quality <= min_quality
                or scale <= min_scale):
            break

        if quality > 60:
            quality -= 10
        else:
            scale *= 0.85

    out = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    out.write(best_bytes)
    out.close()
    return out.name


# ============================================================
# MODEL
# ============================================================
@st.cache_resource
def load_ocr_model():
    model_id = "lightonai/LightOnOCR-2-1B"
    model = LightOnOcrForConditionalGeneration.from_pretrained(
        model_id,
        torch_dtype=torch.bfloat16,
        device_map="auto",                        # Offloads what fits onto GPU
        max_memory={0: "3GiB", "cpu": "10GiB"},   # Reserve some GPU headroom
    )
    processor = LightOnOcrProcessor.from_pretrained(model_id)

    return processor, model


# ============================================================
# IMAGE OCR
# ============================================================

def ocr_image(image_path: str):

    if not os.path.isfile(image_path):
        raise FileNotFoundError(
            f"Image file not found: {image_path}"
        )

    

    try:
        processor, model = load_ocr_model()

        image = Image.open(image_path).convert("RGB")
        image.thumbnail((768, 768))  # Keep image small for your 4GB VRAM
        conversation = [{"role": "user", "content": [{"type": "image", "image": image}]}]
        inputs = processor.apply_chat_template(
               conversation,
               add_generation_prompt=True,
               tokenize=True,
               return_dict=True,
               return_tensors="pt",
           )
       
           # Move inputs to the same device as the model's first layer
        inputs = {k: v.to(model.device) for k, v in inputs.items()}
        with torch.inference_mode():
            output_ids = model.generate(**inputs, max_new_tokens=256, do_sample=False)
       
        generated_ids = output_ids[0, inputs["input_ids"].shape[1]:]
        output_text = processor.decode(generated_ids, skip_special_tokens=True)
        return output_text
    except Exception as e:

        raise RuntimeError(
            f"Error during image OCR processing: {e}"
        ) from e


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

    suffix = Path(file_path).suffix.lower()

    if suffix in (".png", ".jpg", ".jpeg"):

        resized_path = resize_image_for_ocr(file_path)

        try:
            return ocr_image(resized_path)
        finally:
            Path(resized_path).unlink(missing_ok=True)

    if suffix == ".pdf":
        return ocr_pdf(file_path)

    raise ValueError(
        f"Unsupported file type: {suffix or 'unknown'}"
    )