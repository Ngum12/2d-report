from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import date


class WorkLogCreate(BaseModel):
    date: str
    annotator_name: str
    project_name: str
    task_type: str
    images_done: int = 0
    hours_spent: float = 0.0
    status: str
    challenges: Optional[str] = ""
    suggestions: Optional[str] = ""
    extra_notes: Optional[str] = ""

    @field_validator('annotator_name')
    @classmethod
    def annotator_name_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Annotator name is required')
        return v.strip()

    @field_validator('project_name')
    @classmethod
    def project_name_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Project name is required')
        return v.strip()

    @field_validator('date')
    @classmethod
    def date_valid(cls, v):
        if not v:
            raise ValueError('Date is required')
        try:
            date.fromisoformat(v)
        except ValueError:
            raise ValueError('Invalid date format. Use YYYY-MM-DD')
        return v

    @field_validator('task_type')
    @classmethod
    def task_type_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Task type is required')
        return v.strip()

    @field_validator('status')
    @classmethod
    def status_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Status is required')
        return v.strip()

    @field_validator('images_done')
    @classmethod
    def images_done_non_negative(cls, v):
        if v < 0:
            raise ValueError('Images done cannot be negative')
        return v

    @field_validator('hours_spent')
    @classmethod
    def hours_spent_non_negative(cls, v):
        if v < 0:
            raise ValueError('Hours spent cannot be negative')
        return v


class WorkLogResponse(BaseModel):
    id: int
    date: str
    annotator_name: str
    project_name: str
    task_type: str
    images_done: int
    hours_spent: float
    status: str
    challenges: Optional[str]
    suggestions: Optional[str]
    extra_notes: Optional[str]
    created_at: str

    class Config:
        from_attributes = True


class WorkLogFilter(BaseModel):
    date: str
    projects: Optional[List[str]] = None
    annotators: Optional[List[str]] = None

