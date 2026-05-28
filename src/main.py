import streamlit as st
from langchain_core.messages import HumanMessage
from datetime import datetime
st.title("Agentic Workflow: Moroccan Accounting & Tax Assistant")

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

# 5. Only run when there is actual input
if text:
    start=datetime.now()
    # Show user message
    st.session_state.messages.append({"role": "user", "content": text})
    with st.chat_message("user"):
        st.markdown(text)

    # 6. Cache the expensive graph invocation
    @st.cache_data(show_spinner=False)
    def get_response(user_text: str):
        agent = load_agent()
        config = {"configurable": {"thread_id": "session_1"}}
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