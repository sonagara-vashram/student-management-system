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

# Admins table - Manages roles of users
class Admins(Base):
    __tablename__ = "admins"
    
    admins_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now(), index=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), index=True)

    users = relationship('Users', back_populates='admin')

# Users table
class Users(Base):
    __tablename__ = "users"
    
    users_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), nullable=True)  
    created_at = Column(DateTime, default=func.now(), index=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), index=True)
    admin_id = Column(UUID(as_uuid=True), ForeignKey("admins.admins_id"), nullable=False)

    student = relationship('Students', back_populates='user')
    admin = relationship('Admins', back_populates='users') 
    teacher = relationship('Teachers', back_populates='user')
    parent = relationship('Parents', back_populates='user')
    notifications = relationship('Notifications', back_populates='user')

# Students table
class Students(Base):
    __tablename__ = "students"
    
    students_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.users_id"), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    dob = Column(Date, nullable=False)
    gender = Column(String(10), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(15), nullable=False)
    address = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=func.now(), index=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), index=True)

    user = relationship('Users', back_populates='student')
    enrollments = relationship('Enrollments', back_populates='student')
    attendances = relationship('Attendance', back_populates='student')
    fees = relationship('Fees', back_populates='student')
    parents = relationship('Parents', back_populates='student')
    submissions = relationship('Submissions', back_populates='student') 

# Teachers table
class Teachers(Base):
    __tablename__ = "teachers"
    
    teachers_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.users_id"), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(15), nullable=False)
    created_at = Column(DateTime, default=func.now(), index=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), index=True)
    
    user = relationship('Users', back_populates='teacher')
    classes = relationship('Classes', back_populates='teacher')
    assignments = relationship('Assignments', back_populates='teacher')
    subjects = relationship('Subjects', back_populates='teacher')  

# Parents Table
class Parents(Base):
    __tablename__ = "parents"
    
    parents_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.students_id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.users_id"), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(15), nullable=False)
    relation = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=func.now(), index=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), index=True)
    
    student = relationship('Students', back_populates='parents')
    user = relationship('Users', back_populates='parent')

# Enrollments Table
class Enrollments(Base):
    __tablename__ = "enrollments"
    
    enrollments_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.students_id"), nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.courses_id"), nullable=False)
    enrolled_at = Column(DateTime, default=func.now(), index=True)
    
    student = relationship('Students', back_populates='enrollments')
    course = relationship('Courses', back_populates='enrollments')

# Courses Table
class Courses(Base):
    __tablename__ = "courses"
    
    courses_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now(), index=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), index=True)

    classes = relationship('Classes', back_populates='course')
    enrollments = relationship('Enrollments', back_populates='course')
    subjects = relationship('Subjects', back_populates='course')
    assignments = relationship('Assignments', back_populates='course')

# Classes Table
class Classes(Base):
    __tablename__ = "classes"
    
    classes_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    name = Column(String(100), nullable=False)
    teacher_id = Column(UUID(as_uuid=True), ForeignKey("teachers.teachers_id"), nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.courses_id"), nullable=False)
    created_at = Column(DateTime, default=func.now(), index=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), index=True)

    course = relationship('Courses', back_populates='classes')
    teacher = relationship('Teachers', back_populates='classes')
    attendance = relationship('Attendance', back_populates='class_')
    subjects = relationship('Subjects', secondary='class_subject_link', back_populates='classes')

# Subjects Table
class Subjects(Base):
    __tablename__ = "subjects"
    
    subjects_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.courses_id"), nullable=False)
    teacher_id = Column(UUID(as_uuid=True), ForeignKey("teachers.teachers_id"), nullable=False)  
    created_at = Column(DateTime, default=func.now(), index=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), index=True)

    course = relationship('Courses', back_populates='subjects')
    teacher = relationship('Teachers', back_populates='subjects')
    classes = relationship('Classes', secondary='class_subject_link', back_populates='subjects')

class ClassSubjectLink(Base):
    __tablename__ = 'class_subject_link'
    class_id = Column(UUID(as_uuid=True), ForeignKey('classes.classes_id'), primary_key=True)
    subject_id = Column(UUID(as_uuid=True), ForeignKey('subjects.subjects_id'), primary_key=True)

# Notifications Table
class Notifications(Base):
    __tablename__ = "notifications"
    
    notifications_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.users_id"), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now(), index=True)

    user = relationship('Users', back_populates='notifications')

# Attendance Table
class Attendance(Base):
    __tablename__ = "attendances"
    
    attendance_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    student_id = Column(UUID(as_uuid=True), ForeignKey('students.students_id'))
    class_id = Column(UUID(as_uuid=True), ForeignKey('classes.classes_id'))
    date = Column(Date, nullable=False)
    status = Column(String(10), nullable=False)  # 'Present' or 'Absent'
    
    student = relationship('Students', back_populates='attendances')
    class_ = relationship('Classes', back_populates='attendance')

# Fees Table
class Fees(Base):
    __tablename__ = "fees"
    
    fees_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    student_id = Column(UUID(as_uuid=True), ForeignKey('students.students_id'), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String(20), nullable=False)  # 'Paid', 'Pending', etc.
    due_date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=func.now(), index=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), index=True)

    student = relationship('Students', back_populates='fees')

# Submissions Table
class Submissions(Base):
    __tablename__ = "submissions"
    
    submissions_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.students_id"), nullable=False)
    assignment_id = Column(UUID(as_uuid=True), ForeignKey("assignments.assignments_id"), nullable=False)
    submission_date = Column(DateTime, default=func.now(), index=True)
    grade = Column(Float, nullable=True)

    student = relationship('Students', back_populates='submissions')
    assignment = relationship('Assignments', back_populates='submissions')

# Assignments Table
class Assignments(Base):
    __tablename__ = "assignments"
    
    assignments_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.courses_id"), nullable=False)
    teacher_id = Column(UUID(as_uuid=True), ForeignKey("teachers.teachers_id"), nullable=False)
    created_at = Column(DateTime, default=func.now(), index=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), index=True)

    teacher = relationship('Teachers', back_populates='assignments')
    course = relationship('Courses', back_populates='assignments')
    submissions = relationship('Submissions', back_populates='assignment')