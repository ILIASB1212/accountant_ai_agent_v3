from sqlmodel import SQLModel, Field
from sqlalchemy import Column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
import uuid


import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlmodel import SQLModel, Field


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class ChatSession(SQLModel, table=True):
    __tablename__ = "chat_sessions"
    __table_args__ = (
        UniqueConstraint("thread_id", name="uq_chat_sessions_thread_id"),
    )

    uid: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
    )
    user_id: uuid.UUID = Field(
        foreign_key="users.uid",
        nullable=False,
        index=True,
    )
    company_id: uuid.UUID = Field(
        foreign_key="companies.uid",
        nullable=False,
        index=True,
    )
    thread_id: str = Field(nullable=False)
    created_at: datetime = Field(
        default_factory=utc_now,
        sa_type=DateTime(timezone=True),
    )


class Message(SQLModel, table=True):
    __tablename__ = "messages"

    uid: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
    )
    session_id: uuid.UUID = Field(
        foreign_key="chat_sessions.uid",
        nullable=False,
        index=True,
    )
    role: str = Field(nullable=False)
    content: str = Field(
        sa_column=Column(Text, nullable=False)
    )
    created_at: datetime = Field(
        default_factory=utc_now,
        sa_type=DateTime(timezone=True),
    )