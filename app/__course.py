from typing import Annotated
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
from models import Courses
from starlette import status
from database import SessionLocal
from schema import CourseRequest

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/course", operation_id="get_course")
async def read_all(db: db_dependency):
    return db.query(Courses).all()

@app.post("/course", status_code=status.HTTP_201_CREATED)
async def create_course(db: db_dependency, course_request: CourseRequest):
    course_model = Courses(**course_request.model_dump())
    db.add(course_model)
    db.commit()
    db.refresh(course_model)  
    return course_model
    
@app.get("/course/{course_id}", status_code=status.HTTP_200_OK)
async def read_courses(db: db_dependency, course_id: UUID):
    course_model = db.query(Courses).filter(Courses.courses_id == course_id).first()
    if course_model is not None:
        return course_model
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Course not found.')

@app.put("/course/{course_id}")
async def update_course(db: db_dependency, course_request: CourseRequest, course_id: UUID):
    course_model = db.query(Courses).filter(Courses.courses_id == course_id).first()
    if course_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Course not found.')

    course_model.name = course_request.name
    course_model.description = course_request.description
    
    db.add(course_model)
    db.commit()
    db.refresh(course_model)  
    return course_model
    
@app.delete("/course/{course_id}", status_code=status.HTTP_200_OK)
async def delete_course(db: db_dependency, course_id: UUID):
    course_model = db.query(Courses).filter(Courses.courses_id == course_id).first()
    if course_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Course not found.')
    db.delete(course_model)
    db.commit()
    return {"detail": "Course deleted successfully"}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)