from flask import Blueprint, jsonify

from app.api import subjects_bp
from app.models import Subject


# Blueprint imported from app.api to ensure shared registration
assert isinstance(subjects_bp, Blueprint)


def _serialize_subject(subject: Subject) -> dict:
    return {
        "id": subject.id,
        "name": subject.name,
        "category": subject.category,
        "order_index": subject.order_index,
    }


@subjects_bp.route("/", methods=["GET"])
def list_subjects():
    subjects = Subject.query.order_by(
        Subject.order_index.asc().nulls_last(), Subject.id.asc()
    ).all()
    return jsonify([_serialize_subject(subject) for subject in subjects])


@subjects_bp.route("/<int:subject_id>", methods=["GET"])
def get_subject(subject_id: int):
    subject = Subject.query.get_or_404(subject_id)
    return jsonify(_serialize_subject(subject))
