import uuid
from datetime import datetime

from app.extensions import db


class TutorProfile(db.Model):
    __tablename__ = "tutor_profiles"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), unique=True, nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255))
    bio = db.Column(db.Text)
    education = db.Column(db.String(255))
    experience_years = db.Column(db.Integer, default=0, nullable=False)
    hourly_rate = db.Column(db.Numeric, nullable=False)
    base_city = db.Column(db.String(100), default="Istanbul", nullable=False)
    base_district = db.Column(db.String(100), nullable=False)
    lesson_modes = db.Column(db.String(255))
    teaching_levels = db.Column(db.String(255))
    status = db.Column(db.String(50), default="pending", nullable=False)
    avg_rating = db.Column(db.Float, default=0.0, nullable=False)
    rating_count = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    user = db.relationship(
        "User", backref=db.backref("tutor_profile", uselist=False), uselist=False
    )
    subjects = db.relationship(
        "Subject",
        secondary="tutor_subjects",
        back_populates="tutors",
        overlaps="tutor_subject_associations,subject_tutor_associations",
    )
    tutor_subject_associations = db.relationship(
        "TutorSubject", cascade="all, delete-orphan", back_populates="tutor"
    )
    districts = db.relationship(
        "TutorDistrict", cascade="all, delete-orphan", back_populates="tutor"
    )
