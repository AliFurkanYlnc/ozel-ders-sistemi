from typing import List, Tuple

from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt, jwt_required

from app.extensions import db
from app.models import AvailabilitySlot, LessonRequest, StudentProfile, TutorProfile
from app.models.relationships import TutorDistrict, TutorSubject
from app.models.subject import Subject

matching_bp = Blueprint("matching", __name__, url_prefix="/matching")


def parse_csv_to_list_int(value: str) -> List[int]:
    items: List[int] = []
    if not value:
        return items
    for raw_item in value.split(","):
        item = raw_item.strip()
        if not item:
            continue
        try:
            items.append(int(item))
        except ValueError:
            continue
    return items


def parse_csv_to_list_str(value: str) -> List[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def csv_contains(value: str, item: str) -> bool:
    if not value or not item:
        return False
    return item in [entry.strip() for entry in value.split(",") if entry.strip()]


def find_overlapping_slots(
    student_slots: List[AvailabilitySlot],
    tutor_slots: List[AvailabilitySlot],
) -> Tuple[bool, List[dict]]:
    overlaps = []
    for student_slot in student_slots:
        for tutor_slot in tutor_slots:
            if student_slot.day_of_week != tutor_slot.day_of_week:
                continue
            if student_slot.start_time < tutor_slot.end_time and tutor_slot.start_time < student_slot.end_time:
                overlaps.append(
                    {
                        "day_of_week": student_slot.day_of_week,
                        "student_start_time": student_slot.start_time.isoformat(),
                        "student_end_time": student_slot.end_time.isoformat(),
                        "tutor_start_time": tutor_slot.start_time.isoformat(),
                        "tutor_end_time": tutor_slot.end_time.isoformat(),
                    }
                )
            if len(overlaps) >= 3:
                break
        if len(overlaps) >= 3:
            break
    return bool(overlaps), overlaps


@matching_bp.route("/lesson-requests/<request_id>/match", methods=["POST"])
@jwt_required()
def match_tutors(request_id):
    claims = get_jwt()
    role = claims.get("role")
    if role not in {"student", "admin"}:
        return jsonify({"message": "Forbidden"}), 403

    user_id = claims.get("sub") or claims.get("user_id")

    lesson_request = LessonRequest.query.filter_by(id=request_id).first()
    if not lesson_request:
        return jsonify({"message": "LessonRequest not found"}), 404

    student_profile: StudentProfile = lesson_request.student
    if role == "student" and student_profile.user_id != user_id:
        return jsonify({"message": "Forbidden"}), 403

    student_slots = AvailabilitySlot.query.filter_by(user_id=student_profile.user_id).all()
    subject_ids = parse_csv_to_list_int(lesson_request.subject_ids)
    preferred_modes = parse_csv_to_list_str(lesson_request.preferred_modes)

    if not subject_ids:
        return jsonify({"message": "No subjects specified for matching"}), 400

    tutor_query = (
        TutorProfile.query.join(TutorSubject, TutorProfile.id == TutorSubject.tutor_id)
        .filter(TutorProfile.status == "approved")
        .filter(TutorSubject.subject_id.in_(subject_ids))
        .distinct()
    )

    candidate_tutors: List[TutorProfile] = tutor_query.all()

    in_person_modes = {"student_home", "tutor_home", "common_place"}
    requested_in_person = set(preferred_modes) & in_person_modes

    filtered_tutors = []
    for tutor in candidate_tutors:
        tutor_modes = parse_csv_to_list_str(tutor.lesson_modes)
        if preferred_modes and not set(tutor_modes) & set(preferred_modes):
            continue

        if requested_in_person:
            district_match = tutor.base_district == student_profile.district
            if not district_match:
                district_match = TutorDistrict.query.filter_by(
                    tutor_id=tutor.id, district=student_profile.district
                ).first()
            if not district_match:
                continue

        filtered_tutors.append(tutor)

    results = []
    for tutor in filtered_tutors:
        tutor_slots = AvailabilitySlot.query.filter_by(user_id=tutor.user_id).all()
        has_overlap, suggested_slots = find_overlapping_slots(student_slots, tutor_slots)

        score = 50.0
        if tutor.base_district == student_profile.district:
            score += 30
        else:
            district_entry = TutorDistrict.query.filter_by(
                tutor_id=tutor.id, district=student_profile.district
            ).first()
            if district_entry:
                score += 20

        budget_min = float(lesson_request.budget_min) if lesson_request.budget_min is not None else None
        budget_max = float(lesson_request.budget_max) if lesson_request.budget_max is not None else None
        if budget_min is not None and budget_max is not None and tutor.hourly_rate is not None:
            hourly_rate = float(tutor.hourly_rate)
            if budget_min <= hourly_rate <= budget_max:
                score += 20
            else:
                lower_bound = budget_min * 0.8
                upper_bound = budget_max * 1.2
                if lower_bound <= hourly_rate <= upper_bound:
                    score += 5

        if has_overlap:
            score += 20

        if tutor.avg_rating is not None and tutor.rating_count is not None:
            if tutor.avg_rating >= 4.5 and tutor.rating_count >= 5:
                score += 10
            elif tutor.avg_rating >= 4.0 and tutor.rating_count >= 3:
                score += 5

        tutor_subjects = (
            db.session.query(Subject)
            .join(TutorSubject, Subject.id == TutorSubject.subject_id)
            .filter(TutorSubject.tutor_id == tutor.id, TutorSubject.subject_id.in_(subject_ids))
            .all()
        )

        results.append(
            {
                "tutor_id": tutor.id,
                "full_name": tutor.full_name,
                "title": tutor.title,
                "hourly_rate": float(tutor.hourly_rate) if tutor.hourly_rate is not None else None,
                "base_district": tutor.base_district,
                "avg_rating": tutor.avg_rating,
                "rating_count": tutor.rating_count,
                "score": score,
                "subjects": [
                    {"id": subject.id, "name": subject.name, "category": subject.category}
                    for subject in tutor_subjects
                ],
                "has_availability_overlap": has_overlap,
                "suggested_slots": suggested_slots,
            }
        )

    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)
    return jsonify(sorted_results[:10])
