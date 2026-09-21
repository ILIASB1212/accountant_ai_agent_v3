import streamlit as st
from langchain_core.messages import HumanMessage
from datetime import datetime
from src.tools.ocr import ocr_image
st.title("Agentic Workflow: Moroccan Accounting & Tax Assistant")

with st.sidebar:
    session_name = st.text_input("Session name", key="session_name")

# 1. Cache the heavy graph import/initialization
@st.cache_resource
def load_agent():
    from src.agentic_workflow.agent import graph
    return graph

# 2. Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. Get input
text = st.chat_input("Ask questions")

with st.sidebar:
    uploaded_image = st.file_uploader("Upload an image for OCR", type=["png", "jpg", "jpeg"])
    if uploaded_image is not None:
        # Save the uploaded image to a temporary file
        with open("temp_image.png", "wb") as f:
            f.write(uploaded_image.getbuffer())
        # Perform OCR on the uploaded image
        ocr_result = ocr_image("temp_image.png")
        if ocr_result:
            st.write("**img loaded successfully!**")
            st.markdown(f"**OCR Result:** {ocr_result}")







# 5. Only run when there is actual input
if text:
    start=datetime.now()
    # Show user message
    st.session_state.messages.append({"role": "user", "content": text})
    with st.chat_message("user"):
        st.markdown(text)

    # 6. Cache the expensive graph invocation
    def get_response(user_text: str):
        agent = load_agent()
        config = {"configurable": {"thread_id": st.session_state.session_name or "default_thread"}}
        result = agent.invoke({"messages": [HumanMessage(content=user_text)]}, config=config)
        # Return a plain serializable string so Streamlit can cache it
        return result["messages"][-1].content

    # 7. Show assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_response(text)
            st.write(f"_Response generated in {(datetime.now()-start).total_seconds():.2f} seconds_")
            st.markdown(response)

    # 8. Save to history
    st.session_state.messages.append({"role": "assistant", "content": response})