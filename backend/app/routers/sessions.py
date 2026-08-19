from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from app.db.database import get_db
import app.models.models as models
from app.services.calendar_service import (
    fetch_google_calendar_events,
    calculate_session_earnings
)

router = APIRouter(prefix="/sessions", tags=["Teaching Sessions"])

class CalendarCalculateRequest(BaseModel):
    google_token: str
    start_date: str          # YYYY-MM-DD
    end_date: str            # YYYY-MM-DD
    title_filter: Optional[str] = None
    only_sage: bool = True

@router.post("/calculate", response_model=Dict[str, Any])
def calculate_salary_from_events(
    req: CalendarCalculateRequest, 
    db: Session = Depends(get_db)
):
    # Fetch course rates from DB
    courses = db.query(models.CourseRate).all()
    course_rates = {course.course_name: course.hourly_rate for course in courses}
    
    if not course_rates:
        raise HTTPException(
            status_code=400, 
            detail="No hourly rates defined in DB. Please add course rates first in /courses."
        )

    # Fetch events from Google Calendar
    events = fetch_google_calendar_events(req.google_token, req.start_date, req.end_date)
    
    if events is None:
        raise HTTPException(
            status_code=400,
            detail="Failed to fetch events from Google Calendar. Check token/permissions."
        )

    # Calculate earnings filtering by Sage green
    sessions = calculate_session_earnings(
        events=events, 
        course_rates=course_rates, 
        only_sage=req.only_sage,
        title_filter=req.title_filter
    )
    
    grand_total_hours = sum(s.get("duration_hours", 0.0) for s in sessions)
    grand_total_earnings = sum(s.get("total_earnings", 0.0) for s in sessions)
    
    return {
        "summary": {
            "total_hours": round(grand_total_hours, 2),
            "total_salary": round(grand_total_earnings, 2),
            "total_sessions": len(sessions)
        },
        "sessions": sessions
    }