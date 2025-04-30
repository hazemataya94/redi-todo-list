from base import Base
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import get_db
class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    status = Column(String, index=True)
    todo_list_id = Column(Integer, ForeignKey("todo_lists.id"))

    todo_list = relationship("TodoList", back_populates="tasks")
    
    def __init__(self, title: str, description: str, status: str, todo_list_id: int):
        self.title = title
        self.description = description
        self.status = status
        self.todo_list_id = todo_list_id
        
    def save(self):
        db = get_db()
        db.add(self)
        db.commit()
        db.refresh(self)
        return self
    
    @staticmethod
    def create(title: str, description: str, status: str, todo_list_id: int):
        task = Task(title=title, description=description, status=status, todo_list_id=todo_list_id)
        db = get_db()
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
    
    @staticmethod
    def get_all():
        db = get_db()
        return db.query(Task).all()
    