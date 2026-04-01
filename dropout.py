from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

students = {
    1: {"name": "Juan", "dropout_risk": 0.2},
    2: {"name": "Maria", "dropout_risk": 0.7},
}

class Student(BaseModel):
    name: str
    dropout_risk: float

@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/students/{student_id}")
def get_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    return students[student_id]

@app.get("/risk/{student_id}")
def get_risk(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"risk": students[student_id]["dropout_risk"]}

@app.post("/students/{student_id}")
def create_or_update_student(student_id: int, student: Student):
    if student.dropout_risk < 0 or student.dropout_risk > 1:
        raise HTTPException(status_code=400, detail="Invalid risk value")

    students[student_id] = {
        "name": student.name,
        "dropout_risk": student.dropout_risk
    }

    return {"message": "Student saved", "student": students[student_id]}
