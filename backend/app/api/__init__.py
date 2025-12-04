from flask import Blueprint, Flask


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
students_bp = Blueprint("students", __name__, url_prefix="/students")
tutors_bp = Blueprint("tutors", __name__, url_prefix="/tutors")
availability_bp = Blueprint("availability", __name__, url_prefix="/availability")
lesson_requests_bp = Blueprint("lesson_requests", __name__, url_prefix="/lesson-requests")
lessons_bp = Blueprint("lessons", __name__, url_prefix="/lessons")


def register_blueprints(app: Flask) -> None:
    from app.api import auth, availability, lesson_requests, lessons, students, tutors  # noqa: F401

    app.register_blueprint(auth_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(tutors_bp)
    app.register_blueprint(availability_bp)
    app.register_blueprint(lesson_requests_bp)
    app.register_blueprint(lessons_bp)
