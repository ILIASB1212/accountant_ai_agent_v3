from src.tools.plan_comptable import plan_comptable_tool
from src.tools.cgnc import cgnc_tool
from src.tools.finance_law import finance_law_tool
from src.tools.tax import CGI_tool
from src.tools.web_search_tool import search
from  dotenv import  load_dotenv
from langchain_openrouter import ChatOpenRouter
import os

from langgraph.prebuilt import tools_condition
from langchain_core.messages import AIMessage, HumanMessage,SystemMessage

from langgraph.graph import StateGraph, START, END 
from langgraph.prebuilt import ToolNode
from typing import TypedDict,List
from typing_extensions import Annotated
from langgraph.graph import add_messages

load_dotenv()


os.environ["OPENROUTER_API_KEY"] = os.getenv("OPENROUTER_API_KEY")  
tools=[cgnc_tool,finance_law_tool,CGI_tool,plan_comptable_tool,search]

MODEL = "nvidia/nemotron-3-super-120b-a12b:free"
llm = ChatOpenRouter(model=MODEL)


llm_with_tools=llm.bind_tools(tools)


SYSTEM_PROMPT = """You are a Moroccan accounting and tax assistant. 
Follow this STRICT routing hierarchy:

1. Need an ACCOUNT NUMBER → plan_comptable_marocain
2. Need an ACCOUNTING RULE or PRINCIPLE → cgnc_maroc  
3. Need a TAX RATE or PERMANENT TAX RULE → cgi_maroc
4. Need a RECENT/ANNUAL tax change with YEAR mentioned → loi_finances_maroc
5. Need CURRENT news, exchange rates, or outside info → google_search

NEVER invent article numbers. If the retrieved text doesn't contain the answer, say so."""





class AgentState(TypedDict):
    messages:Annotated[List,add_messages]

def chat_node(state: AgentState) -> dict:
    """A simple node that appends an AI response."""
    # `state["messages"]` already contains the full conversation history
    last_human_msg = state["messages"][-1].content if state["messages"] else ""

    response = llm_with_tools.invoke(last_human_msg)

    return {"messages": [response]}







def agent_structuring_response(state: AgentState):
    # Find the last ToolMessage to know which tool was used
    
    system_message = SystemMessage(content=SYSTEM_PROMPT)

    all_messages = [system_message] + state["messages"][-5:]
    return {"messages": [llm_with_tools.invoke(all_messages)]}



tool_node=ToolNode(tools)


# ── Build the graph ──
builder = StateGraph(AgentState)
builder.add_node("chat", chat_node)
builder.add_node("tool_node", tool_node)
builder.add_node("structures", agent_structuring_response)


builder.add_edge(START, "chat")
builder.add_edge("chat", "tool_node")
builder.add_edge("tool_node", "structures")
builder.add_conditional_edges(
    "structures",
    tools_condition,
    {
        "tools": "tool_node",
        "__end__": END
    }
)
builder.add_edge("structures", END)



graph = builder.compile()

