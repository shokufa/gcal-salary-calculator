from fastapi import FastAPI 
from app.db.database import engine, Base
import app.models.models as models

# Create database tables automatically if they don't exist yet
Base.metadata.create_all(bind = engine)

app = FastAPI(
    title="Google Calender Salary Calculator",
    version="1.0.0"
)

@app.get("/")
def reaf_root():
    return {
        "status":"online",
        "message": "FastAPI backend is up and running!"
    }
