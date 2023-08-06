from uuid import uuid4
from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional


def get_id():
    return str(uuid4())

class LogModel(SQLModel, table=True):
    __tablename__="logs"
    id: Optional[int] = Field(primary_key=True)
    session_id: Optional[str] = Field(default=None)
    task: str = Field(default=None, index=True)
    description: Optional[str] = Field(default=None)
    type: str = Field(default="info", index=True)
    data: Optional[str] = Field(default=None)
    objects : Optional[str] = Field(default=None)

    
    start_time: datetime = Field(default=datetime.now(), index=True) 
    end_time: datetime = Field(default=datetime.now(), index=True)
    
    
    created_at: datetime = Field(default=datetime.now(), index=True)
    

class ObjectModel(SQLModel, table=True):
    __tablename__ = "objects"
    id: Optional[int] = Field(primary_key=True)
    title: str
    type: str
    object: Optional[bytes] = Field(None)
    created_at: datetime = Field(default=datetime.now(), index=True)

