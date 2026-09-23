import streamlit as st

from transformers import (
    AutoProcessor,
    GlmOcrForConditionalGeneration
)


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

        output = model.generate(
            **inputs,
            max_new_tokens=256
        )

        text = processor.decode(
            output[0],
            skip_special_tokens=True
        )

        # Remove unwanted image tokens
        text = text.replace(
            "<|image|>",
            ""
        )

        # Remove the OCR instruction if returned
        text = text.replace(
            "Text Recognition:",
            ""
        )

        # Clean whitespace
        text = " ".join(text.split())

        return text.strip()

    except Exception as e:

        print(
            f"Error during image OCR processing: {e}"
        )

        return None


# ============================================================
# PDF OCR
# ============================================================

@st.cache_resource
def load_pdf_parser():

    import glmocr

    parser = glmocr.GlmOcrParser()

    return parser


def ocr_pdf(pdf_path: str):

    try:

        parser = load_pdf_parser()

        result = parser.parse(pdf_path)

        return result

    except Exception as e:

        print(
            f"Error during PDF OCR processing: {e}"
        )

        return None


# ============================================================
# GENERAL OCR FUNCTION
# ============================================================

def ocr_document(file_path: str):

    file_path = file_path.lower()

    if file_path.endswith(
        (".png", ".jpg", ".jpeg")
    ):

        return ocr_image(file_path)

    elif file_path.endswith(".pdf"):

        return ocr_pdf(file_path)

    else:

        print(
            "Unsupported file type."
        )

        return None
