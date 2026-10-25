from uuid import UUID

from pydantic import BaseModel, Field


class ClientCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)


class SessionCreate(BaseModel):
    client_id: UUID
    title: str | None = Field(default=None, max_length=120)  # defaults to the client firm's name


class ChatModel(BaseModel):
    # The session id doubles as the LangGraph thread_id. The server looks the session
    # up through RLS, so a user can only ever talk to sessions of their own company.
    session_id: UUID
    # One plain user turn. Roles/system messages are never accepted from the client.
    message: str = Field(min_length=1, max_length=20000)
