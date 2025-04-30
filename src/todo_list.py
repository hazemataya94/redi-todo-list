from src.base import Base
from src.database import get_db

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class TodoList(Base):
    __tablename__ = "todo_lists"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="todo_lists")
    tasks = relationship("Task", back_populates="todo_list")
    
    def __init__(self, title: str, user_id: int):
        self.title = title
        self.user_id = user_id
        
    def save(self):
        db = get_db()
        db.add(self)
        db.commit()
        db.refresh(self)
        return self
    
    @staticmethod
    def create(title: str, user_id: int):
        todo_list = TodoList(title=title, user_id=user_id)
        db = get_db()
        db.add(todo_list)
        db.commit()
        db.refresh(todo_list)
        return todo_list
    
    @staticmethod
    def get_all():
        db = get_db()
        return db.query(TodoList).all()
    