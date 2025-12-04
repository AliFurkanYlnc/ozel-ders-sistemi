import uuid
from datetime import datetime
from datetime import time as time_type

from app.extensions import db


class AvailabilitySlot(db.Model):
    __tablename__ = "availability_slots"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    user = db.relationship(
        "User", backref=db.backref("availability_slots", lazy="dynamic"), uselist=False
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "day_of_week": self.day_of_week,
            "start_time": self.start_time.strftime("%H:%M") if isinstance(self.start_time, time_type) else None,
            "end_time": self.end_time.strftime("%H:%M") if isinstance(self.end_time, time_type) else None,
            "user_id": self.user_id,
        }
