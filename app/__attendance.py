from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Path
from models import Enrollments, Students, Courses
from starlette import status
from database import SessionLocal
from schema import EnrollmentRequest

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/enrollment", operation_id="get_all_enrollments")
async def read_all(db: db_dependency):
    return db.query(Enrollments).all()

@app.post("/enrollment", status_code=status.HTTP_201_CREATED)
async def create_enrollment(db: db_dependency, enrollment_request: EnrollmentRequest):
    student = db.query(Students).filter(Students.students_id == enrollment_request.student_id_).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid student ID")
    
    course = db.query(Courses).filter(Courses.courses_id == enrollment_request.course_id_).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid course ID")
    
    enrollment_model = Enrollments(**enrollment_request.model_dump())
    db.add(enrollment_model)
    db.commit()
    db.refresh(enrollment_model)
    return enrollment_model
    
@app.get("/enrollment/{enrollment_id}", status_code=status.HTTP_200_OK)
async def read_enrollment(db: db_dependency, enrollment_id: int = Path(gt=0)):
    enrollment_model = db.query(Enrollments).filter(Enrollments.enrollments_id == enrollment_id).first()
    if enrollment_model is not None:
        return enrollment_model
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Enrollment not found.')

@app.put("/enrollment/{enrollment_id}")
async def update_enrollment(db: db_dependency, enrollment_request: EnrollmentRequest, enrollment_id: int = Path(gt=0)):
    enrollment_model = db.query(Enrollments).filter(Enrollments.enrollments_id == enrollment_id).first()
    if enrollment_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Enrollment not found.')

    enrollment_model.student_id_ = enrollment_request.student_id_
    enrollment_model.course_id_ = enrollment_request.course_id_
    
    db.add(enrollment_model)
    db.commit()
    db.refresh(enrollment_model)
    return enrollment_model
    
@app.delete("/enrollment/{enrollment_id}", status_code=status.HTTP_200_OK)
async def delete_enrollment(db: db_dependency, enrollment_id: int = Path(gt=0)):
    enrollment_model = db.query(Enrollments).filter(Enrollments.enrollments_id == enrollment_id).first()
    if enrollment_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Enrollment not found.')
    db.delete(enrollment_model)
    db.commit()
    return {"detail": "Enrollment deleted successfully"}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)