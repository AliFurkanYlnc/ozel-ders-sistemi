import uuid

from app.extensions import db


class TutorSubject(db.Model):
    __tablename__ = "tutor_subjects"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tutor_id = db.Column(db.String(36), db.ForeignKey("tutor_profiles.id"), nullable=False)
    subject_id = db.Column(db.String(36), db.ForeignKey("subjects.id"), nullable=False)

    tutor = db.relationship(
        "TutorProfile",
        back_populates="tutor_subject_associations",
        overlaps="subjects",
    )
    subject = db.relationship(
        "Subject",
        back_populates="subject_tutor_associations",
        overlaps="tutors",
    )


class TutorDistrict(db.Model):
    __tablename__ = "tutor_districts"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tutor_id = db.Column(db.String(36), db.ForeignKey("tutor_profiles.id"), nullable=False)
    district = db.Column(db.String(100), nullable=False)

    tutor = db.relationship("TutorProfile", back_populates="districts")
