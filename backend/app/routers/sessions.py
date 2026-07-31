from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.db.database import get_db
import app.models.models as models
import app.schemas.schemas as schemas
from app.services.calendar_service import calculate_session_earnings

router = APIRouter(prefix="/sessions", tags=["Teaching Sessions"])

@router.post("/calculate", response_model=Dict[str, Any])
def calculate_salary_from_events(
    events: List[Dict[str, Any]], 
    db: Session = Depends(get_db)
):
    courses = db.query(models.CourseRate).all()
    course_rates = {course.course_name: course.hourly_rate for course in courses}
    
    if not course_rates:
        raise HTTPException(
            status_code=400, 
            detail="No hourly rate has been defined yet. Please enter the rates in the /courses section first."
        )
        
    sessions = calculate_session_earnings(events, course_rates)
    
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