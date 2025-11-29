from flask import Blueprint, Flask


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


def register_blueprints(app: Flask) -> None:
    from app.api import auth  # noqa: F401

    app.register_blueprint(auth_bp)
