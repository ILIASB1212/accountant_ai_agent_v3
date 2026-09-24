import os
import tempfile
from pathlib import Path

import streamlit as st
import fitz
import torch

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


def resize_image_for_ocr(image_path: str):
    image = Image.open(image_path)

    new_width = image.width // 2
    new_height = image.height // 2

    resized_path = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".jpg"
    ).name

    image.resize(
        (new_width, new_height),
        Image.Resampling.LANCZOS
    ).convert("RGB").save(
        resized_path,
        "JPEG",
        quality=85
    )

    return resized_path


# ============================================================
# MODEL
# ============================================================

model_id = "zai-org/GLM-OCR"


@st.cache_resource
def load_ocr_model():

    processor = AutoProcessor.from_pretrained(
        model_id
    )

    model = GlmOcrForConditionalGeneration.from_pretrained(
        model_id,
        device_map="auto",
    )

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

        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "url": image_path
                    },
                    {
                        "type": "text",
                        "text": "Text Recognition:"
                    }
                ]
            }
        ]

        inputs = processor.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_dict=True,
            return_tensors="pt",
        ).to(model.device)

        # Some Transformers/model versions can include this field,
        # but GLM-OCR does not need it for generation.
        inputs.pop("token_type_ids", None)

        with torch.inference_mode():
            output = model.generate(
                **inputs,
                max_new_tokens=128
            )

        # Decode only newly generated tokens.
        input_length = inputs["input_ids"].shape[1]

        text = processor.decode(
            output[0][input_length:],
            skip_special_tokens=True
        )

        # Remove unwanted image tokens/instruction text.
        text = text.replace("<|image|>", "")
        text = text.replace("Text Recognition:", "")

        # Clean whitespace.
        text = " ".join(text.split())

        return text.strip()

    except Exception as e:

        raise RuntimeError(
            f"Error during image OCR processing: {e}"
        ) from e


# ============================================================
# PDF OCR
# ============================================================

def ocr_pdf(pdf_path: str):

    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(
            f"PDF file not found: {pdf_path}"
        )

    page_results = []

    try:

        document = fitz.open(pdf_path)

        if document.page_count == 0:
            document.close()
            return None

        # Render PDF pages to PNG and run the same local
        # GLM-OCR image pipeline on every page.
        with tempfile.TemporaryDirectory() as temp_dir:

            for page_number, page in enumerate(document):

                # 200 DPI gives a good balance between OCR
                # quality and memory usage.
                matrix = fitz.Matrix(
                            150 / 72,
                            150 / 72
                        )

                pixmap = page.get_pixmap(
                    matrix=matrix,
                    alpha=False
                )

                page_path = Path(temp_dir) / (
                    f"page_{page_number + 1}.png"
                )

                pixmap.save(str(page_path))

                page_text = ocr_image(
                    str(page_path)
                )

                if page_text:
                    page_results.append(
                        f"--- Page {page_number + 1} ---\n"
                        f"{page_text}"
                    )

        document.close()

        if not page_results:
            return None

        return "\n\n".join(page_results)

    except Exception as e:

        raise RuntimeError(
            f"Error during PDF OCR processing: {e}"
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