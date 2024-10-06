import enum
from typing import Annotated
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Path
from models import Users, Admins, RoleEnum
from schema import UserRequest
from starlette import status
from database import SessionLocal

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def is_valid_role(role):
    formatted_role = role.lower()     
    for roles in RoleEnum:
        if roles.value == formatted_role:
            return roles.name 
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role value")

@app.get("/user", operation_id="get_all_users")
async def read_all(db: db_dependency):
    return db.query(Users).all()

@app.post("/user", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user_request: UserRequest):
    admin = db.query(Admins).filter(Admins.admins_id == user_request.admin_id).first() 
    
    if not admin:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid admin ID")
    
    role = user_request.role
    role = is_valid_role(role)
    
    user_model = Users(
        admin_id=admin.admins_id,  
        username=user_request.username,
        email=user_request.email,
        hashed_password=user_request.hashed_password,
        role=role
    )

    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return user_model

@app.get("/user/{user_id}", status_code=status.HTTP_200_OK)
async def read_user(db: db_dependency, user_id: UUID):
    user_model = db.query(Users).filter(Users.users_id == user_id).first()
    if user_model is not None:
        return user_model
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')

@app.put("/user/{user_id}")
async def update_user(db: db_dependency, user_request: UserRequest, user_id: UUID):
    user_model = db.query(Users).filter(Users.users_id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')

    # Validate the admin_id
    admin = db.query(Admins).filter(Admins.admins_id == user_request.admin_id).first()  # Use admin_id
    if not admin:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid admin ID")

    # Ensure the role matches the RoleEnum values
    role = user_request.role
    roles = is_valid_role(role)

    user_model.admin_id = admin.admins_id 
    user_model.username = user_request.username
    user_model.email = user_request.email
    user_model.hashed_password = user_request.hashed_password
    user_model.role = roles

    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return {'detail': 'User updated successfully.'}

@app.delete("/user/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(db: db_dependency, user_id: UUID):
    user_model = db.query(Users).filter(Users.users_id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')
    
    db.delete(user_model)
    db.commit()
    return {"detail": "User deleted successfully."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)