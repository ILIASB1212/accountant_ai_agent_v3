import hashlib
import os
import tempfile
from pathlib import Path
from datetime import datetime

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessageChunk

from src.tools.glm_ocr import ocr_document
from src.memory.memory_class import Memory


st.title("Internal knowledge Base RAG: Moroccan Accounting & Tax Assistant")


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
# GET RESPONSE (STREAMING VERSION - FILTERED FOR CONTENT ONLY)
# ============================================================

def get_response(user_text: str):
    if not user_text or not user_text.strip():
        yield "Please enter a question."
        return

    agent = load_agent()
    memory = Memory(user_prompt=user_text, user_id="ilias", agent_id="agent1")
    long_tm = memory.retrive()
    memory_context = memory.format_context_for_systeme(long_tm)

    config = {
        "configurable": {
            "thread_id": (
                st.session_state.session_name
                or "default_thread"
            ),
            # picked up by chat_node in agent.py; never enters the message list
            "memory_context": memory_context,
        }
    }

    full_response = ""
    try:
        # Try to stream the response
        for chunk in agent.stream(
            {"messages": [HumanMessage(content=user_text)]},
            config=config,
            stream_mode="messages"
        ):
            # Extract ONLY the AI-generated content chunks, ignore metadata/tool calls
            content = ""

            # Handle direct AIMessageChunk objects (these contain the actual LLM responses)
            if isinstance(chunk, AIMessageChunk):
                content = chunk.content
            # Handle tuple format where first element might be AIMessageChunk
            elif isinstance(chunk, tuple) and len(chunk) >= 1:
                first_elem = chunk[0]
                if isinstance(first_elem, AIMessageChunk):
                    content = first_elem.content
            # Handle dict format that might contain AI-generated content
            elif isinstance(chunk, dict):
                # Look for AIMessageChunk-like content in dict
                if 'content' in chunk and isinstance(chunk['content'], str):
                    content = chunk['content']
                # Sometimes the content is nested differently
                elif 'messages' in chunk and isinstance(chunk['messages'], list):
                    # Look for the latest AI message in messages
                    for msg in reversed(chunk['messages']):
                        if hasattr(msg, 'content') and isinstance(msg.content, str):
                            content = msg.content
                            break
                        elif isinstance(msg, dict) and msg.get('type') == 'ai' and 'content' in msg:
                            content = msg['content']
                            break

            # Only yield non-empty content from AI messages to avoid spamming empty chunks
            # and ignore pure metadata/tool call chunks
            if content and isinstance(content, str) and content.strip():
                full_response += content
                yield content
    except Exception as e:
        # If streaming fails, fall back to non-streaming
        agent_response = agent.invoke({"messages": [HumanMessage(content=user_text)]}, config=config)
        fallback_content = agent_response["messages"][-1].content
        if fallback_content and isinstance(fallback_content, str) and fallback_content.strip():
            full_response = fallback_content
            yield full_response
        else:
            # If fallback also empty, use default message
            full_response = "I’m sorry, but I can’t comply with that request."
            yield full_response

    # If after streaming (and fallback) we still have no response, provide a default
    if not full_response:
        full_response = "I’m sorry, but I can’t comply with that request."
        yield full_response

    # Update memory with the full response after streaming is complete
    # Wrap in try/except to prevent crashes if memory storage fails
    try:
        x = memory.semantic_memory_for_facts(full_response)
        if x:
            # Additional validation to ensure we have valid data
            if (isinstance(x, dict) and
                x.get("text") and isinstance(x["text"], str) and x["text"].strip() and
                x.get("llm_output") and isinstance(x["llm_output"], str) and x["llm_output"].strip()):
                memory.store_memory(x)
    except Exception as mem_error:
        # If memory storage fails, continue without storing (don't crash the app)
        pass


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
        # Consume the OCR result for this question only, then clear it
        ocr_context = st.session_state.ocr_result
        st.session_state.ocr_result = None  # Clear after use to prevent persistence

        final_prompt = f"""
The user uploaded a document and GLM-OCR extracted the following text:

--- OCR TEXT ---
{ocr_context}
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
    # Generate assistant response (STREAMED - CONTENT ONLY)
    # --------------------------------------------------------

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for chunk in get_response(final_prompt):
            full_response += chunk
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

        elapsed = (
            datetime.now() - start
        ).total_seconds()

        st.caption(
            f"Response generated in {elapsed:.2f} seconds"
        )

    # --------------------------------------------------------
    # Save assistant response
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": full_response
        }
    )