from datetime import date
from typing import Optional
from fastapi import APIRouter, Request, Depends, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.work_log_service import WorkLogService

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def parse_filter_list(value: Optional[str]) -> Optional[list]:
    """Parse comma-separated filter string into list."""
    if not value:
        return None
    items = [item.strip() for item in value.split(",") if item.strip()]
    return items if items else None


@router.get("/dashboard", response_class=HTMLResponse)
async def show_dashboard(
    request: Request,
    db: Session = Depends(get_db),
    filter_date: str = Query(None, alias="date"),
    projects: str = Query(None),
    annotators: str = Query(None)
):
    """Display the team lead dashboard."""
    # Default to today if no date provided
    selected_date = filter_date or date.today().isoformat()
    
    # Parse filters
    project_filter = parse_filter_list(projects)
    annotator_filter = parse_filter_list(annotators)
    
    # Get filter options (all available for the date)
    all_projects = WorkLogService.get_distinct_projects(db, selected_date)
    all_annotators = WorkLogService.get_distinct_annotators(db, selected_date)
    all_dates = WorkLogService.get_distinct_dates(db)
    
    # Get data
    metrics = WorkLogService.get_summary_metrics(
        db, selected_date, project_filter, annotator_filter
    )
    
    annotator_summary = WorkLogService.get_annotator_summary(
        db, selected_date, project_filter, annotator_filter
    )
    
    project_summary = WorkLogService.get_project_summary(
        db, selected_date, project_filter, annotator_filter
    )
    
    logs = WorkLogService.get_logs_by_date(
        db, selected_date, project_filter, annotator_filter
    )
    
    challenges_list = WorkLogService.get_challenges_and_suggestions(
        db, selected_date, project_filter, annotator_filter
    )
    
    # Prepare chart data
    chart_annotators = {
        "labels": [a["annotator_name"] for a in annotator_summary],
        "data": [a["total_images"] for a in annotator_summary]
    }
    
    chart_projects = {
        "labels": [p["project_name"] for p in project_summary],
        "data": [p["total_images"] for p in project_summary]
    }
    
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "selected_date": selected_date,
            "all_dates": all_dates,
            "all_projects": all_projects,
            "all_annotators": all_annotators,
            "selected_projects": project_filter or all_projects,
            "selected_annotators": annotator_filter or all_annotators,
            "metrics": metrics,
            "annotator_summary": annotator_summary,
            "project_summary": project_summary,
            "logs": logs,
            "challenges_list": challenges_list,
            "chart_annotators": chart_annotators,
            "chart_projects": chart_projects
        }
    )


@router.get("/api/filters", response_class=JSONResponse)
async def get_filter_options(
    db: Session = Depends(get_db),
    filter_date: str = Query(None, alias="date")
):
    """Get available filter options for a given date."""
    selected_date = filter_date or date.today().isoformat()
    
    return {
        "date": selected_date,
        "projects": WorkLogService.get_distinct_projects(db, selected_date),
        "annotators": WorkLogService.get_distinct_annotators(db, selected_date)
    }

