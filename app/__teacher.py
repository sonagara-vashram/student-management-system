from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Path
from models import Teachers, Users
from starlette import status
from database import SessionLocal
from schema import TeacherRequest

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/teacher", operation_id="get_all_teachers")
async def read_all(db: db_dependency):
    return db.query(Teachers).all()

@app.post("/teacher", status_code=status.HTTP_201_CREATED)
async def create_teacher(db: db_dependency, teacher_request: TeacherRequest):
    user = db.query(Users).filter(Users.users_id == teacher_request.user_id_).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found.")
    
    # Check if the user is designated as a teacher
    if user.role != 'teacher':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not designated as a teacher.")
    
    # Check if a teacher with the same email already exists
    existing_teacher = db.query(Teachers).filter(Teachers.email == teacher_request.email).first()
    if existing_teacher:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Teacher with this email already exists.")
    
    teacher_model = Teachers(**teacher_request.dict())
    db.add(teacher_model)
    db.commit()
    db.refresh(teacher_model)
    return teacher_model
    
@app.get("/teacher/{teacher_id}", status_code=status.HTTP_200_OK)
async def read_teacher(db: db_dependency, teacher_id: int = Path(gt=0)):
    teacher_model = db.query(Teachers).filter(Teachers.teachers_id == teacher_id).first()
    if teacher_model is not None:
        return teacher_model
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Teacher not found.')

@app.put("/teacher/{teacher_id}")
async def update_teacher(db: db_dependency, teacher_request: TeacherRequest, teacher_id: int = Path(gt=0)):
    teacher_model = db.query(Teachers).filter(Teachers.teachers_id == teacher_id).first()
    if teacher_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Teacher not found.')

    teacher_model.user_id_ = teacher_request.user_id_
    teacher_model.first_name = teacher_request.first_name
    teacher_model.last_name = teacher_request.last_name
    teacher_model.email = teacher_request.email
    teacher_model.phone = teacher_request.phone
    teacher_model.department = teacher_request.department
    
    db.add(teacher_model)
    db.commit()
    db.refresh(teacher_model)
    return teacher_model
    
@app.delete("/teacher/{teacher_id}", status_code=status.HTTP_200_OK)
async def delete_teacher(db: db_dependency, teacher_id: int = Path(gt=0)):
    teacher_model = db.query(Teachers).filter(Teachers.teachers_id == teacher_id).first()
    if teacher_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Teacher not found.')
    db.delete(teacher_model)
    db.commit()
    return {"detail": "Teacher deleted successfully"}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)