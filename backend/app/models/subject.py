import uuid

from app.extensions import db


class Subject(db.Model):
    __tablename__ = "subjects"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), unique=True, nullable=False)
    category = db.Column(db.String(50))
    order_index = db.Column(db.Integer)

    tutors = db.relationship(
        "TutorProfile",
        secondary="tutor_subjects",
        back_populates="subjects",
        overlaps="tutor_subject_associations,subject_tutor_associations",
    )
    subject_tutor_associations = db.relationship(
        "TutorSubject", cascade="all, delete-orphan", back_populates="subject"
    )
