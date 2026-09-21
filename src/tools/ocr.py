
from transformers import AutoProcessor, GlmOcrForConditionalGeneration
model_id = "zai-org/GLM-OCR"

# Load processor
processor = AutoProcessor.from_pretrained(model_id)

# Load model
model = GlmOcrForConditionalGeneration.from_pretrained(
    model_id,
    device_map="auto",
)


def ocr_image(image_path:str):

     try:
          # Your image + OCR instruction
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "url": image_path},
                    {"type": "text", "text": "Text Recognition:"},
                ],
            }
        ]

        # Convert message into model inputs
        inputs = processor.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_dict=True,
            return_tensors="pt",
        ).to(model.device)

        # Generate OCR result
        output = model.generate(**inputs,
            max_new_tokens=512
        )

        # Decode result
        text = processor.decode(output[0],
            skip_special_tokens=True
        )
        return text
     except Exception as e:
         print(f"Error during OCR processing: {e}")
         return None