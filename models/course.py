from __future__ import annotations

from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field
from .student import StudentBase

class CourseBase(BaseModel):
    name: str = Field(
        ...,
        description="Course name",
        json_schema_extra={"example": "Cloud Computing"}
    )
    code: str = Field(
        ...,
        description="Course code (e.g., COMS4135)",
        json_schema_extra={"example": "COMS4135"}
    )
    professor: str = Field(
        ...,
        description="Professor's name",
        json_schema_extra={"example": "Michael Johnson"}
    )
    credits: int = Field(
        ...,
        description="Credits",
        json_schema_extra={"example": 3}
    )

    enrolled_students: List[StudentBase] = Field(
        default_factory=list,
        description="List of students enrolled in this course (each with a persistent student ID)",
        json_schema_extra={
            "example": [
                {
                    "id": "87654321-4321-8765-4321-876543218765",
                    "name": "Shohei Otani",
                    "student_id": "so1156",
                    "email": "so1156@columbia.edu"
                }
            ]
        }
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Cloud Computing",
                    "code": "COMS4135",
                    "professor": "Michael Johnson",
                    "credits": 3,
                    "enrolled_students": [
                        {
                            "id": "87654321-4321-8765-4321-876543218765",
                            "name": "Shohei Otani",
                            "student_id": "so1156",
                            "email": "so1156@columbia.edu"
                        }
                    ]
                }
            ]
        }
    }

class CourseCreate(CourseBase):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Python Programming",
                    "code": "COMS1010",
                    "professor": "Michel Lee",
                    "credits": 1,
                    "enrolled_students": []
                }
            ]
        }
    }


class CourseUpdate(BaseModel):
    name: Optional[str] = Field(
        None,
        description="update the course name"
    )
    professor: Optional[str] = Field(
        None,
        description="update the professor's name"
    )
    enrolled_students: Optional[List[StudentBase]] = Field(
        None,
        description="replace the entire list of enrolled students with this list."
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"name": "Database"},
                {"professor": "Sebastian Klein"},
            ]
        }
    }

class CourseRead(CourseBase):
    id: UUID = Field(
        default_factory=uuid4,
        description="Persistent Course ID (server-generated).",
        json_schema_extra={"example": "12345678-1234-5678-1234-567812345678"}
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="creation timestamp",
        json_schema_extra={"example": "2025-01-01T00:00:00Z"}
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="last updated timestamp",
        json_schema_extra={"example": "2025-01-02T00:00:00Z"}
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "12345678-1234-5678-1234-567812345678",
                    "name": "Cloud Computing",
                    "code": "COMS4135",
                    "professor": "Michael Johnson",
                    "credits": 3,
                    "enrolled_students": [
                        {
                            "id": "87654321-4321-8765-4321-876543218765",
                            "name": "Shohei Otani",
                            "student_id": "so1156",
                            "email": "so1156@columbia.edu"
                        }
                    ],
                    "created_at": "2025-01-01T00:00:00Z",
                    "updated_at": "2025-01-02T00:00:00Z"
                }
            ]
        }
    }