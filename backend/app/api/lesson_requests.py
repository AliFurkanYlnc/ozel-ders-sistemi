from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, jwt_required

from app.api import lesson_requests_bp
from app.extensions import db
from app.models import LessonRequest, StudentProfile
from app.models.lesson_request import ALLOWED_REQUEST_STATUSES

# Blueprint imported from app.api to ensure shared registration
assert isinstance(lesson_requests_bp, Blueprint)


def _get_current_student_profile():
    claims = get_jwt()
    role = claims.get("role")
    if role != "student":
        return None, (jsonify({"message": "Forbidden"}), 403)

    user_id = claims.get("sub") or claims.get("user_id")
    student = StudentProfile.query.filter_by(user_id=user_id).first()
    if not student:
        return None, (jsonify({"message": "Student profile not found"}), 404)

    return student, None


def _serialize_request(request_obj: LessonRequest) -> dict:
    return request_obj.to_dict()


@lesson_requests_bp.route("/me", methods=["GET"])
@jwt_required()
def list_my_requests():
    student, error_response = _get_current_student_profile()
    if error_response:
        return error_response

    requests = LessonRequest.query.filter_by(student_id=student.id).all()
    return jsonify([_serialize_request(req) for req in requests])


@lesson_requests_bp.route("/<request_id>", methods=["GET"])
@jwt_required()
def get_request(request_id):
    student, error_response = _get_current_student_profile()
    if error_response:
        return error_response

    req = LessonRequest.query.filter_by(id=request_id, student_id=student.id).first()
    if not req:
        return jsonify({"message": "Not found"}), 404

    return jsonify(_serialize_request(req))


@lesson_requests_bp.route("", methods=["POST"])
@jwt_required()
def create_request():
    student, error_response = _get_current_student_profile()
    if error_response:
        return error_response

    data = request.get_json() or {}

    subject_ids = data.get("subject_ids") or []
    preferred_modes = data.get("preferred_modes") or []

    errors = {}
    if not isinstance(subject_ids, list) or not subject_ids:
        errors["subject_ids"] = "subject_ids must be a non-empty list of IDs."

    if errors:
        return jsonify({"message": "Invalid data", "errors": errors}), 400

    lesson_request = LessonRequest(student_id=student.id)
    if isinstance(subject_ids, list):
        lesson_request.set_subject_id_list(subject_ids)
    if isinstance(preferred_modes, list):
        lesson_request.set_preferred_modes(preferred_modes)

    for field in [
        "budget_min",
        "budget_max",
        "weekly_hours",
        "additional_notes",
    ]:
        if field in data:
            setattr(lesson_request, field, data.get(field))

    lesson_request.status = "open"

    db.session.add(lesson_request)
    db.session.commit()

    return jsonify(_serialize_request(lesson_request)), 201


@lesson_requests_bp.route("/<request_id>", methods=["PUT"])
@jwt_required()
def update_request(request_id):
    student, error_response = _get_current_student_profile()
    if error_response:
        return error_response

    data = request.get_json() or {}

    lesson_request = LessonRequest.query.filter_by(
        id=request_id, student_id=student.id
    ).first()
    if not lesson_request:
        return jsonify({"message": "Not found"}), 404

    errors = {}

    if "subject_ids" in data:
        subject_ids = data.get("subject_ids") or []
        if not isinstance(subject_ids, list) or not subject_ids:
            errors["subject_ids"] = "subject_ids must be a non-empty list of IDs."
        else:
            lesson_request.set_subject_id_list(subject_ids)

    if "preferred_modes" in data:
        preferred_modes = data.get("preferred_modes") or []
        if not isinstance(preferred_modes, list):
            errors["preferred_modes"] = "preferred_modes must be a list."
        else:
            lesson_request.set_preferred_modes(preferred_modes)

    if "status" in data:
        status = data.get("status")
        if status not in ALLOWED_REQUEST_STATUSES:
            errors["status"] = "Invalid status."
        else:
            lesson_request.status = status

    for field in [
        "budget_min",
        "budget_max",
        "weekly_hours",
        "additional_notes",
    ]:
        if field in data:
            setattr(lesson_request, field, data.get(field))

    if errors:
        return jsonify({"message": "Invalid data", "errors": errors}), 400

    db.session.commit()
    return jsonify(_serialize_request(lesson_request))


@lesson_requests_bp.route("/<request_id>", methods=["DELETE"])
@jwt_required()
def delete_request(request_id):
    student, error_response = _get_current_student_profile()
    if error_response:
        return error_response

    lesson_request = LessonRequest.query.filter_by(
        id=request_id, student_id=student.id
    ).first()
    if not lesson_request:
        return jsonify({"message": "Not found"}), 404

    db.session.delete(lesson_request)
    db.session.commit()
    return jsonify({"message": "Deleted"}), 200
