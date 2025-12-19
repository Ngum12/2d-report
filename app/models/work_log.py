from sqlalchemy import Column, Integer, String, Float, Text, Index
from app.database import Base


class WorkLog(Base):
    __tablename__ = "work_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String(10), nullable=False, index=True)  # YYYY-MM-DD
    annotator_name = Column(String(100), nullable=False, index=True)
    project_name = Column(String(200), nullable=False, index=True)
    task_type = Column(String(50), nullable=False)
    images_done = Column(Integer, nullable=False, default=0)
    hours_spent = Column(Float, nullable=False, default=0.0)
    status = Column(String(50), nullable=False)
    challenges = Column(Text, nullable=True)
    suggestions = Column(Text, nullable=True)
    extra_notes = Column(Text, nullable=True)
    created_at = Column(String(30), nullable=False)  # ISO datetime

    __table_args__ = (
        Index('ix_work_logs_date_annotator', 'date', 'annotator_name'),
    )

    def __repr__(self):
        return f"<WorkLog(id={self.id}, date={self.date}, annotator={self.annotator_name})>"

