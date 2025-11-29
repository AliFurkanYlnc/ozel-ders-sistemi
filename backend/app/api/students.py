from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, jwt_required

from app.api import students_bp
from app.extensions import db
from app.models import StudentProfile


# Blueprint imported from app.api to ensure shared registration
assert isinstance(students_bp, Blueprint)


def _serialize_student(profile: StudentProfile) -> dict:
    preferred_modes = (
        profile.preferred_modes.split(",") if profile.preferred_modes else []
    )
    return {
        "id": profile.id,
        "user_id": profile.user_id,
        "full_name": profile.full_name,
        "grade": profile.grade,
        "target_exam": profile.target_exam,
        "target_score": profile.target_score,
        "target_rank": profile.target_rank,
        "city": profile.city,
        "district": profile.district,
        "neighborhood": profile.neighborhood,
        "preferred_modes": preferred_modes,
        "notes": profile.notes,
        "created_at": profile.created_at.isoformat() if profile.created_at else None,
        "updated_at": profile.updated_at.isoformat() if profile.updated_at else None,
    }


@students_bp.route("/me", methods=["GET"])
@jwt_required()
def get_me():
    claims = get_jwt()
    role = claims.get("role")
    if role != "student":
        return jsonify({"message": "Forbidden"}), 403

    user_id = claims.get("sub") or claims.get("user_id")
    profile = StudentProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        return jsonify({"message": "Profile not found"}), 404

    return jsonify({"profile": _serialize_student(profile)})


@students_bp.route("/me", methods=["POST"])
@jwt_required()
def upsert_me():
    claims = get_jwt()
    role = claims.get("role")
    if role != "student":
        return jsonify({"message": "Forbidden"}), 403

    user_id = claims.get("sub") or claims.get("user_id")
    data = request.get_json() or {}

    profile = StudentProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        profile = StudentProfile(user_id=user_id)
        db.session.add(profile)

    preferred_modes = data.get("preferred_modes")
    if isinstance(preferred_modes, list):
        preferred_modes_str = ",".join(preferred_modes)
    else:
        preferred_modes_str = preferred_modes

    for field in [
        "full_name",
        "grade",
        "target_exam",
        "target_score",
        "target_rank",
        "city",
        "district",
        "neighborhood",
        "notes",
    ]:
        if field in data:
            setattr(profile, field, data.get(field))

    if preferred_modes_str is not None:
        profile.preferred_modes = preferred_modes_str

    if not profile.full_name or not profile.district:
        return jsonify({"message": "Full name and district are required."}), 400

    db.session.commit()

    return jsonify({"profile": _serialize_student(profile)})
