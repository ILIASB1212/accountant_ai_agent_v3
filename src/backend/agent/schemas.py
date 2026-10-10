from pydantic import BaseModel


class ChatModel(BaseModel):
    thread_id: str
    messages: list