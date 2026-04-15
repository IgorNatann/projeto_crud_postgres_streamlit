
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

POSTGRES_DATABASE_URL = 'postgresql://user_crud:password_crud@localhost:5432/database_crud'

engine = create_engine(POSTGRES_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() #ORM

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()