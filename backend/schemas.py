from pydantic import BaseModel
from typing import List, Optional

class DepartmentBase(BaseModel):
    name: str

class DepartmentCreate(DepartmentBase):
    pass

class Department(DepartmentBase):
    id: int
    class Config:
        from_attributes = True

class FacultyBase(BaseModel):
    name: str
    department_id: int
    max_hours_per_week: int = 40

class FacultyCreate(FacultyBase):
    pass

class Faculty(FacultyBase):
    id: int
    class Config:
        orm_mode = True

class SubjectBase(BaseModel):
    name: str
    code: str
    credit_hours: int
    weekly_frequency: int
    semester_id: int
    faculty_id: Optional[int] = None

class SubjectCreate(SubjectBase):
    pass

class Subject(SubjectBase):
    id: int
    class Config:
        orm_mode = True

class ClassroomBase(BaseModel):
    name: str
    capacity: int
    room_type: str

class ClassroomCreate(ClassroomBase):
    pass

class Classroom(ClassroomBase):
    id: int
    class Config:
        orm_mode = True
        
class CourseBase(BaseModel):
    name: str
    department_id: int

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int
    class Config:
        orm_mode = True

class SemesterBase(BaseModel):
    name: str
    course_id: int

class SemesterCreate(SemesterBase):
    pass

class Semester(SemesterBase):
    id: int
    class Config:
        from_attributes = True

class ClassSessionBase(BaseModel):
    subject_id: int
    faculty_id: Optional[int]
    classroom_id: int
    day_of_week: str
    start_time: int
    end_time: int

class ClassSessionCreate(ClassSessionBase):
    pass

class ClassSession(ClassSessionBase):
    id: int
    timetable_id: int
    class Config:
        from_attributes = True

class TimetableBase(BaseModel):
    created_at: str
    fitness_score: float
    is_active: bool

class TimetableCreate(TimetableBase):
    pass

class Timetable(TimetableBase):
    id: int
    sessions: List[ClassSession] = []
    class Config:
        from_attributes = True
