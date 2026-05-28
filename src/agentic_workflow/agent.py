from langchain_core.messages import AIMessage, HumanMessage,SystemMessage
from src.tools.plan_comptable import plan_comptable_tool
from langgraph.checkpoint.memory import MemorySaver
from src.tools.finance_law import finance_law_tool
from langgraph.graph import StateGraph, START, END 
from langchain_openrouter import ChatOpenRouter
from langgraph.prebuilt import tools_condition
from src.tools.web_search_tool import search
from langgraph.prebuilt import ToolNode
from typing_extensions import Annotated
from langgraph.graph import add_messages
from src.tools.cgnc import cgnc_tool
from src.tools.tax import CGI_tool
from typing import TypedDict,List
from  dotenv import  load_dotenv
import os

load_dotenv()


os.environ["OPENROUTER_API_KEY"] = os.getenv("OPENROUTER_API_KEY")  
tools=[cgnc_tool,finance_law_tool,CGI_tool,plan_comptable_tool,search]

MODEL = "nvidia/nemotron-3-nano-30b-a3b:free"
llm = ChatOpenRouter(model=MODEL)


llm_with_tools=llm.bind_tools(tools)


CHAT_PROMPT = """You are a Moroccan accounting and tax assistant.
You MUST always use a tool. NEVER answer from memory.

Tool routing rules:
1. Account number needed → plan_comptable_marocain
2. Accounting rule or principle → cgnc_maroc
3. Permanent tax rate or tax law → cgi_maroc
4. Recent/annual tax change + year mentioned → loi_finances_maroc
5. Current news, exchange rates, outside info → google_ssearch

NEVER invent article numbers or account codes."""


STRUCTURING_PROMPT = """You are a Moroccan accounting and tax assistant.
You received tool results. Now produce a clear, structured final answer in the same language as the user.

Rules:
- Cite the source tool used
- Use tables for journal entries (Débit / Crédit / Montant)
- If the tool result doesn't contain the answer, say so explicitly
- NEVER invent article numbers, account codes, or tax rates not present in the retrieved text"""






class AgentState(TypedDict):
    messages:Annotated[List,add_messages]

def chat_node(state: AgentState) -> dict:
    system_message = SystemMessage(content=CHAT_PROMPT)
    all_messages = [system_message] + state["messages"]
    response = llm_with_tools.invoke(all_messages)
    return {"messages": [response]}


def agent_structuring_response(state: AgentState):
    system_message = SystemMessage(content=STRUCTURING_PROMPT)
    all_messages = [system_message] + state["messages"]
    return {"messages": [llm_with_tools.invoke(all_messages)]}



tool_node=ToolNode(tools)


# ── Build the graph ──
builder = StateGraph(AgentState)
builder.add_node("chat", chat_node)
builder.add_node("tool_node", tool_node)
builder.add_node("structures", agent_structuring_response)


builder.add_edge(START, "chat")
builder.add_conditional_edges(
    "chat",
    tools_condition,
    {
        "tools": "tool_node",
        "__end__": END
    }
)
builder.add_edge("tool_node", "structures")
builder.add_conditional_edges(
    "structures",
    tools_condition,
    {
        "tools": "tool_node",
        "__end__": END
    }
)
checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)

