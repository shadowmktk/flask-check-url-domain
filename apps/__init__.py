from flask import Flask
from config import config_map
from apps.extensions import register_sqlalchemy
from apps.extensions import register_celery
from apps.router import register_router
from apps.router import register_blueprints
import os

FLASK_APP_ENVIRONMENT = os.environ.get("FLASK_APP_ENVIRONMENT") or "development"

def create_app():
    app = Flask(__name__)
    app.config.from_object(config_map[FLASK_APP_ENVIRONMENT])
    app.json.ensure_ascii = False
    
    register_sqlalchemy(app)
    register_celery(app)
    register_router()
    register_blueprints(app)
    return app
