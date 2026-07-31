from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Database URL pointing to a local SQLite file named salary_calculator.db
SQLALCHEMY_DATABASE_URL = "sqlite:///./salary_calculator.db"

# connect_args={"check_same_thread": False} is required specifically for SQLite in FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency function to get a database session for API requests
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()