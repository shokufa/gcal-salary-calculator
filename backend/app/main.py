from fastapi import FastAPI 
from app.db.database import engine, Base
import app.models.models as models
from app.routers import courses, sessions
from fastapi.middleware.cors import CORSMiddleware

# Create database tables automatically if they don't exist yet
Base.metadata.create_all(bind = engine)

app = FastAPI(
    title="Google Calender Salary Calculator",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Regiter routers
app.include_router(courses.router)
app.include_router(sessions.router)

@app.get("/")
def reaf_root():
    return {
        "status":"online",
        "message": "FastAPI backend is up and running!"
    }
