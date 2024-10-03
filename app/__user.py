from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Path
from models import Users, Admins
from pydantic import BaseModel
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

@app.get("/user", operation_id="get_all_users")
async def read_all(db: db_dependency):
    return db.query(Users).all()

@app.post("/user", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user_request: UserRequest):
    admin = db.query(Admins).filter(Admins.admins_id == user_request.admin_id).first()
    
    if not admin:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid admin ID")
    
    user_model = Users(
        admin_id_=admin.admins_id,  
        username=user_request.username,
        email=user_request.email,
        hashed_password=user_request.hashed_password,
        role=user_request.role,
        created_at=user_request.created_at
    )
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return user_model

@app.get("/user/{user_id}", status_code=status.HTTP_200_OK)
async def read_user(db: db_dependency, user_id: int = Path(gt=0)):
    user_model = db.query(Users).filter(Users.users_id == user_id).first()
    if user_model is not None:
        return user_model
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')

@app.put("/user/{user_id}")
async def update_user(db: db_dependency, user_request: UserRequest, user_id: int = Path(gt=0)):
    user_model = db.query(Users).filter(Users.users_id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')

    # Validate the admin_id
    admin = db.query(Admins).filter(Admins.admins_id == user_request.admin_id).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid admin ID")

    user_model.admin_id_ = admin.admins_id 
    user_model.username = user_request.username
    user_model.email = user_request.email
    user_model.hashed_password = user_request.hashed_password
    user_model.role = user_request.role
    user_model.created_at = user_request.created_at

    db.add(user_model)
    db.commit()
    return {'detail': 'user update successfullly.'}

@app.delete("/user/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(db: db_dependency, user_id: int = Path(gt=0)):
    user_model = db.query(Users).filter(Users.users_id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')
    
    db.delete(user_model)
    db.commit()
    return {"detail": "User deleted successfully."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)