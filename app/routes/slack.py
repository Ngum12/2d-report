from datetime import date
from typing import Optional
from fastapi import APIRouter, Request, Depends, Form, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.config import SLACK_WEBHOOK_URL
from app.services.work_log_service import WorkLogService
from app.services.slack_service import SlackService

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def parse_filter_list(value: Optional[str]) -> Optional[list]:
    """Parse comma-separated filter string into list."""
    if not value:
        return None
    items = [item.strip() for item in value.split(",") if item.strip()]
    return items if items else None


@router.post("/api/slack/preview", response_class=JSONResponse)
async def preview_slack_message(
    request: Request,
    db: Session = Depends(get_db),
    filter_date: str = Form(None, alias="date"),
    projects: str = Form(None),
    annotators: str = Form(None),
    task_allocation: str = Form("")
):
    """Generate a preview of the Slack message."""
    selected_date = filter_date or date.today().isoformat()
    project_filter = parse_filter_list(projects)
    annotator_filter = parse_filter_list(annotators)
    
    # Get data
    metrics = WorkLogService.get_summary_metrics(
        db, selected_date, project_filter, annotator_filter
    )
    project_summary = WorkLogService.get_project_summary(
        db, selected_date, project_filter, annotator_filter
    )
    annotator_summary = WorkLogService.get_annotator_summary(
        db, selected_date, project_filter, annotator_filter
    )
    challenges_list = WorkLogService.get_challenges_and_suggestions(
        db, selected_date, project_filter, annotator_filter
    )
    
    # Generate preview
    preview = SlackService.generate_preview(
        selected_date,
        metrics,
        project_summary,
        annotator_summary,
        challenges_list,
        task_allocation
    )
    
    return {"success": True, "preview": preview}


@router.post("/api/slack/send", response_class=JSONResponse)
async def send_slack_message(
    request: Request,
    db: Session = Depends(get_db),
    filter_date: str = Form(None, alias="date"),
    projects: str = Form(None),
    annotators: str = Form(None),
    task_allocation: str = Form(""),
    webhook_url: str = Form(None)
):
    """Send the daily report to Slack."""
    selected_date = filter_date or date.today().isoformat()
    project_filter = parse_filter_list(projects)
    annotator_filter = parse_filter_list(annotators)
    
    # Get data
    metrics = WorkLogService.get_summary_metrics(
        db, selected_date, project_filter, annotator_filter
    )
    project_summary = WorkLogService.get_project_summary(
        db, selected_date, project_filter, annotator_filter
    )
    annotator_summary = WorkLogService.get_annotator_summary(
        db, selected_date, project_filter, annotator_filter
    )
    challenges_list = WorkLogService.get_challenges_and_suggestions(
        db, selected_date, project_filter, annotator_filter
    )
    
    # Generate message
    message = SlackService.generate_slack_message(
        selected_date,
        metrics,
        project_summary,
        annotator_summary,
        challenges_list,
        task_allocation
    )
    
    # Send to Slack
    result = await SlackService.send_to_slack(message, webhook_url or None)
    
    return result


@router.get("/api/slack/config", response_class=JSONResponse)
async def get_slack_config():
    """Check if Slack is configured."""
    return {
        "configured": bool(SLACK_WEBHOOK_URL),
        "webhook_url_set": bool(SLACK_WEBHOOK_URL)
    }

