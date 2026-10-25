import logging
from datetime import datetime

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request
from fastapi.responses import PlainTextResponse
from langchain_core.messages import HumanMessage
from postgrest.exceptions import APIError

from src.backend.agent.schemas import ChatModel, ClientCreate, SessionCreate
from src.backend.dependencies import Membership, active_member, db_error
from src.memory.memory_class import Memory

logger = logging.getLogger(__name__)
agent_router = APIRouter()


@agent_router.get("/health")
def check_health():
    return {"status": "ok"}


# ------------------------------------------------------------ client firms

@agent_router.post("/clients", status_code=201)
def add_client_firm(body: ClientCreate, m: Membership = Depends(active_member)):
    """A firm the fiduciary works for. Chat sessions are opened per client firm."""
    try:
        res = (
            m.user.db.table("clients")
            .insert({"company_id": m.company_id, "name": body.name.strip()})
            .execute()
        )
    except APIError as e:
        raise db_error(e)
    return res.data[0]


@agent_router.get("/clients")
def list_client_firms(m: Membership = Depends(active_member)):
    return (
        m.user.db.table("clients").select("id,name,created_at")
        .eq("company_id", m.company_id).order("name").execute().data
    )


# ------------------------------------------------------------ sessions

@agent_router.post("/sessions", status_code=201)
def create_session(body: SessionCreate, m: Membership = Depends(active_member)):
    client = (
        m.user.db.table("clients").select("id,name")
        .eq("id", str(body.client_id)).limit(1).execute().data
    )
    if not client:  # also what a client firm of ANOTHER company looks like: RLS hides it
        raise HTTPException(404, "Client firm not found.")
    try:
        res = (
            m.user.db.table("chat_sessions")
            .insert(
                {
                    "company_id": m.company_id,
                    "client_id": client[0]["id"],
                    "created_by": m.user.id,
                    "title": (body.title or client[0]["name"]).strip(),
                }
            )
            .execute()
        )
    except APIError as e:
        raise db_error(e)
    return res.data[0]


@agent_router.get("/sessions")
def list_sessions(client_id: str | None = None, m: Membership = Depends(active_member)):
    q = m.user.db.table("chat_sessions").select("id,client_id,title,created_by,created_at")
    if client_id:
        q = q.eq("client_id", client_id)
    return q.order("created_at", desc=True).limit(100).execute().data


def _get_session(m: Membership, session_id: str) -> dict:
    rows = (
        m.user.db.table("chat_sessions").select("id,company_id,client_id")
        .eq("id", session_id).limit(1).execute().data
    )
    if not rows:
        raise HTTPException(404, "Session not found.")
    return rows[0]


@agent_router.get("/sessions/{session_id}/messages")
def session_messages(session_id: str, m: Membership = Depends(active_member)):
    _get_session(m, session_id)
    return (
        m.user.db.table("messages").select("id,role,content,created_at")
        .eq("session_id", session_id).order("id").execute().data
    )


# ------------------------------------------------------------ chat

def _remember(memory: Memory, answer: str) -> None:
    """Runs after the response is sent; memory problems must never break a chat."""
    try:
        payload = memory.semantic_memory_for_facts(answer)
        if payload:
            memory.store_memory(payload)
    except Exception:
        logger.exception("mem0 store failed")


@agent_router.post("/invoke")
def ask_agent(
    body: ChatModel,
    request: Request,
    background: BackgroundTasks,
    m: Membership = Depends(active_member),
):
    session = _get_session(m, str(body.session_id))  # 404 unless it is in the caller's company

    client = (
        m.user.db.table("clients").select("name")
        .eq("id", session["client_id"]).limit(1).execute().data
    )
    client_name = client[0]["name"] if client else ""

    # Long-term memory is scoped by IDs read from the database row, never from the request.
    memory = Memory.for_client(body.message, session["company_id"], session["client_id"])
    try:
        memory_context = memory.format_context_for_systeme(memory.retrive())
    except Exception:
        logger.exception("mem0 search failed")
        memory_context = ""

    config = {
        "configurable": {
            "thread_id": str(body.session_id),  # conversation state lives per session
            "memory_context": memory_context,   # picked up by chat_node, never enters the checkpoint
            "client_name": client_name,
        }
    }

    start = datetime.now()
    try:
        result = request.app.state.graph.invoke(
            {"messages": [HumanMessage(content=body.message)]}, config=config
        )
    except Exception:
        logger.exception("agent failed")
        raise HTTPException(500, "The agent could not answer. Please try again.")
    answer = result["messages"][-1].content
    answer = answer if isinstance(answer, str) else str(answer)
    elapsed = (datetime.now() - start).total_seconds()

    try:  # history for the UI; the checkpointer stays the source of truth for the agent
        m.user.db.table("messages").insert(
            [
                {"session_id": str(body.session_id), "role": "user", "content": body.message},
                {"session_id": str(body.session_id), "role": "assistant", "content": answer},
            ]
        ).execute()
    except APIError:
        logger.exception("could not save chat history")

    background.add_task(_remember, memory, answer)
    return PlainTextResponse(f"_Response generated in {elapsed:.2f} seconds_ \n {answer}")
