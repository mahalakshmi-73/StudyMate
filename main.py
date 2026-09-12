from fastapi import FastAPI, Depends 
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import engine, SessionLocal, Base
from models import StudentDB

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Student(BaseModel):
    name: str
    study_hours: int
    mark: float


def get_db():
     db = SessionLocal()
     try:
          yield db
     finally:
          db.close()


@app.get("/")
def home():
     return {"message": "studyMate API is working!"} 

@app.post("/student")
def create_student(student:Student, db:Session = Depends(get_db)):

     if student.mark >= 90:
          level = "Excellent"

     elif student.mark >= 75:
          level = "Very Good"

     elif student.mark >= 50:
          level = "Good"

     else:
          level = "Needs Improvement"

     if student.study_hours >= 5:
          suggestion = "Keep up the good study routine!"
     elif student.study_hours >= 3:
          suggestion = "Try to increase your study hours."
     else:
          suggestion = "You need to spend more time studying."

     if student.mark >= 90:
          study_plan = "Revision important topics and practice mock tests."
     elif student.mark >= 75:
          study_plan = "Spend 1 hours on revision and 1 hour on weak topics."
     elif student.mark >= 50:
          study_plan = "Study 2 hours daily and practice important questions."
     else:
          study_plan = "Study 3 hours daily and focus more on weak subjects." 

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
          "message":"Student saved successfully!",
          "id":new_student.id,
          "name": new_student.name,
          "study_hours":new_student.study_hours,
          "mark": new_student.mark,
          "level": new_student.level,
          "suggestion": new_student.suggestion,
          "study_plan": study_plan
    }
@app.get("/students")
def get_students(db: Session = Depends(get_db)):
     students = db.query(StudentDB).all()

     return {
          "students": students
     }

@app.put("/student/{student_id}")
def update_student(
     student_id: int,
     student: Student,
     db: Session = Depends(get_db)
):
     existing_student = db.query(StudentDB).filter(StudentDB.id == student_id).first()

     if existing_student is None:
          return {
               "message": "Student not found"
          }
     
     if student.mark >= 90:
          level = "Excellent"
     elif student.mark >=75:
          level = "Very Good"
     elif student.mark >= 50:
          level = "Good"
     else:
          level = "Needs Improvement"

     if student.study_hours >= 5:
          suggestion = "Keep up the good study routine!"
     elif student.study_hours >= 3:
          suggestion = "Try to increase your study hours."
     else:
          suggestion = "You need to spend more time studying."

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
          "suggestion": existing_student.suggestion
     }

@app.delete("/student/{student_id}")
def delete_student(
     student_id: int,
     db: Session = Depends(get_db)
):
     existing_student = db.query(StudentDB).filter(StudentDB.id == student_id).first()
     
     if existing_student is None:
          return {
               "message": "Student not found"
          }
     
     db.delete(existing_student)
     db.commit()

     return {
          "message": "Student deleted successfully!",
          "id": student_id
     }

     