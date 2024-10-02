from typing import Annotated
import uuid
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Path
from models import Admins
from starlette import status
from database import SessionLocal
from schema import AdminRequest

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/admin", operation_id="get_admin")
async def read_all(db: db_dependency):
    return db.query(Admins).all()

@app.post("/admin", status_code=status.HTTP_201_CREATED)
async def create_admin(db: db_dependency, admin_request: AdminRequest):
    admin_model = Admins(**admin_request.model_dump())
    db.add(admin_model)
    db.commit()
    
@app.get("/admin/{admin_id}", status_code=status.HTTP_200_OK)
async def read_admins(db: db_dependency, admin_id: int = Path(gt=0)):
    admin_model = db.query(Admins).filter(Admins.admins_id == admin_id).first()
    if admin_model is not None:
        return admin_model
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Admin not found.')

@app.put("/admin/{admin_id}")
async def update_admin(db: db_dependency, admin_request: AdminRequest, admin_id: int = Path(gt=0)):
    admin_model = db.query(Admins).filter(Admins.admins_id == admin_id).first()
    if admin_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Admin not found.')

    admin_model.username = admin_request.username
    admin_model.hashed_password = admin_request.hashed_password
    admin_model.created_at = admin_request.created_at
    admin_model.email = admin_request.email
    admin_model.updated_at = admin_request.updated_at
    
    db.add(admin_model)
    db.commit()
    
@app.delete("/admin/{admin_id}", status_code=status.HTTP_200_OK)
async def delete_admin(db: db_dependency, admin_id):
    admin_model = db.query(Admins).filter(Admins.admins_id == admin_id)
    if admin_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found.')
    db.query(Admins).filter(Admins.admins_id == admin_id).delete()
    db.commit()
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)