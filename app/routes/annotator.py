from datetime import date
from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import ValidationError

from app.database import get_db
from app.config import TASK_TYPES, STATUS_OPTIONS
from app.schemas.work_log import WorkLogCreate
from app.services.work_log_service import WorkLogService

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/log", response_class=HTMLResponse)
async def show_form(request: Request):
    """Display the annotator work log form."""
    return templates.TemplateResponse(
        "annotator_form.html",
        {
            "request": request,
            "today": date.today().isoformat(),
            "task_types": TASK_TYPES,
            "status_options": STATUS_OPTIONS,
            "errors": {},
            "form_data": {}
        }
    )


@router.post("/log", response_class=HTMLResponse)
async def submit_form(
    request: Request,
    db: Session = Depends(get_db),
    log_date: str = Form(..., alias="date"),
    annotator_name: str = Form(""),
    project_name: str = Form(""),
    task_type: str = Form(""),
    images_done: int = Form(0),
    hours_spent: float = Form(0.0),
    status: str = Form(""),
    challenges: str = Form(""),
    suggestions: str = Form(""),
    extra_notes: str = Form("")
):
    """Handle work log form submission."""
    form_data = {
        "date": log_date,
        "annotator_name": annotator_name,
        "project_name": project_name,
        "task_type": task_type,
        "images_done": images_done,
        "hours_spent": hours_spent,
        "status": status,
        "challenges": challenges,
        "suggestions": suggestions,
        "extra_notes": extra_notes
    }
    
    errors = {}
    
    # Validate using Pydantic schema
    try:
        work_log_data = WorkLogCreate(**form_data)
        
        # Additional validation: at least some work should be logged
        if work_log_data.images_done == 0 and work_log_data.hours_spent == 0:
            errors["images_done"] = "Please log either images done or hours spent"
        
    except ValidationError as e:
        for error in e.errors():
            field = error["loc"][0]
            errors[field] = error["msg"]
    
    if errors:
        return templates.TemplateResponse(
            "annotator_form.html",
            {
                "request": request,
                "today": date.today().isoformat(),
                "task_types": TASK_TYPES,
                "status_options": STATUS_OPTIONS,
                "errors": errors,
                "form_data": form_data
            },
            status_code=400
        )
    
    # Save to database
    work_log = WorkLogService.create_work_log(db, work_log_data)
    
    return templates.TemplateResponse(
        "annotator_success.html",
        {
            "request": request,
            "work_log": work_log
        }
    )

