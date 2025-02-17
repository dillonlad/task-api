from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TaskInBM(BaseModel):
    title: str
    description: Optional[str] = None
    priority: int  # Add validation on int to make sure between 1 and 3
    due_date: Optional[datetime] = None


class TaskBM(TaskInBM):
    class Config:
        from_attributes = True

    completed: bool = False


class UpdateTaskInBM(BaseModel):

    class Config:
        extra = "forbid"
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = None  # Add validation on int to make sure between 1 and 3
    due_date: Optional[datetime] = None
    completed: bool = None


class TaskOut(TaskBM):
    id: int


class MessageOut(BaseModel):
    message: str
