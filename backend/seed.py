import requests

BASE_URL = "http://localhost:8001/api"

def seed():
    # 1. Dept
    d = requests.post(f"{BASE_URL}/departments/", json={"name": "Computer Science"}).json()
    d_id = d["id"]

    # 2. Course
    c = requests.post(f"{BASE_URL}/courses/", json={"name": "B.Tech CS", "department_id": d_id}).json()
    c_id = c["id"]

    # 3. Semester
    sem = requests.post(f"{BASE_URL}/semesters/", json={"name": "Semester 1", "course_id": c_id}).json()
    sem_id = sem["id"]

    # 4. Faculties
    f1 = requests.post(f"{BASE_URL}/faculties/", json={"name": "Dr. Smith", "department_id": d_id, "max_hours_per_week": 40}).json()
    f2 = requests.post(f"{BASE_URL}/faculties/", json={"name": "Prof. Johnson", "department_id": d_id, "max_hours_per_week": 40}).json()
    f3 = requests.post(f"{BASE_URL}/faculties/", json={"name": "Dr. Emily", "department_id": d_id, "max_hours_per_week": 20}).json()

    # 5. Classrooms
    r1 = requests.post(f"{BASE_URL}/classrooms/", json={"name": "Room 101", "capacity": 60, "room_type": "Lecture"}).json()
    r2 = requests.post(f"{BASE_URL}/classrooms/", json={"name": "Lab A", "capacity": 30, "room_type": "Lab"}).json()

    # 6. Subjects
    requests.post(f"{BASE_URL}/subjects/", json={
        "name": "Data Structures", "code": "CS101", "credit_hours": 3, "weekly_frequency": 3,
        "semester_id": sem_id, "faculty_id": f1["id"]
    })
    requests.post(f"{BASE_URL}/subjects/", json={
        "name": "Algorithms", "code": "CS102", "credit_hours": 4, "weekly_frequency": 4,
        "semester_id": sem_id, "faculty_id": f2["id"]
    })
    requests.post(f"{BASE_URL}/subjects/", json={
        "name": "Programming Lab", "code": "CSL10", "credit_hours": 2, "weekly_frequency": 2,
        "semester_id": sem_id, "faculty_id": f3["id"]
    })

    print("Data seeded successfully!")

    # Generate timetable
    res = requests.post(f"{BASE_URL}/generate/")
    print("Generation result:", res.json())

if __name__ == "__main__":
    seed()
