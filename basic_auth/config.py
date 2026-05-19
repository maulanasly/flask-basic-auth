import os
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

load_dotenv()


class BaseConfig(object):
    ADMINS = []
    DEBUG = True
    TESTING = False
    VERBOSE = False
    PROPAGATE_EXCEPTIONS = True

    SENTRY_DSN = os.getenv("SENTRY_DSN", "")
    SENTRY_RELEASE = os.getenv("SENTRY_RELEASE", "v0.1-rc1")
    APP_SECRET = os.getenv("APP_SECRET", "basic_auth")

    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "")
    GOOGLE_ID = os.getenv("GOOGLE_ID", "")
    GOOGLE_SECRET = os.getenv("GOOGLE_SECRET", "")


class DevelopmentConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = ''


class StagingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = ''


class ProductionConfig(BaseConfig):
    pass


config = {
    "development": "basic_auth.config.DevelopmentConfig",
    "testing": "basic_auth.config.TestingConfig",
    "staging": "basic_auth.config.StagingConfig",
    "production": "basic_auth.config.ProductionConfig"
}
