from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, jwt_required

from app.api import availability_bp
from app.extensions import db
from app.models import AvailabilitySlot

# Blueprint imported from app.api to ensure shared registration
assert isinstance(availability_bp, Blueprint)


def _parse_time(value: str):
    try:
        return datetime.strptime(value, "%H:%M").time()
    except (TypeError, ValueError):
        return None


def _serialize_slot(slot: AvailabilitySlot) -> dict:
    return {
        "id": slot.id,
        "day_of_week": slot.day_of_week,
        "start_time": slot.start_time.strftime("%H:%M") if slot.start_time else None,
        "end_time": slot.end_time.strftime("%H:%M") if slot.end_time else None,
    }


@availability_bp.route("/me", methods=["GET"])
@jwt_required()
def list_my_availability():
    claims = get_jwt()
    user_id = claims.get("sub") or claims.get("user_id")

    slots = AvailabilitySlot.query.filter_by(user_id=user_id).all()
    return jsonify([_serialize_slot(slot) for slot in slots])


@availability_bp.route("", methods=["POST"])
@jwt_required()
def create_availability():
    claims = get_jwt()
    user_id = claims.get("sub") or claims.get("user_id")
    data = request.get_json() or {}

    day_of_week = data.get("day_of_week")
    start_time = _parse_time(data.get("start_time"))
    end_time = _parse_time(data.get("end_time"))

    errors = {}
    if day_of_week is None or not isinstance(day_of_week, int) or not 0 <= day_of_week <= 6:
        errors["day_of_week"] = "Must be an integer between 0 and 6."
    if not start_time:
        errors["start_time"] = "Invalid start_time format. Use HH:MM."
    if not end_time:
        errors["end_time"] = "Invalid end_time format. Use HH:MM."
    if start_time and end_time and end_time <= start_time:
        errors["time_range"] = "end_time must be greater than start_time."

    if errors:
        return jsonify({"message": "Invalid data", "errors": errors}), 400

    slot = AvailabilitySlot(
        user_id=user_id,
        day_of_week=day_of_week,
        start_time=start_time,
        end_time=end_time,
    )
    db.session.add(slot)
    db.session.commit()

    return jsonify(_serialize_slot(slot)), 201


@availability_bp.route("/<slot_id>", methods=["PUT"])
@jwt_required()
def update_availability(slot_id):
    claims = get_jwt()
    user_id = claims.get("sub") or claims.get("user_id")
    data = request.get_json() or {}

    slot = AvailabilitySlot.query.filter_by(id=slot_id, user_id=user_id).first()
    if not slot:
        return jsonify({"message": "Not found"}), 404

    errors = {}

    if "day_of_week" in data:
        day_of_week = data.get("day_of_week")
        if day_of_week is None or not isinstance(day_of_week, int) or not 0 <= day_of_week <= 6:
            errors["day_of_week"] = "Must be an integer between 0 and 6."
        else:
            slot.day_of_week = day_of_week

    if "start_time" in data:
        parsed_start = _parse_time(data.get("start_time"))
        if not parsed_start:
            errors["start_time"] = "Invalid start_time format. Use HH:MM."
        else:
            slot.start_time = parsed_start

    if "end_time" in data:
        parsed_end = _parse_time(data.get("end_time"))
        if not parsed_end:
            errors["end_time"] = "Invalid end_time format. Use HH:MM."
        else:
            slot.end_time = parsed_end

    if slot.start_time and slot.end_time and slot.end_time <= slot.start_time:
        errors["time_range"] = "end_time must be greater than start_time."

    if errors:
        return jsonify({"message": "Invalid data", "errors": errors}), 400

    db.session.commit()
    return jsonify(_serialize_slot(slot))


@availability_bp.route("/<slot_id>", methods=["DELETE"])
@jwt_required()
def delete_availability(slot_id):
    claims = get_jwt()
    user_id = claims.get("sub") or claims.get("user_id")

    slot = AvailabilitySlot.query.filter_by(id=slot_id, user_id=user_id).first()
    if not slot:
        return jsonify({"message": "Not found"}), 404

    db.session.delete(slot)
    db.session.commit()
    return jsonify({"message": "Deleted"}), 200
