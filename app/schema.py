from typing import Annotated
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field, EmailStr
from starlette import status
from database import SessionLocal
from datetime import date, datetime

class AdminRequest(BaseModel):
    username: str = Field(min_length=2, max_length=50, description="Username must be between 2 and 50 characters")
    email: EmailStr = Field(description="Valid email address")
    hashed_password: str = Field(min_length=8, max_length=255, description="Password must be between 8 and 255 characters")
    created_at: date = Field(default_factory=date.today, description="Creation date")
    updated_at: date = Field(default_factory=date.today, description="Last update date")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "adminuser",
                "email": "admin@example.com",
                "hashed_password": "hashedpassword123",
                "created_at": "2023-01-01",
                "updated_at": "2023-01-01"
            }
        }
        
class UserRequest(BaseModel):
    admin_id: UUID  # Correct type for UUID
    username: str = Field(min_length=3, max_length=50, description="Username must be between 3 and 50 characters")
    email: EmailStr = Field(description="Valid email address")
    hashed_password: str = Field(min_length=8, max_length=255, description="Password must be between 8 and 255 characters")
    role: str = Field(min_length=3, max_length=20, description="Role must be between 3 and 20 characters")
    created_at: date = Field(default_factory=date.today, description="Creation date")

    class Config:
        json_schema_extra = {
            "example": {
                "admin_id": "d4a1a0b1-114c-4268-9e67-091af22dbc16",  # Example UUID
                "username": "user123",
                "email": "user@example.com",
                "hashed_password": "hashedpassword123",
                "role": "user",
                "created_at": "2023-01-01"
            }
        }
        
class StudentRequest(BaseModel):
    user_id_: UUID  # Add user_id_ field
    first_name: str = Field(min_length=2, max_length=50, description="First name must be between 2 and 50 characters")
    last_name: str = Field(min_length=2, max_length=50, description="Last name must be between 2 and 50 characters")
    dob: date = Field(description="Date of birth in YYYY-MM-DD format")
    gender: str = Field(min_length=1, max_length=10, description="Gender must be between 1 and 10 characters")
    email: EmailStr = Field(description="Valid email address")
    phone: str = Field(min_length=10, max_length=15, description="Phone number must be between 10 and 15 characters")
    address: str = Field(max_length=255, description="Address must be up to 255 characters")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id_": "d4a1a0b1-114c-4268-9e67-091af22dbc16",  # Example UUID
                "first_name": "John",
                "last_name": "Doe",
                "dob": "2000-01-01",
                "gender": "Male",
                "email": "john.doe@example.com",
                "phone": "1234567890",
                "address": "123 Main St, Anytown, USA"
            }
        }

class CourseRequest(BaseModel):
    name: str = Field(min_length=2, max_length=50, description="Name must be between 2 and 50 characters")
    description: str = Field(min_length=2, max_length=255, description="Description must be between 2 and 255 characters")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Math",
                "description": "Introduction to mathematics"
            }
        }
        
class EnrollmentRequest(BaseModel):
    student_id_: UUID
    course_id_: UUID
    
    class Config:
        json_schema_extra = {
            "example": {
                "student_id_": "d4a1a0b1-114c-4268-9e67-091af22dbc16", 
                "course_id_": "d4a1a0b1-114c-4268-9e67-091af22dbc16", 
            }
        }