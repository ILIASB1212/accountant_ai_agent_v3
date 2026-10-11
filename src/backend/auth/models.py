
import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlmodel import SQLModel, Field


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class User(SQLModel, table=True):
    __tablename__ = "users"

    uid: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
    )
    email: str = Field(
        sa_column=Column(String, nullable=False, unique=True, index=True)
    )
    password_hash: str = Field(
        sa_column=Column(String, nullable=False)
    )
    created_at: datetime = Field(
        default_factory=utc_now,
        sa_type=DateTime(timezone=True),
    )


class Company(SQLModel, table=True):
    __tablename__ = "companies"

    uid: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
    )
    name: str = Field(nullable=False, index=True)
    created_at: datetime = Field(
        default_factory=utc_now,
        sa_type=DateTime(timezone=True),
    )



