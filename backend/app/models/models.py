from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class CourseRate(Base):
    __tablename__ = "course_rates"

    id = Column(Integer, primary_order=True, primary_key=True, index=True)
    course_name = Column(String, unique = True, index = True, nullable = False)
    hourly_rate = Column(Float, nullable=False)

    # Relationship to sessions
    sessions = relationship("TeachingSession", back_populates="course")

class TeachingSession(Base):
    __tablename__ = "teaching_sessions"

    id = Column(Integer, primary_key =True, index=True)
    event_title = Column(String, nullable=False)
    event_date = Column(DateTime, default= datetime.utcnow)
    duration_hours = Column(Float, nullable=False)
    total_earnings = Column(Float, nullable=False)

    course_id = Column(Integer, ForeignKey("course_rates.id"), nullable=True)
    course = relationship("CourseRate", back_populates="sessions")
