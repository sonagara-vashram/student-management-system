from typing import Annotated
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Path
from models import Subjects, Students, Courses, Teachers
from starlette import status
from database import SessionLocal
from schema import SubjectRequest

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/subject", operation_id="get_all_subjects")
async def read_all(db: db_dependency):
    return db.query(Subjects).all()

@app.post("/subject", status_code=status.HTTP_201_CREATED)
async def create_subject(db: db_dependency, subject_request: SubjectRequest):
    teacher = db.query(Teachers).filter(Teachers.teachers_id == subject_request.teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid teacher ID")
    
    course = db.query(Courses).filter(Courses.courses_id == subject_request.course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid course ID")
            
    subject_model = Subjects(**subject_request.model_dump())
    db.add(subject_model)
    db.commit()
    db.refresh(subject_model)
    return subject_model
    
@app.get("/subject/{subject_id}", status_code=status.HTTP_200_OK)
async def read_subject(db: db_dependency, subject_id: UUID):
    subject_model = db.query(Subjects).filter(Subjects.subjects_id == subject_id).first()
    if subject_model is not None:
        return subject_model
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Subject not found.')

@app.put("/subject/{subject_id}")
async def update_subject(db: db_dependency, subject_request: SubjectRequest, subject_id: UUID):
    subject_model = db.query(Subjects).filter(Subjects.subjects_id == subject_id).first()
    if subject_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Subject not found.')

    subject_model.teacher_id = subject_request.teacher_id
    subject_model.name = subject_request.name
    subject_model.description = subject_request.description
    subject_model.course_id = subject_request.course_id
    
    db.add(subject_model)
    db.commit()
    db.refresh(subject_model)
    return subject_model
    
@app.delete("/subject/{subject_id}", status_code=status.HTTP_200_OK)
async def delete_subject(db: db_dependency, subject_id: UUID):
    subject_model = db.query(Subjects).filter(Subjects.subjects_id == subject_id).first()
    if subject_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Subject not found.')
    db.delete(subject_model)
    db.commit()
    return {"detail": "Enrollment deleted successfully"}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)