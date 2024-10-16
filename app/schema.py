from uuid import UUID
from pydantic import BaseModel, Field, EmailStr
from datetime import date, datetime

class AdminRequest(BaseModel):
    username: str = Field(min_length=2, max_length=50, description="Username must be between 2 and 50 characters")
    email: EmailStr = Field(description="Valid email address")
    hashed_password: str = Field(min_length=8, max_length=255, description="Password must be between 8 and 255 characters")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "adminuser",
                "email": "admin@example.com",
                "hashed_password": "hashedpassword123",
            }
        }
        
class UserRequest(BaseModel):
    admin_id: UUID  
    username: str = Field(min_length=3, max_length=50, description="Username must be between 3 and 50 characters")
    email: EmailStr = Field(description="Valid email address")
    hashed_password: str = Field(min_length=8, max_length=255, description="Password must be between 8 and 255 characters")
    role: str = Field(description="Role must be one of the following: 'Admin', 'User', or 'Teacher'")
    class Config:
        json_schema_extra = {
            "example": {
                "admin_id": "9f2239c3-5218-49b9-9087-d85e0520df9b",
                "email": "jon@gmail.com",
                "hashed_password": "jingoes0102",
                "role": "teacher", 
                "username": "jon0106"
            }
        }
        
class StudentRequest(BaseModel):
    user_id: UUID
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
                "user_id": "d4a1a0b1-114c-4268-9e67-091af22dbc16",  
                "first_name": "John",
                "last_name": "Doe",
                "dob": "2000-01-01",
                "gender": "Male",
                "email": "john.doe@example.com",
                "phone": "1234567890",
                "address": "123 Main St, Anytown, USA"
            }
        }
        
class ParentsRequest(BaseModel):
    user_id: UUID
    student_id: UUID
    first_name: str = Field(min_length=2, max_length=50, description="First name must be between 2 and 50 characters")
    last_name: str = Field(min_length=2, max_length=50, description="Last name must be between 2 and 50 characters")
    email: EmailStr = Field(description="Valid email address")
    phone: str = Field(min_length=10, max_length=15, description="Phone number must be between 10 and 15 characters")
    relation: str = Field(min_length=2, max_length=50, description="Relation must be between 2 and 50 characters")

    class Config:
        schema_extra = {
            "example": {
                "user_id": "d4a1a0b1-114c-4268-9e67-091af22dbc16", 
                "student_id": "a702a426-b019-4497-be30-9c75bb5d8665", 
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "phone": "1234567890",
                "relation": "Father"
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
    student_id: UUID
    course_id: UUID
    
    class Config:
        json_schema_extra = {
            "example": {
                "student_id": "d4a1a0b1-114c-4268-9e67-091af22dbc16", 
                "course_id": "d4a1a0b1-114c-4268-9e67-091af22dbc16", 
            }
        }

        
        
class TeacherRequest(BaseModel):
    user_id: UUID
    first_name: str = Field(min_length=2, max_length=50, description="First name must be between 2 and 50 characters")
    last_name: str = Field(min_length=2, max_length=50, description="Last name must be between 2 and 50 characters")
    email: EmailStr = Field(description="Valid email address")
    phone: str = Field(min_length=10, max_length=15, description="Phone number must be between 10 and 15 characters")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "d4a1a0b1-114c-4268-9e67-091af22dbc16",  # Example UUID
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "phone": "1234567890",
            }
        }
        
class ClassRequest(BaseModel):
    name: str = Field(min_length=2, max_length=50, description="First name must be between 2 and 50 characters")
    teacher_id: UUID
    course_id: UUID
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "101",
                "teacher_id": "d4a1a0b1-114c-4268-9e67-091af22dbc16",
                "course_id": "d4a1a0b1-114c-4268-9e67-091af22dbc16"
            }
        }
        
class SubjectRequest(BaseModel):
    name: str = Field(min_length=2, max_length=50, description="Name must be between 2 and 50 characters")
    description: str = Field(min_length=2, max_length=255, description="Description must be between 2 and 255 characters")
    course_id: UUID
    teacher_id: UUID
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Math",
                "description": "Introduction to mathematics",
                "course_id": "d4a1a0b1-114c-4268-9e67-091af22dbc16",
                "teacher_id": "d4a1a0b1-114c-4268-9e67-091af22dbc16"
            }
        }
    
class NotificationRequest(BaseModel):
    user_id: UUID
    message: str = Field(min_length=2, max_length=255, description="Message must be between 2 and 255 characters")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "d4a1a0b1-114c-4268-9e67-091af22dbc16", 
                "message": "message!"
            }
        }
    
#! pending..!
class AttendanceRequest(BaseModel):
    student_id_: UUID
    class_id_: UUID
    date: datetime = Field(default_factory=date.today, description="Date of attendance in YYYY-MM-DD format")
    status: str = Field(min_length=2, max_length=10, description="Status must be between 2 and 10 characters")
    
    class Config:
        json_schema_extra = {
            "example": {
                "student_id_": "d4a1a0b1-114c-4268-9e67-091af22dbc16", 
                "class_id_": "d4a1a0b1-114c-4268-9e67-091af22dbc16", 
                "date": "2001-02-15", 
                "status": "present", 
            }
        }
        
class FeeRequest(BaseModel):
    student_id: UUID
    amount: float = Field(gt=0, description="Amount must be greater than 0")
    status: str = Field(min_length=2, max_length=10, description="Status must be between 2 and 10 characters")
    due_date: str = Field(min_length=2, max_length=10, description="Due date in YYYY-MM-DD format")
    
    class Config:
        json_schema_extra = {
            "example": {
                "student_id": "d4a1a0b1-114c-4268-9e67-091af22dbc16",
                "amount": 100.0,
                "status": "pending",
                "due_date": "2022-01-31",
            }
        }