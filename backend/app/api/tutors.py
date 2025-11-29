from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, jwt_required

from app.api import tutors_bp
from app.extensions import db
from app.models import Subject, TutorDistrict, TutorProfile


# Blueprint imported from app.api to ensure shared registration
assert isinstance(tutors_bp, Blueprint)


def _serialize_tutor(profile: TutorProfile) -> dict:
    lesson_modes = profile.lesson_modes.split(",") if profile.lesson_modes else []
    teaching_levels = (
        profile.teaching_levels.split(",") if profile.teaching_levels else []
    )
    subject_ids = [subject.id for subject in profile.subjects]
    districts = [district.district for district in profile.districts]

    return {
        "id": profile.id,
        "user_id": profile.user_id,
        "full_name": profile.full_name,
        "title": profile.title,
        "bio": profile.bio,
        "education": profile.education,
        "experience_years": profile.experience_years,
        "hourly_rate": float(profile.hourly_rate) if profile.hourly_rate is not None else None,
        "base_city": profile.base_city,
        "base_district": profile.base_district,
        "lesson_modes": lesson_modes,
        "teaching_levels": teaching_levels,
        "status": profile.status,
        "avg_rating": profile.avg_rating,
        "rating_count": profile.rating_count,
        "subject_ids": subject_ids,
        "districts": districts,
        "created_at": profile.created_at.isoformat() if profile.created_at else None,
        "updated_at": profile.updated_at.isoformat() if profile.updated_at else None,
    }


@tutors_bp.route("/me", methods=["GET"])
@jwt_required()
def get_me():
    claims = get_jwt()
    role = claims.get("role")
    if role != "tutor":
        return jsonify({"message": "Forbidden"}), 403

    user_id = claims.get("sub") or claims.get("user_id")
    profile = TutorProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        return jsonify({"message": "Profile not found"}), 404

    return jsonify({"profile": _serialize_tutor(profile)})


@tutors_bp.route("/me", methods=["POST"])
@jwt_required()
def upsert_me():
    claims = get_jwt()
    role = claims.get("role")
    if role != "tutor":
        return jsonify({"message": "Forbidden"}), 403

    user_id = claims.get("sub") or claims.get("user_id")
    data = request.get_json() or {}

    profile = TutorProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        profile = TutorProfile(user_id=user_id)
        db.session.add(profile)

    lesson_modes = data.get("lesson_modes")
    if isinstance(lesson_modes, list):
        lesson_modes_str = ",".join(lesson_modes)
    else:
        lesson_modes_str = lesson_modes

    teaching_levels = data.get("teaching_levels")
    if isinstance(teaching_levels, list):
        teaching_levels_str = ",".join(teaching_levels)
    else:
        teaching_levels_str = teaching_levels

    for field in [
        "full_name",
        "title",
        "bio",
        "education",
        "experience_years",
        "hourly_rate",
        "base_city",
        "base_district",
        "status",
    ]:
        if field in data:
            setattr(profile, field, data.get(field))

    if lesson_modes_str is not None:
        profile.lesson_modes = lesson_modes_str
    if teaching_levels_str is not None:
        profile.teaching_levels = teaching_levels_str

    subject_ids = data.get("subject_ids") or []
    if subject_ids:
        subjects = Subject.query.filter(Subject.id.in_(subject_ids)).all()
    else:
        subjects = []
    profile.subjects = subjects

    districts = data.get("districts") or []
    profile.districts.clear()
    for district_name in districts:
        profile.districts.append(TutorDistrict(district=district_name))

    if not profile.full_name or profile.hourly_rate is None or not profile.base_district:
        return (
            jsonify({"message": "Full name, hourly rate, and base district are required."}),
            400,
        )

    db.session.commit()

    return jsonify({"profile": _serialize_tutor(profile)})
