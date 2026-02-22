from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Time
from sqlalchemy.orm import relationship
from database import Base

class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    courses = relationship("Course", back_populates="department")
    faculties = relationship("Faculty", back_populates="department")

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    department_id = Column(Integer, ForeignKey("departments.id"))
    
    department = relationship("Department", back_populates="courses")
    semesters = relationship("Semester", back_populates="course")

class Semester(Base):
    __tablename__ = "semesters"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String) # e.g., "Fall 2024" or "Semester 1"
    course_id = Column(Integer, ForeignKey("courses.id"))
    
    course = relationship("Course", back_populates="semesters")
    subjects = relationship("Subject", back_populates="semester")

class Faculty(Base):
    __tablename__ = "faculties"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    department_id = Column(Integer, ForeignKey("departments.id"))
    max_hours_per_week = Column(Integer, default=40)
    
    department = relationship("Department", back_populates="faculties")
    subjects = relationship("Subject", back_populates="faculty")

class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    code = Column(String, index=True)
    credit_hours = Column(Integer)
    weekly_frequency = Column(Integer)
    semester_id = Column(Integer, ForeignKey("semesters.id"))
    faculty_id = Column(Integer, ForeignKey("faculties.id"), nullable=True) # Assigned faculty
    
    semester = relationship("Semester", back_populates="subjects")
    faculty = relationship("Faculty", back_populates="subjects")

class Classroom(Base):
    __tablename__ = "classrooms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    capacity = Column(Integer)
    room_type = Column(String) # e.g., "Lecture", "Lab"

class Timetable(Base):
    __tablename__ = "timetables"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(String) # simple ISO format string
    fitness_score = Column(Float)
    is_active = Column(Boolean, default=False)
    
    sessions = relationship("ClassSession", back_populates="timetable", cascade="all, delete-orphan")

class ClassSession(Base):
    __tablename__ = "class_sessions"
    id = Column(Integer, primary_key=True, index=True)
    timetable_id = Column(Integer, ForeignKey("timetables.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    faculty_id = Column(Integer, ForeignKey("faculties.id"), nullable=True)
    classroom_id = Column(Integer, ForeignKey("classrooms.id"))
    
    day_of_week = Column(String) # e.g. "Monday"
    start_time = Column(Integer) # e.g. 9 for 9:00 AM
    end_time = Column(Integer)   # e.g. 10 for 10:00 AM
    
    timetable = relationship("Timetable", back_populates="sessions")
