from typing import Annotated
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
from models import Fees, Students
from starlette import status
from database import SessionLocal
from schema import FeeRequest

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/fee", operation_id="get_all_fees")
async def read_all(db: db_dependency):
    return db.query(Fees).all()

@app.post("/fee", status_code=status.HTTP_201_CREATED)
async def create_fee(db: db_dependency, fee_request: FeeRequest):
    student = db.query(Students).filter(Students.students_id == fee_request.student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid student ID")
        
    fee_model = Fees(**fee_request.model_dump())
    db.add(fee_model)
    db.commit()
    db.refresh(fee_model)
    return fee_model
    
@app.get("/fee/{fee_id}", status_code=status.HTTP_200_OK)
async def read_fee(db: db_dependency, fee_id: UUID):
    fee_model = db.query(Fees).filter(Fees.fees_id == fee_id).first()
    if fee_model is not None:
        return fee_model
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Fee not found.')

@app.put("/fee/{fee_id}")
async def update_fee(db: db_dependency, fee_request: FeeRequest, fee_id: UUID):
    fee_model = db.query(Fees).filter(Fees.fees_id == fee_id).first()
    if fee_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Fee not found.')

    fee_model.student_id = fee_request.student_id
    fee_model.amount = fee_request.amount
    fee_model.status = fee_request.status
    fee_model.due_date = fee_request.due_date
    
    db.add(fee_model)
    db.commit()
    db.refresh(fee_model)
    return fee_model
    
@app.delete("/fee/{fee_id}", status_code=status.HTTP_200_OK)
async def delete_fee(db: db_dependency, fee_id: UUID):
    fee_model = db.query(Fees).filter(Fees.fees_id == fee_id).first()
    if fee_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Fee not found.')
    db.delete(fee_model)
    db.commit()
    return {"detail": "Fee deleted successfully"}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)