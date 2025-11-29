import uuid
from datetime import datetime

from app.extensions import db


class StudentProfile(db.Model):
    __tablename__ = "student_profiles"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), unique=True, nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    grade = db.Column(db.String(50))
    target_exam = db.Column(db.String(50))
    target_score = db.Column(db.Integer)
    target_rank = db.Column(db.Integer)
    city = db.Column(db.String(100), default="Istanbul", nullable=False)
    district = db.Column(db.String(100), nullable=False)
    neighborhood = db.Column(db.String(100))
    preferred_modes = db.Column(db.String(255))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    user = db.relationship(
        "User", backref=db.backref("student_profile", uselist=False), uselist=False
    )
