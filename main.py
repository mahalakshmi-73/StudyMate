import os

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import engine, SessionLocal, Base
from models import StudentDB


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI()


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Student input model
class Student(BaseModel):
    name: str = Field(..., min_length=1)
    study_hours: float = Field(..., ge=0)
    mark: float = Field(..., ge=0, le=100)


# Database connection
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# Calculate level
def get_student_level(mark):

    if mark >= 90:
        return "Excellent"

    elif mark >= 75:
        return "Very Good"

    elif mark >= 50:
        return "Good"

    else:
        return "Needs Improvement"


# Generate suggestion
def get_suggestion(study_hours):

    if study_hours >= 5:
        return "Keep up the good study routine!"

    elif study_hours >= 3:
        return "Try to increase your study hours."

    else:
        return "You need to spend more time studying."


# Generate study plan
def get_study_plan(mark):

    if mark >= 90:
        return "Revise important topics and practice mock tests."

    elif mark >= 75:
        return "Spend 1 hour on revision and 1 hour on weak topics."

    elif mark >= 50:
        return "Study 2 hours daily and practice important questions."

    else:
        return "Study 3 hours daily and focus more on weak subjects."


# ==========================================
# API ROUTES
# ==========================================


@app.get("/api")
def api_home():

    return {
        "message": "StudyMate API is working!"
    }


# ==========================================
# CREATE STUDENT
# ==========================================

@app.post("/student")
def create_student(
    student: Student,
    db: Session = Depends(get_db)
):

    level = get_student_level(student.mark)

    suggestion = get_suggestion(
        student.study_hours
    )

    study_plan = get_study_plan(
        student.mark
    )

    new_student = StudentDB(
        name=student.name,
        study_hours=student.study_hours,
        mark=student.mark,
        level=level,
        suggestion=suggestion
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return {
        "message": "Student saved successfully!",
        "id": new_student.id,
        "name": new_student.name,
        "study_hours": new_student.study_hours,
        "mark": new_student.mark,
        "level": new_student.level,
        "suggestion": new_student.suggestion,
        "study_plan": study_plan
    }


# ==========================================
# GET ALL STUDENTS
# ==========================================

@app.get("/students")
def get_students(
    db: Session = Depends(get_db)
):

    students = db.query(StudentDB).all()

    result = []

    for student in students:

        result.append({
            "id": student.id,
            "name": student.name,
            "study_hours": student.study_hours,
            "mark": student.mark,
            "level": student.level,
            "suggestion": student.suggestion,
            "study_plan": get_study_plan(student.mark)
        })

    return {
        "students": result
    }


# ==========================================
# UPDATE STUDENT
# ==========================================

@app.put("/student/{student_id}")
def update_student(
    student_id: int,
    student: Student,
    db: Session = Depends(get_db)
):

    existing_student = (
        db.query(StudentDB)
        .filter(StudentDB.id == student_id)
        .first()
    )

    if existing_student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    level = get_student_level(student.mark)
    suggestion = get_suggestion(student.study_hours)
    study_plan = get_study_plan(student.mark)

    existing_student.name = student.name
    existing_student.study_hours = student.study_hours
    existing_student.mark = student.mark
    existing_student.level = level
    existing_student.suggestion = suggestion

    db.commit()
    db.refresh(existing_student)

    return {
        "message": "Student updated successfully!",
        "id": existing_student.id,
        "name": existing_student.name,
        "study_hours": existing_student.study_hours,
        "mark": existing_student.mark,
        "level": existing_student.level,
        "suggestion": existing_student.suggestion,
        "study_plan": study_plan
    }


# ==========================================
# DELETE STUDENT
# ==========================================

@app.delete("/student/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    existing_student = (
        db.query(StudentDB)
        .filter(StudentDB.id == student_id)
        .first()
    )

    if existing_student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(existing_student)
    db.commit()

    return {
        "message": "Student deleted successfully!",
        "id": student_id
    }


# ==========================================
# SERVE FRONTEND
# ==========================================
# Your project uses a single frontend.html file (per README), not a
# "frontend" folder, so mounting StaticFiles(directory="frontend") crashed
# on startup because that directory doesn't exist. This serves the single
# HTML file at "/" instead, and only if it's actually present.

FRONTEND_FILE = os.path.join(os.path.dirname(__file__), "frontend.html")


@app.get("/")
def serve_frontend():

    if os.path.exists(FRONTEND_FILE):
        return FileResponse(FRONTEND_FILE)

    return {
        "message": "StudyMate API is working! frontend.html not found.",
        "looking_for_this_exact_path": FRONTEND_FILE,
        "files_actually_in_that_folder": os.listdir(
            os.path.dirname(FRONTEND_FILE) or "."
        )
    }
