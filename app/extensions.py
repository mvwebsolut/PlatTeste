from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

database = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
marshmallow = Marshmallow()