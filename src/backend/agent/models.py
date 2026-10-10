from sqlmodel import SQLModel, Field
from sqlalchemy import Column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
import uuid


class ChatModel(SQLModel, table=True):
    __tablename__ = "messages_table"

    thread_id: uuid.UUID = Field(
                            sa_column=Column(
                            pg. UUID,
                            nullable=False,
                            primary_key=True,
                            default=uuid.uuid4()))
    messages: list
    date : datetime = Field(Column(pg.TIMESTAMP, default=datetime.now) )