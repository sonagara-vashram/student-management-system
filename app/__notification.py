from typing import Annotated
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
from models import Notifications, Users
from starlette import status
from database import SessionLocal
from schema import NotificationRequest

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/notification", operation_id="get_notifications")
async def read_all(db: db_dependency):
    return db.query(Notifications).all()

@app.post("/notification", status_code=status.HTTP_201_CREATED)
async def create_notification(db: db_dependency, notification_request: NotificationRequest):
    user = db.query(Users).filter(Users.users_id == notification_request.user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid user ID.')
    notification_model = Notifications(**notification_request.model_dump())
    db.add(notification_model)
    db.commit()
    db.refresh(notification_model)  
    return notification_model
    
@app.get("/notification/{notification_id}", status_code=status.HTTP_200_OK)
async def read_notification(db: db_dependency, notification_id: UUID):
    notification_model = db.query(Notifications).filter(Notifications.notifications_id == notification_id).first()
    if notification_model is not None:
        return notification_model
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Notification not found.')

@app.put("/notification/{notification_id}")
async def update_notification(db: db_dependency, notification_request: NotificationRequest, notification_id: UUID):
    notification_model = db.query(Notifications).filter(Notifications.courses_id == notification_id).first()
    if notification_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Notification not found.')

    notification_model.user_id = notification_request.user_id
    notification_model.message = notification_request.message
    
    db.add(notification_model)
    db.commit()
    db.refresh(notification_model)  
    return notification_model
    
@app.delete("/notification/{notification_id}", status_code=status.HTTP_200_OK)
async def delete_notification(db: db_dependency, notification_id: UUID):
    notification_model = db.query(Notifications).filter(Notifications.courses_id == notification_id).first()
    if notification_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Notification not found.')
    db.delete(notification_model)
    db.commit()
    return {"detail": "Course deleted successfully"}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)