from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# --- Course Rate Schemas ---
class CourseRateBase(BaseModel):
    course_name: str
    hourly_rate: float

class CourseRateCreate(CourseRateBase):
    pass

class CourseRate(CourseRateBase):
    id: int

    class Config:
        from_attributes = True

# --- Teaching Session Schemas ---
        
class TeachingSessionBase(BaseModel):
    event_title: str
    duration_hourse: float
    total_earnings: float
    course_id: Optional[int] = None

class TeachingSessionCreate(TeachingSessionBase):
    event_date: Optional[datetime] = None

class TeachingSession(TeachingSessionBase):
    id: int
    event_date: datetime

    class Config:
        from_attributes = True
