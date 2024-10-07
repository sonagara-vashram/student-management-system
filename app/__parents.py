from typing import Annotated
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Path
from models import RoleEnum, Parents, Users, Students
from starlette import status
from database import SessionLocal
from schema import ParentsRequest

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/parents", operation_id="get_all_parents")
async def read_all(db: db_dependency):
    return db.query(Parents).all()

@app.post("/parents", status_code=status.HTTP_201_CREATED)
async def create_parents(db: db_dependency, parent_request: ParentsRequest):
    user = db.query(Users).filter(Users.users_id == parent_request.user_id).first()
    if user is None or user.role != RoleEnum.PARENT:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid user ID. User must be a parent.')
    
    student = db.query(Students).filter(Students.students_id == parent_request.student_id).first()
    if student is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid student ID.')
    
    existing_user_parents = db.query(Parents).filter(Parents.user_id == parent_request.user_id).first()
    if existing_user_parents:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Parent already exists for this user.")
    
    existing_student_parents = db.query(Parents).filter(Parents.student_id == parent_request.student_id).first()
    if existing_student_parents:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Parent already exists for this student.")

    parent_model = Parents(**parent_request.model_dump())
    db.add(parent_model)
    db.commit()
    db.refresh(parent_model)
    return parent_model
    
@app.get("/parents/{parent_id}", status_code=status.HTTP_200_OK)
async def read_parents(db: db_dependency, parent_id: UUID):
    parent_model = db.query(Parents).filter(Parents.parents_id == parent_id).first()
    if parent_model is not None:
        return parent_model
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Parents not found.')

@app.put("/parents/{parent_id}")
async def update_parents(db: db_dependency, parent_request: ParentsRequest, parent_id: UUID):
    parent_model = db.query(Parents).filter(Parents.parents_id == parent_id).first()
    if parent_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Parents not found.')

    parent_model.user_id = parent_request.user_id
    parent_model.student_id = parent_request.student_id
    parent_model.first_name = parent_request.first_name
    parent_model.last_name = parent_request.last_name
    parent_model.email = parent_request.email
    parent_model.phone = parent_request.phone
    parent_model.relation = parent_request.relation
    
    db.add(parent_model)
    db.commit()
    db.refresh(parent_model)
    return parent_model
    
@app.delete("/parents/{parent_id}", status_code=status.HTTP_200_OK)
async def delete_parents(db: db_dependency, parent_id: UUID):
    parent_model = db.query(Parents).filter(Parents.parents_id == parent_id).first()
    if parent_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Student not found.')
    db.delete(parent_model)
    db.commit()
    return {"detail": "Parents deleted successfully"}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)