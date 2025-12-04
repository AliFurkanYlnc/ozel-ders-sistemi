import uuid
from datetime import datetime

from app.extensions import db

ALLOWED_LESSON_STATUSES = {"pending", "confirmed", "completed", "cancelled"}
ALLOWED_LESSON_MODES = {"online", "student_home", "tutor_home", "common_place"}


class Lesson(db.Model):
    __tablename__ = "lessons"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tutor_id = db.Column(db.String(36), db.ForeignKey("tutor_profiles.id"), nullable=False)
    student_id = db.Column(
        db.String(36), db.ForeignKey("student_profiles.id"), nullable=False
    )
    subject_id = db.Column(db.String(36), db.ForeignKey("subjects.id"), nullable=False)
    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=False)
    mode = db.Column(db.String(50), nullable=False)
    location_description = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), default="pending", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    student = db.relationship("StudentProfile", backref=db.backref("lessons", lazy="dynamic"))
    tutor = db.relationship("TutorProfile", backref=db.backref("lessons", lazy="dynamic"))
    subject = db.relationship("Subject", backref=db.backref("lessons", lazy="dynamic"))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "student_id": self.student_id,
            "tutor_id": self.tutor_id,
            "subject_id": self.subject_id,
            "start_datetime": self.start_datetime.isoformat() if self.start_datetime else None,
            "end_datetime": self.end_datetime.isoformat() if self.end_datetime else None,
            "mode": self.mode,
            "location_description": self.location_description,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
