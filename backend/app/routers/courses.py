from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
import app.models.models as models
import app.schemas.schemas as schemas

router = APIRouter(prefix="/courses", tags=["Course Rates"])

@router.post("/", response_model=schemas.CourseRate)
def create_course_rate(course: schemas.CourseRateCreate, db: Session = Depends(get_db)):
    db_course = db.query(models.CourseRate).filter(models.CourseRate.course_name == course.course_name).first()
    if db_course:
        raise HTTPException(status_code=400, detail="Course rate with this name already exists")
    
    new_course = models.CourseRate(
        course_name=course.course_name,
        hourly_rate=course.hourly_rate
    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

@router.get("/", response_model=List[schemas.CourseRate])
def get_all_courses(db: Session = Depends(get_db)):
    return db.query(models.CourseRate).all()

@router.delete("/{course_id}")
def delete_course_rate(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.CourseRate).filter(models.CourseRate.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    db.delete(course)
    db.commit()
    return {"message": f"Course ID {course_id} deleted successfully"}