import hashlib
import os
import tempfile
from pathlib import Path
from datetime import datetime

import streamlit as st
from langchain_core.messages import HumanMessage

from src.tools.glm_ocr import ocr_document


st.title("Agentic Workflow: Moroccan Accounting & Tax Assistant")


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    session_name = st.text_input(
        "Session name",
        key="session_name"
    )


# ============================================================
# LOAD AGENT
# ============================================================

@st.cache_resource
def load_agent():
    from src.agentic_workflow.agent import graph
    return graph


# ============================================================
# GET RESPONSE
# ============================================================

def get_response(user_text: str):

    if not user_text or not user_text.strip():
        return "Please enter a question."

    agent = load_agent()

    config = {
        "configurable": {
            "thread_id": (
                st.session_state.session_name
                or "default_thread"
            )
        }
    }

    result = agent.invoke(
        {
            "messages": [
                HumanMessage(content=user_text)
            ]
        },
        config=config
    )

    return result["messages"][-1].content


# ============================================================
# INITIALIZE SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "ocr_result" not in st.session_state:
    st.session_state.ocr_result = None

if "uploaded_file_id" not in st.session_state:
    st.session_state.uploaded_file_id = None

if "ocr_time" not in st.session_state:
    st.session_state.ocr_time = None


# ============================================================
# CHAT HISTORY
# ============================================================

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# ============================================================
# OCR UPLOAD
# ============================================================

uploaded_file = st.file_uploader(
    "Upload an image or PDF for OCR",
    type=["png", "jpg", "jpeg", "pdf"]
)


if uploaded_file is not None:

    file_bytes = uploaded_file.getvalue()
    file_id = hashlib.md5(file_bytes).hexdigest()

    # Only process a file once per Streamlit session.
    if st.session_state.uploaded_file_id != file_id:

        suffix = Path(uploaded_file.name).suffix.lower()

        if not suffix:
            st.error("Could not determine the uploaded file type.")
            st.stop()

        start_ocr_time = datetime.now()

        # Keep the original extension. This is important because
        # OCR routing uses the file extension to distinguish
        # images from PDFs.
        temp_path = None

        try:
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=suffix
            ) as temp_file:
                temp_file.write(file_bytes)
                temp_path = temp_file.name

            with st.spinner("Reading file with GLM-OCR..."):
                st.session_state.ocr_result = ocr_document(
                    temp_path
                )

            st.session_state.uploaded_file_id = file_id
            st.session_state.ocr_time = (
                datetime.now() - start_ocr_time
            )

        except Exception as e:
            st.session_state.ocr_result = None
            st.session_state.uploaded_file_id = None
            st.error(f"OCR failed: {e}")

        finally:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)

    # Display OCR result
    if st.session_state.ocr_result:

        st.success("File processed successfully")

        with st.expander("View OCR result"):
            if st.session_state.ocr_time:
                st.write(
                    f"OCR Time: {st.session_state.ocr_time.total_seconds():.2f} seconds"
                )

            st.write(st.session_state.ocr_result)


# ============================================================
# USER INPUT
# ============================================================

text = st.chat_input(
    "Ask a question about Moroccan accounting or taxation"
)


# ============================================================
# PROCESS REQUEST
# ============================================================

if text:

    start = datetime.now()

    # --------------------------------------------------------
    # Build prompt
    # --------------------------------------------------------

    if st.session_state.ocr_result:

        final_prompt = f"""
The user uploaded a document and GLM-OCR extracted the following text:

--- OCR TEXT ---
{st.session_state.ocr_result}
--- END OCR TEXT ---

User's question:

{text}

Use the OCR text as context when answering the user's question.
"""

    else:

        final_prompt = text

    # --------------------------------------------------------
    # Display user message
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": text
        }
    )

    with st.chat_message("user"):
        st.markdown(text)

    # --------------------------------------------------------
    # Generate assistant response
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):
            response = get_response(final_prompt)

        elapsed = (
            datetime.now() - start
        ).total_seconds()

        st.markdown(response)

        st.caption(
            f"Response generated in {elapsed:.2f} seconds"
        )

    # --------------------------------------------------------
    # Save assistant response
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )
