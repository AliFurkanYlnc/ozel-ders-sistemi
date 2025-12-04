import uuid
from datetime import datetime
from typing import List

from app.extensions import db

ALLOWED_REQUEST_STATUSES = {"open", "matched", "closed", "cancelled"}


class LessonRequest(db.Model):
    __tablename__ = "lesson_requests"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = db.Column(
        db.String(36), db.ForeignKey("student_profiles.id"), nullable=False
    )
    subject_ids = db.Column(db.Text, nullable=True)
    preferred_modes = db.Column(db.Text, nullable=True)
    budget_min = db.Column(db.Numeric, nullable=True)
    budget_max = db.Column(db.Numeric, nullable=True)
    weekly_hours = db.Column(db.Float, nullable=True)
    additional_notes = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default="open", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    student = db.relationship(
        "StudentProfile", backref=db.backref("lesson_requests", lazy="dynamic")
    )

    def get_subject_id_list(self) -> List[int]:
        if not self.subject_ids:
            return []
        return [int(x) for x in self.subject_ids.split(",") if x]

    def set_subject_id_list(self, ids: List[int]) -> None:
        self.subject_ids = ",".join(str(i) for i in ids)

    def get_preferred_modes(self) -> List[str]:
        if not self.preferred_modes:
            return []
        return [mode for mode in self.preferred_modes.split(",") if mode]

    def set_preferred_modes(self, modes: List[str]) -> None:
        self.preferred_modes = ",".join(modes)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "student_id": self.student_id,
            "subject_ids": self.get_subject_id_list(),
            "preferred_modes": self.get_preferred_modes(),
            "budget_min": float(self.budget_min) if self.budget_min is not None else None,
            "budget_max": float(self.budget_max) if self.budget_max is not None else None,
            "weekly_hours": self.weekly_hours,
            "additional_notes": self.additional_notes,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
