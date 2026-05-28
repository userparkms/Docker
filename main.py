from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import json
import os

app = FastAPI(
    title="Courses API",
    description="Docker & EC2 배포 실습",
    version="1.0.0"
)

DATA_FILE = "courses.json"


def load_courses():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_courses(courses):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(courses, f, ensure_ascii=False, indent=2)


class Course(BaseModel):
    id: Optional[int] = None
    name: str
    instructor: str
    description: Optional[str] = ""
    credits: int


@app.get("/")
def root():
    return {
        "message": "Courses API is running!",
        "docs": "/docs",
        "courses": "/courses"
    }


@app.get("/courses")
def get_courses():
    return load_courses()


@app.get("/courses/{course_id}")
def get_course(course_id: int):
    courses = load_courses()
    for course in courses:
        if course["id"] == course_id:
            return course
    raise HTTPException(status_code=404, detail="Course not found")


@app.post("/courses", status_code=201)
def create_course(course: Course):
    courses = load_courses()
    new_id = max((c["id"] for c in courses), default=0) + 1
    new_course = course.model_dump()
    new_course["id"] = new_id
    courses.append(new_course)
    save_courses(courses)
    return new_course


@app.put("/courses/{course_id}")
def update_course(course_id: int, course: Course):
    courses = load_courses()
    for i, c in enumerate(courses):
        if c["id"] == course_id:
            updated = course.model_dump()
            updated["id"] = course_id
            courses[i] = updated
            save_courses(courses)
            return updated
    raise HTTPException(status_code=404, detail="Course not found")


@app.delete("/courses/{course_id}")
def delete_course(course_id: int):
    courses = load_courses()
    for i, c in enumerate(courses):
        if c["id"] == course_id:
            courses.pop(i)
            save_courses(courses)
            return {"message": f"Course {course_id} deleted"}
    raise HTTPException(status_code=404, detail="Course not found")