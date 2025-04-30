from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./todo.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create a new session for each request
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def get_db():
    return next(get_session())

