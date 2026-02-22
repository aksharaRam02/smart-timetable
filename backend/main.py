from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, database
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import algorithm
import os

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Smart Timetable Generator API",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# ------------------------
# CORS
# ------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------
# FRONTEND PATH SAFE FIX
# ------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

# Serve CSS, JS, assets
app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")


# --------- FRONTEND ROUTES ----------

@app.get("/")
def home():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.get("/admin.html")
def admin():
    return FileResponse(os.path.join(FRONTEND_DIR, "admin.html"))

@app.get("/faculty.html")
def faculty():
    return FileResponse(os.path.join(FRONTEND_DIR, "faculty.html"))

@app.get("/student.html")
def student():
    return FileResponse(os.path.join(FRONTEND_DIR, "student.html"))

@app.get("/timetable.html")
def timetable():
    return FileResponse(os.path.join(FRONTEND_DIR, "timetable.html"))


# ------------------------
# DATABASE
# ------------------------

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------------
# API ROUTES
# ------------------------

@app.post("/api/departments/", response_model=schemas.Department)
def create_department(department: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    obj = models.Department(name=department.name)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.get("/api/departments/", response_model=List[schemas.Department])
def read_departments(db: Session = Depends(get_db)):
    return db.query(models.Department).all()


@app.post("/api/courses/", response_model=schemas.Course)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    obj = models.Course(**course.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.get("/api/courses/", response_model=List[schemas.Course])
def read_courses(db: Session = Depends(get_db)):
    return db.query(models.Course).all()


@app.post("/api/semesters/", response_model=schemas.Semester)
def create_semester(semester: schemas.SemesterCreate, db: Session = Depends(get_db)):
    obj = models.Semester(**semester.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.get("/api/semesters/", response_model=List[schemas.Semester])
def read_semesters(db: Session = Depends(get_db)):
    return db.query(models.Semester).all()


@app.post("/api/faculties/", response_model=schemas.Faculty)
def create_faculty(faculty: schemas.FacultyCreate, db: Session = Depends(get_db)):
    obj = models.Faculty(**faculty.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.get("/api/faculties/", response_model=List[schemas.Faculty])
def read_faculties(db: Session = Depends(get_db)):
    return db.query(models.Faculty).all()


@app.post("/api/classrooms/", response_model=schemas.Classroom)
def create_classroom(classroom: schemas.ClassroomCreate, db: Session = Depends(get_db)):
    obj = models.Classroom(**classroom.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.get("/api/classrooms/", response_model=List[schemas.Classroom])
def read_classrooms(db: Session = Depends(get_db)):
    return db.query(models.Classroom).all()


@app.post("/api/subjects/", response_model=schemas.Subject)
def create_subject(subject: schemas.SubjectCreate, db: Session = Depends(get_db)):
    obj = models.Subject(**subject.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.get("/api/subjects/", response_model=List[schemas.Subject])
def read_subjects(db: Session = Depends(get_db)):
    return db.query(models.Subject).all()


@app.get("/api/timetables/", response_model=List[schemas.Timetable])
def read_timetables(db: Session = Depends(get_db)):
    return db.query(models.Timetable).all()


@app.get("/api/timetables/latest", response_model=schemas.Timetable)
def read_latest_timetable(db: Session = Depends(get_db)):
    tt = db.query(models.Timetable).order_by(models.Timetable.id.desc()).first()
    if not tt:
        raise HTTPException(status_code=404, detail="No timetables found")
    return tt


@app.get("/api/timetables/{timetable_id}", response_model=schemas.Timetable)
def read_timetable(timetable_id: int, db: Session = Depends(get_db)):
    tt = db.query(models.Timetable).filter(models.Timetable.id == timetable_id).first()
    if not tt:
        raise HTTPException(status_code=404, detail="Timetable not found")
    return tt


@app.post("/api/generate/")
def generate_timetable_endpoint(db: Session = Depends(get_db)):
    result = algorithm.generate_timetable(db)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
