class DebugConfig:

    SQLALCHEMY_DATABASE_URI = "sqlite:///debug.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "ozama123"

    ROUTES = [
        'home',
        'webhooks',
        'auth'
    ]