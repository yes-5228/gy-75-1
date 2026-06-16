from pathlib import Path

from flask import Flask
from flask_cors import CORS

from app.config import Config
from app.extensions import db
from app.routes import register_blueprints
from app.seed import seed_data


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})
    db.init_app(app)
    register_blueprints(app)

    with app.app_context():
        db.create_all()
        seed_data()

    @app.get("/api/health")
    def health_check():
        return {"status": "ok", "service": "elevator-maintenance-api"}

    return app
