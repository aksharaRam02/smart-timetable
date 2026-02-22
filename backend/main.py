from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, database
from fastapi.middleware.cors import CORSMiddleware
from typing import List

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Smart Timetable Generator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Smart Timetable Generator API"}

# --- Departments ---
@app.post("/api/departments/", response_model=schemas.Department)
def create_department(department: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    db_department = models.Department(name=department.name)
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department

@app.get("/api/departments/", response_model=List[schemas.Department])
def read_departments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Department).offset(skip).limit(limit).all()

# --- Courses ---
@app.post("/api/courses/", response_model=schemas.Course)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    db_course = models.Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@app.get("/api/courses/", response_model=List[schemas.Course])
def read_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Course).offset(skip).limit(limit).all()

# --- Semesters ---
@app.post("/api/semesters/", response_model=schemas.Semester)
def create_semester(semester: schemas.SemesterCreate, db: Session = Depends(get_db)):
    db_semester = models.Semester(**semester.dict())
    db.add(db_semester)
    db.commit()
    db.refresh(db_semester)
    return db_semester

@app.get("/api/semesters/", response_model=List[schemas.Semester])
def read_semesters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Semester).offset(skip).limit(limit).all()

# --- Faculties ---
@app.post("/api/faculties/", response_model=schemas.Faculty)
def create_faculty(faculty: schemas.FacultyCreate, db: Session = Depends(get_db)):
    db_faculty = models.Faculty(**faculty.dict())
    db.add(db_faculty)
    db.commit()
    db.refresh(db_faculty)
    return db_faculty

@app.get("/api/faculties/", response_model=List[schemas.Faculty])
def read_faculties(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Faculty).offset(skip).limit(limit).all()

# --- Classrooms ---
@app.post("/api/classrooms/", response_model=schemas.Classroom)
def create_classroom(classroom: schemas.ClassroomCreate, db: Session = Depends(get_db)):
    db_classroom = models.Classroom(**classroom.dict())
    db.add(db_classroom)
    db.commit()
    db.refresh(db_classroom)
    return db_classroom

@app.get("/api/classrooms/", response_model=List[schemas.Classroom])
def read_classrooms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Classroom).offset(skip).limit(limit).all()

# --- Subjects ---
@app.post("/api/subjects/", response_model=schemas.Subject)
def create_subject(subject: schemas.SubjectCreate, db: Session = Depends(get_db)):
    db_subject = models.Subject(**subject.dict())
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject

@app.get("/api/subjects/", response_model=List[schemas.Subject])
def read_subjects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Subject).offset(skip).limit(limit).all()

# --- Timetables & Generation ---
@app.get("/api/timetables/", response_model=List[schemas.Timetable])
def read_timetables(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Timetable).offset(skip).limit(limit).all()

@app.get("/api/timetables/latest", response_model=schemas.Timetable)
def read_latest_timetable(db: Session = Depends(get_db)):
    tt = db.query(models.Timetable).order_by(models.Timetable.id.desc()).first()
    if tt is None:
        raise HTTPException(status_code=404, detail="No timetables found")
    return tt

@app.get("/api/timetables/{timetable_id}", response_model=schemas.Timetable)
def read_timetable(timetable_id: int, db: Session = Depends(get_db)):
    tt = db.query(models.Timetable).filter(models.Timetable.id == timetable_id).first()
    if tt is None:
        raise HTTPException(status_code=404, detail="Timetable not found")
    return tt

import algorithm

@app.post("/api/generate/")
def generate_timetable_endpoint(db: Session = Depends(get_db)):
    result = algorithm.generate_timetable(db)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
