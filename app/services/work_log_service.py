from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct

from app.models.work_log import WorkLog
from app.schemas.work_log import WorkLogCreate


class WorkLogService:
    """Service for work log operations."""

    @staticmethod
    def create_work_log(db: Session, data: WorkLogCreate) -> WorkLog:
        """Create a new work log entry."""
        work_log = WorkLog(
            date=data.date,
            annotator_name=data.annotator_name,
            project_name=data.project_name,
            task_type=data.task_type,
            images_done=data.images_done,
            hours_spent=data.hours_spent,
            status=data.status,
            challenges=data.challenges or "",
            suggestions=data.suggestions or "",
            extra_notes=data.extra_notes or "",
            created_at=datetime.now().isoformat()
        )
        db.add(work_log)
        db.commit()
        db.refresh(work_log)
        return work_log

    @staticmethod
    def get_logs_by_date(
        db: Session,
        date: str,
        projects: Optional[List[str]] = None,
        annotators: Optional[List[str]] = None
    ) -> List[WorkLog]:
        """Get work logs for a specific date with optional filters."""
        query = db.query(WorkLog).filter(WorkLog.date == date)
        
        if projects:
            query = query.filter(WorkLog.project_name.in_(projects))
        
        if annotators:
            query = query.filter(WorkLog.annotator_name.in_(annotators))
        
        return query.order_by(WorkLog.created_at.desc()).all()

    @staticmethod
    def get_summary_metrics(
        db: Session,
        date: str,
        projects: Optional[List[str]] = None,
        annotators: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Get summary metrics for dashboard KPIs."""
        query = db.query(
            func.sum(WorkLog.images_done).label('total_images'),
            func.sum(WorkLog.hours_spent).label('total_hours'),
            func.count(distinct(WorkLog.annotator_name)).label('annotator_count'),
            func.count(WorkLog.id).label('total_entries')
        ).filter(WorkLog.date == date)
        
        if projects:
            query = query.filter(WorkLog.project_name.in_(projects))
        
        if annotators:
            query = query.filter(WorkLog.annotator_name.in_(annotators))
        
        result = query.first()
        
        return {
            'total_images': result.total_images or 0,
            'total_hours': round(result.total_hours or 0, 2),
            'annotator_count': result.annotator_count or 0,
            'total_entries': result.total_entries or 0
        }

    @staticmethod
    def get_annotator_summary(
        db: Session,
        date: str,
        projects: Optional[List[str]] = None,
        annotators: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Get summary grouped by annotator."""
        query = db.query(
            WorkLog.annotator_name,
            func.sum(WorkLog.images_done).label('total_images'),
            func.sum(WorkLog.hours_spent).label('total_hours'),
            func.count(WorkLog.id).label('entries_count')
        ).filter(WorkLog.date == date)
        
        if projects:
            query = query.filter(WorkLog.project_name.in_(projects))
        
        if annotators:
            query = query.filter(WorkLog.annotator_name.in_(annotators))
        
        results = query.group_by(WorkLog.annotator_name).order_by(
            func.sum(WorkLog.images_done).desc()
        ).all()
        
        return [
            {
                'annotator_name': r.annotator_name,
                'total_images': r.total_images or 0,
                'total_hours': round(r.total_hours or 0, 2),
                'entries_count': r.entries_count or 0
            }
            for r in results
        ]

    @staticmethod
    def get_project_summary(
        db: Session,
        date: str,
        projects: Optional[List[str]] = None,
        annotators: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Get summary grouped by project."""
        query = db.query(
            WorkLog.project_name,
            func.sum(WorkLog.images_done).label('total_images'),
            func.sum(WorkLog.hours_spent).label('total_hours'),
            func.count(WorkLog.id).label('entries_count')
        ).filter(WorkLog.date == date)
        
        if projects:
            query = query.filter(WorkLog.project_name.in_(projects))
        
        if annotators:
            query = query.filter(WorkLog.annotator_name.in_(annotators))
        
        results = query.group_by(WorkLog.project_name).order_by(
            func.sum(WorkLog.images_done).desc()
        ).all()
        
        return [
            {
                'project_name': r.project_name,
                'total_images': r.total_images or 0,
                'total_hours': round(r.total_hours or 0, 2),
                'entries_count': r.entries_count or 0
            }
            for r in results
        ]

    @staticmethod
    def get_challenges_and_suggestions(
        db: Session,
        date: str,
        projects: Optional[List[str]] = None,
        annotators: Optional[List[str]] = None
    ) -> List[WorkLog]:
        """Get logs that have challenges or suggestions."""
        query = db.query(WorkLog).filter(
            WorkLog.date == date
        ).filter(
            (WorkLog.challenges != "") | (WorkLog.suggestions != "")
        )
        
        if projects:
            query = query.filter(WorkLog.project_name.in_(projects))
        
        if annotators:
            query = query.filter(WorkLog.annotator_name.in_(annotators))
        
        return query.order_by(WorkLog.created_at.desc()).all()

    @staticmethod
    def get_distinct_annotators(db: Session, date: Optional[str] = None) -> List[str]:
        """Get distinct annotator names."""
        query = db.query(distinct(WorkLog.annotator_name))
        if date:
            query = query.filter(WorkLog.date == date)
        results = query.order_by(WorkLog.annotator_name).all()
        return [r[0] for r in results]

    @staticmethod
    def get_distinct_projects(db: Session, date: Optional[str] = None) -> List[str]:
        """Get distinct project names."""
        query = db.query(distinct(WorkLog.project_name))
        if date:
            query = query.filter(WorkLog.date == date)
        results = query.order_by(WorkLog.project_name).all()
        return [r[0] for r in results]

    @staticmethod
    def get_distinct_dates(db: Session) -> List[str]:
        """Get all distinct dates with data."""
        results = db.query(distinct(WorkLog.date)).order_by(WorkLog.date.desc()).all()
        return [r[0] for r in results]

