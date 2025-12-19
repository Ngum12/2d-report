from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.work_log_service import WorkLogService
from app.services.export_service import ExportService

router = APIRouter()


def parse_filter_list(value: Optional[str]) -> Optional[list]:
    """Parse comma-separated filter string into list."""
    if not value:
        return None
    items = [item.strip() for item in value.split(",") if item.strip()]
    return items if items else None


@router.get("/export/csv")
async def download_csv(
    db: Session = Depends(get_db),
    filter_date: str = Query(None, alias="date"),
    projects: str = Query(None),
    annotators: str = Query(None)
):
    """Download work logs as CSV file."""
    selected_date = filter_date or date.today().isoformat()
    project_filter = parse_filter_list(projects)
    annotator_filter = parse_filter_list(annotators)
    
    logs = WorkLogService.get_logs_by_date(
        db, selected_date, project_filter, annotator_filter
    )
    
    csv_content = ExportService.generate_csv(logs)
    filename = f"annotation_report_{selected_date}.csv"
    
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
    )


@router.get("/export/excel")
async def download_excel(
    db: Session = Depends(get_db),
    filter_date: str = Query(None, alias="date"),
    projects: str = Query(None),
    annotators: str = Query(None)
):
    """Download work logs as Excel file."""
    selected_date = filter_date or date.today().isoformat()
    project_filter = parse_filter_list(projects)
    annotator_filter = parse_filter_list(annotators)
    
    logs = WorkLogService.get_logs_by_date(
        db, selected_date, project_filter, annotator_filter
    )
    
    excel_content = ExportService.generate_excel(logs, selected_date)
    filename = f"annotation_report_{selected_date}.xlsx"
    
    return Response(
        content=excel_content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
    )

