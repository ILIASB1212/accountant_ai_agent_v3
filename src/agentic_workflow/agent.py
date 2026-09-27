from langchain_core.messages import AIMessage, HumanMessage,SystemMessage
from src.tools.plan_comptable import plan_comptable_tool
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables import RunnableConfig
from src.tools.finance_law import finance_law_tool
from langgraph.graph import StateGraph, START, END 
from langchain.chat_models import init_chat_model
from langchain_openrouter import ChatOpenRouter
from langgraph.prebuilt import tools_condition
from src.tools.web_search_tool import search
from langgraph.prebuilt import ToolNode
from typing_extensions import Annotated
from langgraph.graph import add_messages
from src.tools.cgnc import cgnc_tool
from src.tools.tax import CGI_tool
from src.tools.la_rac import ras_tool
from typing import TypedDict,List
from  dotenv import  load_dotenv
import os

load_dotenv()



os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
#os.environ["OPENROUTER_API_KEY"] = os.getenv("OPENROUTER_API_KEY") 
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")  

tools=[cgnc_tool,finance_law_tool,CGI_tool,plan_comptable_tool,search,ras_tool]

MODEL = "openai:gpt-4o-mini"
llm = init_chat_model(model=MODEL, temperature=0)

llm_with_tools=llm.bind_tools(tools)


CHAT_PROMPT = """You are a Moroccan accounting and tax assistant.
                    You MUST always use a tool.

                    Tool routing rules:
                    1. Account number needed → plan_comptable_marocain
                    2. Accounting rule or principle → cgnc_maroc
                    3. Permanent tax rate or tax law → cgi_maroc
                    4. Recent/annual tax change + year mentioned → loi_finances_maroc
                    5. Current news, exchange rates, outside info → google_ssearch

                    NEVER invent article numbers or account codes."""






class AgentState(TypedDict):
    messages:Annotated[List,add_messages]

def chat_node(state: AgentState, config: RunnableConfig) -> dict:
    # Mem0 long-term memory arrives via config, not via the message list,
    # so it never gets permanently written into the checkpointed thread history.
    memory_context = config.get("configurable", {}).get("memory_context", "")
 
    system_content = CHAT_PROMPT
    if memory_context:
        system_content = (
            f"{CHAT_PROMPT}\n\n"
            f"Known user context (from long-term memory):\n{memory_context}"
        )
 
    system_message = SystemMessage(content=system_content)
    all_messages = [system_message] + state["messages"]
    response = llm_with_tools.invoke(all_messages)
    return {"messages": [response]}





tool_node=ToolNode(tools)


# ── Build the graph ──
builder = StateGraph(AgentState)
builder.add_node("chat", chat_node)
builder.add_node("tool_node", tool_node)
#builder.add_node("structures", agent_structuring_response)


builder.add_edge(START, "chat")
builder.add_conditional_edges(
    "chat",
    tools_condition,
    {
        "tools": "tool_node",
        "__end__": END
    }
)
builder.add_edge("tool_node", "chat")

checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)

