from fastapi import APIRouter,HTTPException
from src.agentic_workflow.agent import graph
from datetime import datetime
from fastapi.responses import PlainTextResponse
from src.backend.agent.schemas import ChatModel

agent_router=APIRouter()

@agent_router.get("/health")
def ask_agent():
    return {"status": "ok"}



@agent_router.post("/invoke")
def ask_agent(request:ChatModel):
    try:
        config = {"configurable": {"thread_id": request.thread_id}}
        start=datetime.now()

        response = graph.invoke({"messages": request.messages}, config=config)
        end = f"_Response generated in {(datetime.now()-start).total_seconds():.2f} seconds_"
        text= f"{end} \n {response['messages'][-1].content}"
        return PlainTextResponse(content=text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




