import os

import app.settings as settings


class Config(object):
    PYLTI_CONFIG = settings.PYLTI_CONFIG


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    PYLTI_CONFIG = settings.PYLTI_CONFIG


def make_database_uri() -> str:
    db_user = os.getenv("DB_USERNAME")
    db_pass = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")
    unix_socket_path = os.getenv("DB_INSTANCE_UNIX_SOCKET")

    database_uri = f"postgresql+psycopg2://{db_user}:{db_pass}@/{db_name}?host={unix_socket_path}"

    return database_uri

class DevelopmentConfig(BaseConfig):
    db_pass = os.getenv("DB_PASSWORD")
    username = os.getenv("DB_USERNAME")
    SECRET_KEY = os.getenv("SECRET_FLASK")
    DEBUG = True
    TESTING = True
    PYLTI_CONFIG = settings.PYLTI_CONFIG
    SQLALCHEMY_DATABASE_URI = make_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "None"
    REDIS_URL = os.getenv("REDIS_URL")
    PREFERRED_URL_SCHEME = "https"
    CANVAS_API_URL = os.environ.get("CANVAS_API_URL")  # maybe move
    CANVAS_API_KEY = os.environ.get("CANVAS_API_KEY")  # maybe move


class StageConfig(BaseConfig):
    db_pass = os.getenv("DB_PASSWORD")
    username = "TheDoctor"
    SECRET_KEY = os.getenv("SECRET_FLASK")
    DEBUG = False
    TESTING = False
    PYLTI_CONFIG = settings.PYLTI_CONFIG
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "None"
    REDIS_URL = os.getenv("REDIS_URL")


class ProductionConfig(BaseConfig):
    db_pass = os.getenv("DB_PASSWORD")
    username = os.getenv("DB_USERNAME")
    SECRET_KEY = os.getenv("SECRET_FLASK")
    DEBUG = False
    TESTING = False
    PYLTI_CONFIG = settings.PYLTI_CONFIG
    SQLALCHEMY_DATABASE_URI = make_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "None"
    REDIS_URL = os.getenv("REDIS_URL")


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    PYLTI_CONFIG = settings.PYLTI_CONFIG


configuration = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "stage": StageConfig,
}
