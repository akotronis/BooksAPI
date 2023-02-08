import os
import secrets


basedir = os.path.abspath(os.path.dirname(__name__))


class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_TITLE = 'BookAPI'
    API_VERSION = 'v1'
    OPENAPI_VERSION = '3.0.2'
    # Required for ordered=True to work in Schemas Meta classes
    JSON_SORT_KEYS = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('PROD_DATABASE_URL')
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL') or f"sqlite:///{os.path.join(basedir, 'data.db')}"
    JWT_SECRET_KEY = secrets.token_urlsafe(32)
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL') or f"sqlite:///{os.path.join(basedir, 'test-data.db')}"
    JWT_SECRET_KEY = secrets.token_urlsafe(32)
    SQLALCHEMY_ECHO = False


config_by_name = dict(
    prod=ProductionConfig,
    dev=DevelopmentConfig,
    test=TestingConfig,
)