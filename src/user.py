from src.base import Base
from src.database import get_db

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from passlib.context import CryptContext

class User(Base):
    __tablename__ = "users"
        
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    
    todo_lists = relationship("TodoList", back_populates="owner")

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def __init__(self, username: str, password: str):
        self.username = username
        self.password_hash = User.hash_password(password)

    def validate_password(self, password: str) -> bool:
        return self.pwd_context.verify(password, self.password_hash)
    
    @staticmethod
    def hash_password(password: str) -> str:
        return User.pwd_context.hash(password)

    def validate(self) -> tuple[bool, str]:
        if not self.username or not isinstance(self.username, str) and len(self.username) < 3:
            return False, "Username must be a string and at least 3 characters long"
        if not self.password_hash or not isinstance(self.password_hash, str) and len(self.password_hash) < 8:
            return False, "Password must be a string and at least 8 characters long"
        # if username already exists
        db = get_db()
        if db.query(User).filter(User.username == self.username).first():
            return False, "Username already exists"
        return True, "User created successfully"

    def save(self):
        valid, message = self.validate()
        if not valid:
            raise ValueError(message)
        
        db = get_db()
        db.add(self)
        db.commit()
        db.refresh(self)
        
        return self

    @staticmethod
    def create(username: str, password: str):
        hashed_password = User.hash_password(password)
        
        user = User(username=username, password_hash=hashed_password)
        
        valid, message = user.validate()
        if not valid:
            raise ValueError(message)
        
        db = get_db()
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return user
    
    def get_all():
        db = get_db()
        return db.query(User).all()