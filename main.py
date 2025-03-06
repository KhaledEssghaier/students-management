from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS Configuration
origins = [
    "http://localhost",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Student Model
class Student(BaseModel):
    id: int
    name: str
    age: int
    course: str

class StudentCreate(BaseModel):
    name: str
    age: int
    course: str

# In-memory student data
students = [
    Student(id=1, name="John Doe", age=21, course="Computer Science"),
    Student(id=2, name="Jane Smith", age=22, course="Mathematics"),
    Student(id=3, name="Alice Johnson", age=20, course="Physics")
]

# Endpoints
@app.get("/students", response_model=List[Student])
def get_students():
    """Retrieve all students"""
    return students

@app.post("/students", response_model=Student)
def create_student(student: StudentCreate):
    """Add a new student"""
    new_id = max(s.id for s in students) + 1 if students else 1
    new_student = Student(id=new_id, **student.dict())
    students.append(new_student)
    return new_student

@app.get("/students/{student_id}", response_model=Student)
def get_student(student_id: int):
    """Retrieve a specific student by ID"""
    student = next((s for s in students if s.id == student_id), None)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student