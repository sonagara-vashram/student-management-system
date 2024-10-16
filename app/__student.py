from typing import Annotated
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
from models import RoleEnum, Students, Users
from starlette import status
from database import SessionLocal
from schema import StudentRequest

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/student", operation_id="get_all_students")
async def read_all(db: db_dependency):
    return db.query(Students).all()

@app.post("/student", status_code=status.HTTP_201_CREATED)
async def create_student(db: db_dependency, std_request: StudentRequest):
    user = db.query(Users).filter(Users.users_id == std_request.user_id).first()
    if user is None or user.role != RoleEnum.STUDENT:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid user ID. User must be a student.')
    
    existing_student = db.query(Students).filter(Students.user_id == std_request.user_id).first()
    if existing_student:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student already exists for this user.")

    std_model = Students(**std_request.model_dump())
    db.add(std_model)
    db.commit()
    db.refresh(std_model)
    return std_model
    
@app.get("/student/{student_id}", status_code=status.HTTP_200_OK)
async def read_students(db: db_dependency, student_id: UUID):
    std_model = db.query(Students).filter(Students.students_id == student_id).first()
    if std_model is not None:
        return std_model
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Student not found.')

@app.put("/student/{student_id}")
async def update_student(db: db_dependency, std_request: StudentRequest, student_id: UUID):
    std_model = db.query(Students).filter(Students.students_id == student_id).first()
    if std_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Student not found.')

    std_model.user_id = std_request.user_id
    std_model.first_name = std_request.first_name
    std_model.last_name = std_request.last_name
    std_model.dob = std_request.dob
    std_model.gender = std_request.gender
    std_model.email = std_request.email
    std_model.phone = std_request.phone
    std_model.address = std_request.address
    
    db.add(std_model)
    db.commit()
    db.refresh(std_model)
    return std_model
    
@app.delete("/student/{student_id}", status_code=status.HTTP_200_OK)
async def delete_student(db: db_dependency, student_id: UUID):
    std_model = db.query(Students).filter(Students.students_id == student_id).first()
    if std_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Student not found.')
    db.delete(std_model)
    db.commit()
    return {"detail": "Student deleted successfully"}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)