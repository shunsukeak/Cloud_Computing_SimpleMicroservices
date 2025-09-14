from __future__ import annotations

from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class StudentBase(BaseModel):
    id: UUID = Field(
        default_factory=uuid4,
        description="Persistent Student ID (server-generated).",
        json_schema_extra={"example": "87654321-4321-8765-4321-876543218765"}
    )
    name: str = Field(
        ...,
        description="Student's name.",
        json_schema_extra={"example": "Steve Smith"}
    )
    student_id: str = Field(
        ...,
        description="Student ID (e.g., ss2234)",
        json_schema_extra={"example": "ss2234"}
    )
    email: EmailStr = Field(
        ...,
        description="Student's email address",
        json_schema_extra={"example": "ss2234@columbia.edu"}
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "87654321-4321-8765-4321-876543218765",
                    "name": "Steve Smith",
                    "student_id": "ss2234",
                    "email": "ss2234@columbia.edu"
                }
            ]
        }
    }


class StudentCreate(StudentBase):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Bob Johnson",
                    "student_id": "bj2235",
                    "email": "bj2235@columbia.edu"
                }
            ]
        }
    }


class StudentUpdate(BaseModel):
    name: Optional[str] = Field(
        None,
        description="Name of the student to update.",
        json_schema_extra={"example": "Robert jordan"}
    )
    email: Optional[EmailStr] = Field(
        None,
        description="Email address of the student to update.",
        json_schema_extra={"example": "rj1133@columbia.edu"}
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Robert jordan",
                    "email": "rj1133@columbia.edu"
                }
            ]
        }
    }


class StudentRead(StudentBase):
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-01-01T00:00:00Z"}
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-01-02T00:00:00Z"}
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "87654321-4321-8765-4321-876543218765",
                    "name": "Alice Smith",
                    "student_id": "as2277",
                    "email": "as2277@columbia.edu",
                    "created_at": "2025-01-01T00:00:00Z",
                    "updated_at": "2025-01-02T00:00:00Z"
                }
            ]
        }
    }