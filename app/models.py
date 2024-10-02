import sys
import os

# TodoApp directory ko path me add karte hain
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import Base
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime, Date, Text, Float, func
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Admins(Base):
    __tablename__ = "admins"
    
    admins_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True) 
    username = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    user_ = relationship('Users', back_populates='admin_')
    
    
class Users(Base):
    __tablename__ = "users"
    
    users_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=func.now())
    admin_id_ = Column(UUID(as_uuid=True), ForeignKey("admins.admins_id"), nullable=True)

    student_ = relationship('Students', back_populates='user_')
    admin_ = relationship('Admins', back_populates='user_')
    teacher_ = relationship('Teachers', back_populates='user_')
    
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
    
class Enrollments(Base):
    __tablename__ = "enrollments"
    
    enrollments_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    student_id_ = Column(UUID(as_uuid=True), ForeignKey("students.students_id"), nullable=False)
    course_id_ = Column(UUID(as_uuid=True), ForeignKey("courses.courses_id"), nullable=False)
    enrolled_at = Column(DateTime, default=func.now())
    
    student_ = relationship('Students', back_populates='enrollment_')
    course_ = relationship('Courses', back_populates='enrollment_')
    
class Attendance(Base):
    __tablename__ = "attendances"
    
    attendance_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    student_id_ = Column(UUID(as_uuid=True), ForeignKey('students.students_id'))
    class_id_ = Column(UUID(as_uuid=True), ForeignKey('classes.classes_id'))
    date = Column(Date, nullable=False)
    status = Column(String(10), nullable=False)  # 'Present' or 'Absent'
    
    student_ = relationship('Students', back_populates='attendance_')
    class_ = relationship('Classes', back_populates='attendance_')
    
class Teachers(Base):
    __tablename__ = "teachers"
    
    teachers_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    user_id_ = Column(UUID(as_uuid=True), ForeignKey("users.users_id"), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(15), nullable=False)
    department = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=func.now())

    user_ = relationship('Users', back_populates='teacher_')
    class_ = relationship('Classes', back_populates='teacher_')
    assignment_ = relationship('Assignments', back_populates='teacher_')
    
class Departments(Base):
    __tablename__ = "departments"
    
    departments_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=func.now())
    
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
    
class Subjects(Base):
    __tablename__ = "subjects"
    
    subjects_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    course_id_ = Column(UUID(as_uuid=True), ForeignKey("courses.courses_id"), nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    course_ = relationship('Courses', back_populates='subject_')

class Assignments(Base):
    __tablename__ = "assignments"
    
    assignments_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(DateTime, nullable=False)
    course_id_ = Column(UUID(as_uuid=True), ForeignKey("courses.courses_id"), nullable=False)
    teacher_id_ = Column(UUID(as_uuid=True), ForeignKey("teachers.teachers_id"), nullable=False)
    created_at = Column(DateTime, default=func.now())

    course_ = relationship('Courses', back_populates='assignment_')
    teacher_ = relationship('Teachers', back_populates='assignment_')
    submission_ = relationship('Submissions', back_populates='assignment_')

class Submissions(Base):
    __tablename__ = "submissions"
    
    submissions_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    assignment_id_ = Column(UUID(as_uuid=True), ForeignKey("assignments.assignments_id"), nullable=False)
    student_id_ = Column(UUID(as_uuid=True), ForeignKey("students.students_id"), nullable=False)
    submitted_at = Column(DateTime, default=func.now())
    grade = Column(String(2), nullable=True)
    
    assignment_ = relationship('Assignments', back_populates='submission_')
    
class Fees(Base):
    __tablename__ = "fees"
    
    fees_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    student_id_ = Column(UUID(as_uuid=True), ForeignKey("students.students_id"), nullable=False)
    amount_paid = Column(Float, nullable=False)
    paid_date = Column(DateTime, nullable=True)
    status = Column(String(10), nullable=False)
    created_at = Column(DateTime, default=func.now())

    student_ = relationship('Students', back_populates='fee_')
    
class Parents(Base):
    __tablename__ = "parents"
    
    parents_id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    student_id_ = Column(UUID(as_uuid=True), ForeignKey("students.students_id"), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(15), nullable=False)
    relation = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    student_ = relationship('Students', back_populates='parent_')