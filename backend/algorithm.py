import random
from sqlalchemy.orm import Session
from datetime import datetime
import models, schemas

# Constants
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
START_HOUR = 9
END_HOUR = 17 # 5 PM

def generate_timetable(db: Session):
    departments = db.query(models.Department).all()
    courses = db.query(models.Course).all()
    semesters = db.query(models.Semester).all()
    faculties = db.query(models.Faculty).all()
    classrooms = db.query(models.Classroom).all()
    subjects = db.query(models.Subject).all()
    
    if not classrooms or not subjects:
        return {"error": "Need at least one classroom and one subject to generate a timetable."}

    # Initialize Timetable
    new_tt = models.Timetable(
        created_at=datetime.now().isoformat(),
        fitness_score=0.0,
        is_active=False
    )
    db.add(new_tt)
    db.commit()
    db.refresh(new_tt)

    # Heuristic Data Structures
    faculty_schedule = {f.id: {day: [] for day in DAYS} for f in faculties}
    classroom_schedule = {r.id: {day: [] for day in DAYS} for r in classrooms}
    semester_schedule = {s.id: {day: [] for day in DAYS} for s in semesters}

    fitness = 100.0 # Start with perfect score, deduct for soft constraint violations
    
    def is_slot_free(schedule, entity_id, day, start, end):
        if entity_id is None or entity_id not in schedule: return True
        for (s_start, s_end) in schedule[entity_id][day]:
            # if overlaps
            if max(start, s_start) < min(end, s_end):
                return False
        return True

    def book_slot(schedule, entity_id, day, start, end):
        if entity_id is not None and entity_id in schedule:
            schedule[entity_id][day].append((start, end))

    # Process each subject based on weekly frequency
    # Sort subjects randomly to introduce variance in generation
    shuffled_subjects = list(subjects)
    random.shuffle(shuffled_subjects)
    
    for subject in shuffled_subjects:
        placed_classes = 0
        attempts = 0
        
        # Try to place each required class session for the subject
        while placed_classes < subject.weekly_frequency and attempts < 1000:
            attempts += 1
            
            day = random.choice(DAYS)
            start_time = random.randint(START_HOUR, END_HOUR - 1)
            end_time = start_time + 1 # 1 hour slot for simplicity
            
            room = random.choice(classrooms)
            faculty_id = subject.faculty_id
            sem_id = subject.semester_id
            
            # Check Hard Constraints
            # 1. Room is free
            if not is_slot_free(classroom_schedule, room.id, day, start_time, end_time):
                continue
                
            # 2. Faculty is free
            if faculty_id and not is_slot_free(faculty_schedule, faculty_id, day, start_time, end_time):
                continue
                
            # 3. Semester (students) is free
            if not is_slot_free(semester_schedule, sem_id, day, start_time, end_time):
                continue
                
            # Add session to DB
            session = models.ClassSession(
                timetable_id=new_tt.id,
                subject_id=subject.id,
                faculty_id=faculty_id,
                classroom_id=room.id,
                day_of_week=day,
                start_time=start_time,
                end_time=end_time
            )
            db.add(session)
            
            # Book the slots
            book_slot(classroom_schedule, room.id, day, start_time, end_time)
            book_slot(faculty_schedule, faculty_id, day, start_time, end_time)
            book_slot(semester_schedule, sem_id, day, start_time, end_time)
            
            placed_classes += 1
            
        if placed_classes < subject.weekly_frequency:
            # Failed to place all classes, deduct fitness heavily
            fitness -= (subject.weekly_frequency - placed_classes) * 10
            
    # Soft constraints evaluate (e.g. gaps in schedule)
    for f_id, schedule in faculty_schedule.items():
        for day, slots in schedule.items():
            if len(slots) > 4: # Penaltize more than 4 hours a day
                fitness -= 2
                
    new_tt.fitness_score = max(0.0, fitness)
    db.commit()
    db.refresh(new_tt)
    
    return {"message": "Timetable generated successfully", "timetable_id": new_tt.id, "fitness_score": new_tt.fitness_score}
