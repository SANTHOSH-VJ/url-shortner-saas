import os
from flask import Flask
from .config import Config
from .extensions import db, migrate, login_manager, cors
from .errors import register_error_handlers
from .logging_config import configure_logging


def create_app(config_class: type[Config] | None = None) -> Flask:
    app = Flask(__name__, static_folder=None)

    app.config.from_object(config_class or Config())

    configure_logging()
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    # Blueprints
    from .api import api_bp
    from .auth import auth_bp
    from .web import web_bp
    app.register_blueprint(api_bp, url_prefix="/api/v1")
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(web_bp)

    # Health check
    @app.get("/health")
    def health_check():
        return {"status": "ok"}

    register_error_handlers(app)

    return app


