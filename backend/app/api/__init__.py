from flask import Blueprint, Flask


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
students_bp = Blueprint("students", __name__, url_prefix="/students")
tutors_bp = Blueprint("tutors", __name__, url_prefix="/tutors")


def register_blueprints(app: Flask) -> None:
    from app.api import auth, students, tutors  # noqa: F401

    app.register_blueprint(auth_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(tutors_bp)
