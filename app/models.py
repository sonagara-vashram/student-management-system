import sys
import os
from sqlalchemy import Column, String, ForeignKey, DateTime, Date, Text, Float, func, Enum
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.dialects.postgresql import UUID
import enum
from database import Base

# Role Enum for User Roles
class RoleEnum(enum.Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    PARENT = "parent"

# Admin table - Main table to manage other roles
class Admins(Base):
    __tablename__ = "admins"
    
    admins_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    users_ = relationship('Users', back_populates='admin_')

class Users(Base):
    __tablename__ = "users"
    
    users_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum))   
    created_at = Column(DateTime, default=func.now())
    admin_id_ = Column(UUID(as_uuid=True), ForeignKey("admins.admins_id"), nullable=False)  # Every user is managed by an admin
    
    student_ = relationship('Students', back_populates='user_')
    admin_ = relationship('Admins', back_populates='users_') 
    teacher_ = relationship('Teachers', back_populates='user_')
    parent_ = relationship('Parents', back_populates='user_')
    notification_ = relationship('Notifications', back_populates='user_')

# Students table
class Students(Base):
    __tablename__ = "students"
    
    students_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    user_id_ = Column(UUID(as_uuid=True), ForeignKey("users.users_id"), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    dob = Column(Date, nullable=False)
    gender = Column(String(10), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(15), nullable=False)
    address = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=func.now())

    user_ = relationship('Users', back_populates='student_')
    enrollment_ = relationship('Enrollments', back_populates='student_')
    attendance_ = relationship('Attendance', back_populates='student_')
    fee_ = relationship('Fees', back_populates='student_')
    parent_ = relationship('Parents', back_populates='student_')
    submission_ = relationship('Submissions', back_populates='student_') 

# Teachers table
class Teachers(Base):
    __tablename__ = "teachers"
    
    teachers_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    user_id_ = Column(UUID(as_uuid=True), ForeignKey("users.users_id"), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(15), nullable=False)
    created_at = Column(DateTime, default=func.now())

    user_ = relationship('Users', back_populates='teacher_')
    class_ = relationship('Classes', back_populates='teacher_')
    assignment_ = relationship('Assignments', back_populates='teacher_')
    subject_ = relationship('Subjects', back_populates='teacher_')  # Ensure this line is present

# Parents Table
class Parents(Base):
    __tablename__ = "parents"
    
    parents_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    student_id_ = Column(UUID(as_uuid=True), ForeignKey("students.students_id"), nullable=False)
    user_id_ = Column(UUID(as_uuid=True), ForeignKey("users.users_id"), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(15), nullable=False)
    relation = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    student_ = relationship('Students', back_populates='parent_')
    user_ = relationship('Users', back_populates='parent_')

# Enrollments Table
class Enrollments(Base):
    __tablename__ = "enrollments"
    
    enrollments_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    student_id_ = Column(UUID(as_uuid=True), ForeignKey("students.students_id"), nullable=False)
    course_id_ = Column(UUID(as_uuid=True), ForeignKey("courses.courses_id"), nullable=False)
    enrolled_at = Column(DateTime, default=func.now())
    
    student_ = relationship('Students', back_populates='enrollment_')
    course_ = relationship('Courses', back_populates='enrollment_')

# Courses Table
class Courses(Base):
    __tablename__ = "courses"
    
    courses_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())

    class_ = relationship('Classes', back_populates='course_')
    enrollment_ = relationship('Enrollments', back_populates='course_')
    subject_ = relationship('Subjects', back_populates='course_')
    assignment_ = relationship('Assignments', back_populates='course_')

# Classes Table
class Classes(Base):
    __tablename__ = "classes"
    
    classes_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    name = Column(String(100), nullable=False)
    teacher_id_ = Column(UUID(as_uuid=True), ForeignKey("teachers.teachers_id"), nullable=False)
    course_id_ = Column(UUID(as_uuid=True), ForeignKey("courses.courses_id"), nullable=False)
    created_at = Column(DateTime, default=func.now())

    course_ = relationship('Courses', back_populates='class_')
    teacher_ = relationship('Teachers', back_populates='class_')
    attendance_ = relationship('Attendance', back_populates='class_')
    subject_ = relationship('Subjects', secondary='class_subject_link', back_populates='class_')

# Subjects Table
class Subjects(Base):
    __tablename__ = "subjects"
    
    subjects_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    course_id_ = Column(UUID(as_uuid=True), ForeignKey("courses.courses_id"), nullable=False)
    teacher_id_ = Column(UUID(as_uuid=True), ForeignKey("teachers.teachers_id"), nullable=False)  
    created_at = Column(DateTime, default=func.now())

    course_ = relationship('Courses', back_populates='subject_')
    teacher_ = relationship('Teachers', back_populates='subject_')
    class_ = relationship('Classes', secondary='class_subject_link', back_populates='subject_')

class ClassSubjectLink(Base):
    __tablename__ = 'class_subject_link'
    class_id = Column(UUID(as_uuid=True), ForeignKey('classes.classes_id'), primary_key=True)
    subject_id = Column(UUID(as_uuid=True), ForeignKey('subjects.subjects_id'), primary_key=True)

# Notifications Table
class Notifications(Base):
    __tablename__ = "notifications"
    
    notifications_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    user_id_ = Column(UUID(as_uuid=True), ForeignKey("users.users_id"), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())

    user_ = relationship('Users', back_populates='notification_')

# Attendance Table
class Attendance(Base):
    __tablename__ = "attendances"
    
    attendance_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    student_id_ = Column(UUID(as_uuid=True), ForeignKey('students.students_id'))
    class_id_ = Column(UUID(as_uuid=True), ForeignKey('classes.classes_id'))
    date = Column(Date, nullable=False)
    status = Column(String(10), nullable=False)  # 'Present' or 'Absent'
    
    student_ = relationship('Students', back_populates='attendance_')
    class_ = relationship('Classes', back_populates='attendance_')

# Fees Table
class Fees(Base):
    __tablename__ = "fees"
    
    fees_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    student_id_ = Column(UUID(as_uuid=True), ForeignKey('students.students_id'), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String(20), nullable=False)  # 'Paid', 'Pending', etc.
    due_date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=func.now())

    student_ = relationship('Students', back_populates='fee_')

# Submissions Table
class Submissions(Base):
    __tablename__ = "submissions"
    
    submissions_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    student_id_ = Column(UUID(as_uuid=True), ForeignKey("students.students_id"), nullable=False)
    assignment_id_ = Column(UUID(as_uuid=True), ForeignKey("assignments.assignments_id"), nullable=False)
    submission_date = Column(DateTime, default=func.now())
    grade = Column(Float, nullable=True)

    student_ = relationship('Students', back_populates='submission_')
    assignment_ = relationship('Assignments', back_populates='submission_')

# Assignments Table
class Assignments(Base):
    __tablename__ = "assignments"
    
    assignments_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    course_id_ = Column(UUID(as_uuid=True), ForeignKey("courses.courses_id"), nullable=False)
    teacher_id_ = Column(UUID(as_uuid=True), ForeignKey("teachers.teachers_id"), nullable=False)
    created_at = Column(DateTime, default=func.now())

    teacher_ = relationship('Teachers', back_populates='assignment_')
    course_ = relationship('Courses', back_populates='assignment_')
    submission_ = relationship('Submissions', back_populates='assignment_')
