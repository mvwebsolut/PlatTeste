from flask import Flask
from importlib import import_module

from config import DebugConfig

from app.extensions import database, login_manager, migrate, marshmallow
from app.template_filters import get_states_from_db

app_config = DebugConfig()

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(app_config)
    load_app_extensions(app)
    load_app_routes(app)
    load_app_template_filters(app)
    return app

def load_app_routes(app: Flask):
    for route in app.config['ROUTES']:
        module = import_module(f"app.routes.{route}")
        app.register_blueprint(module.router)
    return

def load_app_extensions(app: Flask):
    database.init_app(app)
    migrate.init_app(app, database)
    login_manager.init_app(app)
    marshmallow.init_app(app)
    return

def load_app_template_filters(app: Flask):
    app.add_template_filter(get_states_from_db, name="get_states_from_db")




