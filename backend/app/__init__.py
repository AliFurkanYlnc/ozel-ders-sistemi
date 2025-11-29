from flask import Flask

from app.api import register_blueprints
from app.config import Config
from app.extensions import db, jwt, migrate


def create_app(config_class: type | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class or Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    register_blueprints(app)

    return app
