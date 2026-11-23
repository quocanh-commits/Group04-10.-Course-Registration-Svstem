from flask import Flask

from config import Config
from app.extensions import db

def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)
    db.init_app(app)

    from app import models  # noqa: F401  (đăng ký model với SQLAlchemy)
    from app.routes.auth_routes import auth_bp
    from app.routes.student_routes import student_bp
    from app.routes.lecturer_routes import lecturer_bp
    from app.routes.admin_routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(lecturer_bp)
    app.register_blueprint(admin_bp)

    return app
