from fastapi import FastAPI
from pydantic import BaseModel
from src.agentic_workflow.agent import graph
from datetime import datetime
from fastapi.responses import PlainTextResponse


app=FastAPI()

class ChatModel(BaseModel):
    thread_id: str
    messages: str



@app.post("/invoke")
def ask_agent(request:ChatModel):
    config = {"configurable": {"thread_id": request.thread_id}}
    start=datetime.now()

    response = graph.invoke({"messages": request.messages}, config=config)
    end = f"_Response generated in {(datetime.now()-start).total_seconds():.2f} seconds_"
    text= f"{end} \n {response['messages'][-1].content}"
    return PlainTextResponse(content=text)




