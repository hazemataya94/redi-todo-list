from pydantic import BaseModel
from typing import List, Optional

class User(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class TodoList(BaseModel):
    id: int
    user_id: int
    title: str

    class Config:
        from_attributes = True

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: str
    todo_list_id: int

    class Config:
        from_attributes = True 