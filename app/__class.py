from typing import Annotated
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
from models import Classes, Courses, Teachers
from starlette import status
from database import SessionLocal
from schema import ClassRequest

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/class", operation_id="get_all_classes")
async def read_all(db: db_dependency):
    return db.query(Classes).all()

@app.post("/class", status_code=status.HTTP_201_CREATED)
async def create_class(db: db_dependency, class_request: ClassRequest):
    teacher = db.query(Teachers).filter(Teachers.teachers_id == class_request.teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid teacher ID")
    
    course = db.query(Courses).filter(Courses.courses_id == class_request.course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid course ID")
            
    class_model = Teachers(**class_request.model_dump())
    db.add(class_model)
    db.commit()
    db.refresh(class_model)
    return class_model
    
@app.get("/class/{class_id}", status_code=status.HTTP_200_OK)
async def read_class(db: db_dependency, class_id: UUID):
    class_model = db.query(Classes).filter(Classes.classes_id == class_id).first()
    if class_model is not None:
        return class_model
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Class not found.')

@app.put("/class/{class_id}")
async def update_class(db: db_dependency, class_request: ClassRequest, class_id: UUID):
    class_model = db.query(Classes).filter(Classes.classes_id == class_id).first()
    if class_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Class not found.')

    class_model.teacher_id = class_request.teacher_id
    class_model.name = class_request.name
    class_model.course_id = class_request.course_id
    
    db.add(class_model)
    db.commit()
    db.refresh(class_model)
    return class_model
    
@app.delete("/class/{class_id}", status_code=status.HTTP_200_OK)
async def delete_class(db: db_dependency, class_id: UUID):
    class_model = db.query(Classes).filter(Classes.teacher_id == class_id).first()
    if class_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Class not found.')
    db.delete(class_model)
    db.commit()
    return {"detail": "Class deleted successfully"}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)