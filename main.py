from __future__ import annotations

import os
import socket
from datetime import datetime

from typing import Dict, List, Optional
from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException, Query, Path, Response

from models.student import StudentCreate, StudentRead, StudentUpdate
from models.course import CourseCreate, CourseRead, CourseUpdate
from models.health import Health

port = int(os.environ.get("FASTAPIPORT", 8000))

# -----------------------------------------------------------------------------
# Fake in-memory "databases"
# -----------------------------------------------------------------------------
students: Dict[UUID, StudentRead] = {}
courses: Dict[UUID, CourseRead] = {}

app = FastAPI(
    title="Course/Student API",
    description="Demo FastAPI app using Pydantic v2 models for Courses and Students",
    version="0.1.0",
)

def make_health(echo: Optional[str], path_echo: Optional[str]=None) -> Health:
    return Health(
        status=200,
        status_message="OK",
        timestamp=datetime.utcnow().isoformat() + "Z",
        ip_address=socket.gethostbyname(socket.gethostname()),
        echo=echo,
        path_echo=path_echo
    )

@app.get("/health", response_model=Health)
def get_health_no_path(echo: str | None = Query(None, description="Optional echo string")):
    return make_health(echo=echo, path_echo=None)

@app.get("/health/{path_echo}", response_model=Health)
def get_health_with_path(
    path_echo: str = Path(..., description="Required echo in the URL path"),
    echo: str | None = Query(None, description="Optional echo string"),
):
    return make_health(echo=echo, path_echo=path_echo)

# -----------------------------------------------------------------------------
# Student endpoints
# -----------------------------------------------------------------------------
@app.post("/students", response_model=StudentRead, status_code=201)
def create_student(student: StudentCreate):
    new_id = uuid4()
    student_read = StudentRead(id=new_id, **student.model_dump(exclude={'id'}))
    students[student_read.id] = student_read
    return student_read

@app.get("/students", response_model=List[StudentRead])
def list_students(
    name: Optional[str] = Query(None, description="Filter by student name"),
    student_id: Optional[str] = Query(None, description="Filter by student ID"),
):
    results = list(students.values())

    if name is not None:
        results = [s for s in results if s.name == name]
    if student_id is not None:
        results = [s for s in results if s.student_id == student_id]

    return results

@app.get("/students/{student_id}", response_model=StudentRead)
def get_student(student_id: UUID):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    return students[student_id]

@app.put("/students/{student_id}", response_model=StudentRead)
def update_student(student_id: UUID, student: StudentCreate):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    
    updated_student = StudentRead(id=student_id, **student.model_dump(exclude={'id'}))
    students[student_id] = updated_student
    return updated_student

@app.delete("/students/{student_id}", status_code=204)
def delete_student(student_id: UUID):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    del students[student_id]
    return Response(status_code=204)

# -----------------------------------------------------------------------------
# Course endpoints
# -----------------------------------------------------------------------------
@app.post("/courses", response_model=CourseRead, status_code=201)
def create_course(course: CourseCreate):
    new_id = uuid4()
    course_read = CourseRead(id=new_id, **course.model_dump(exclude={'id'}))
    courses[course_read.id] = course_read
    return course_read

@app.get("/courses", response_model=List[CourseRead])
def list_courses(
    name: Optional[str] = Query(None, description="filter by course name"),
    professor: Optional[str] = Query(None, description="filter by professor name"),
    credits: Optional[int] = Query(None, description="filter by number of credits"),
):
    results = list(courses.values())

    if name is not None:
        results = [c for c in results if c.name == name]
    if professor is not None:
        results = [c for c in results if c.professor == professor]
    if credits is not None:
        results = [c for c in results if c.credits == credits]

    return results

@app.get("/courses/{course_id}", response_model=CourseRead)
def get_course(course_id: UUID):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    return courses[course_id]

@app.put("/courses/{course_id}", response_model=CourseRead)
def update_course(course_id: UUID, course: CourseCreate):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    
    updated_course = CourseRead(id=course_id, **course.model_dump(exclude={'id'}))
    courses[course_id] = updated_course
    return updated_course

@app.delete("/courses/{course_id}", status_code=204)
def delete_course(course_id: UUID):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    del courses[course_id]
    return Response(status_code=204)

# -----------------------------------------------------------------------------
# Root
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Welcome to the Course/Student API. See /docs for OpenAPI UI."}

# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)