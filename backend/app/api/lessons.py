from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, jwt_required

from app.api import lessons_bp
from app.extensions import db
from app.models import Lesson, StudentProfile, Subject, TutorProfile
from app.models.lesson import ALLOWED_LESSON_MODES, ALLOWED_LESSON_STATUSES

# Blueprint imported from app.api to ensure shared registration
assert isinstance(lessons_bp, Blueprint)


def _parse_iso_datetime(value: str):
    if not value:
        return None
    try:
        if isinstance(value, str) and value.endswith("Z"):
            value = value.replace("Z", "+00:00")
        return datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return None


def _get_current_student():
    claims = get_jwt()
    if claims.get("role") != "student":
        return None
    user_id = claims.get("sub") or claims.get("user_id")
    return StudentProfile.query.filter_by(user_id=user_id).first()


def _get_current_tutor():
    claims = get_jwt()
    if claims.get("role") != "tutor":
        return None
    user_id = claims.get("sub") or claims.get("user_id")
    return TutorProfile.query.filter_by(user_id=user_id).first()


def _serialize_lesson(lesson: Lesson) -> dict:
    data = lesson.to_dict()
    if lesson.subject:
        data["subject_name"] = lesson.subject.name
    if lesson.tutor:
        data["tutor_name"] = lesson.tutor.full_name
    if lesson.student:
        data["student_name"] = lesson.student.full_name
    return data


@lessons_bp.route("/me", methods=["GET"])
@jwt_required()
def list_my_lessons():
    claims = get_jwt()
    role = claims.get("role")

    if role == "student":
        student = _get_current_student()
        if not student:
            return jsonify({"message": "Student profile not found"}), 404
        lessons = Lesson.query.filter_by(student_id=student.id).all()
    elif role == "tutor":
        tutor = _get_current_tutor()
        if not tutor:
            return jsonify({"message": "Tutor profile not found"}), 404
        lessons = Lesson.query.filter_by(tutor_id=tutor.id).all()
    elif role == "admin":
        lessons = Lesson.query.all()
    else:
        return jsonify({"message": "Forbidden"}), 403

    return jsonify([_serialize_lesson(lesson) for lesson in lessons])


@lessons_bp.route("", methods=["POST"])
@jwt_required()
def create_lesson():
    claims = get_jwt()
    if claims.get("role") != "student":
        return jsonify({"message": "Forbidden"}), 403

    student = _get_current_student()
    if not student:
        return jsonify({"message": "Student profile not found"}), 404

    data = request.get_json() or {}

    tutor_id = data.get("tutor_id")
    subject_id = data.get("subject_id")
    start_datetime = _parse_iso_datetime(data.get("start_datetime"))
    end_datetime = _parse_iso_datetime(data.get("end_datetime"))
    mode = data.get("mode")
    location_description = data.get("location_description")

    errors = {}
    tutor = TutorProfile.query.get(tutor_id) if tutor_id else None
    subject = Subject.query.get(subject_id) if subject_id else None

    if not tutor:
        errors["tutor_id"] = "Invalid tutor_id."
    if not subject:
        errors["subject_id"] = "Invalid subject_id."
    if not start_datetime:
        errors["start_datetime"] = "Invalid start_datetime format."
    if not end_datetime:
        errors["end_datetime"] = "Invalid end_datetime format."
    if start_datetime and end_datetime and end_datetime <= start_datetime:
        errors["time_range"] = "end_datetime must be greater than start_datetime."
    if mode not in ALLOWED_LESSON_MODES:
        errors["mode"] = "Invalid mode."

    if errors:
        return jsonify({"message": "Invalid data", "errors": errors}), 400

    lesson = Lesson(
        tutor_id=tutor.id,
        student_id=student.id,
        subject_id=subject.id,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        mode=mode,
        location_description=location_description,
        status="pending",
    )

    db.session.add(lesson)
    db.session.commit()

    return jsonify(_serialize_lesson(lesson)), 201


@lessons_bp.route("/<lesson_id>", methods=["PATCH"])
@jwt_required()
def update_lesson(lesson_id):
    claims = get_jwt()
    role = claims.get("role")

    lesson = Lesson.query.get(lesson_id)
    if not lesson:
        return jsonify({"message": "Not found"}), 404

    tutor = None
    if role == "tutor":
        tutor = _get_current_tutor()
        if not tutor:
            return jsonify({"message": "Tutor profile not found"}), 404
        if lesson.tutor_id != tutor.id:
            return jsonify({"message": "Not found"}), 404
    elif role != "admin":
        return jsonify({"message": "Forbidden"}), 403

    data = request.get_json() or {}
    errors = {}

    if "status" in data:
        status = data.get("status")
        if status not in ALLOWED_LESSON_STATUSES:
            errors["status"] = "Invalid status."
        else:
            lesson.status = status

    if "start_datetime" in data:
        parsed_start = _parse_iso_datetime(data.get("start_datetime"))
        if not parsed_start:
            errors["start_datetime"] = "Invalid start_datetime format."
        else:
            lesson.start_datetime = parsed_start

    if "end_datetime" in data:
        parsed_end = _parse_iso_datetime(data.get("end_datetime"))
        if not parsed_end:
            errors["end_datetime"] = "Invalid end_datetime format."
        else:
            lesson.end_datetime = parsed_end

    if lesson.start_datetime and lesson.end_datetime and lesson.end_datetime <= lesson.start_datetime:
        errors["time_range"] = "end_datetime must be greater than start_datetime."

    if "location_description" in data:
        lesson.location_description = data.get("location_description")

    if errors:
        return jsonify({"message": "Invalid data", "errors": errors}), 400

    db.session.commit()
    return jsonify(_serialize_lesson(lesson))


@lessons_bp.route("/<lesson_id>", methods=["GET"])
@jwt_required()
def get_lesson(lesson_id):
    claims = get_jwt()
    role = claims.get("role")
    user_id = claims.get("sub") or claims.get("user_id")

    lesson = Lesson.query.get(lesson_id)
    if not lesson:
        return jsonify({"message": "Not found"}), 404

    student = StudentProfile.query.filter_by(user_id=user_id).first()
    tutor = TutorProfile.query.filter_by(user_id=user_id).first()

    if role == "student" and student and lesson.student_id != student.id:
        return jsonify({"message": "Forbidden"}), 403
    if role == "tutor" and tutor and lesson.tutor_id != tutor.id:
        return jsonify({"message": "Forbidden"}), 403
    if role not in {"student", "tutor", "admin"}:
        return jsonify({"message": "Forbidden"}), 403

    return jsonify(_serialize_lesson(lesson))
