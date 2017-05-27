class BaseConfig(object):
    ADMINS = []
    DEBUG = True
    TESTING = False
    VERBOSE = False
    PROPAGATE_EXCEPTIONS = True

    SENTRY_DSN = ""
    SENTRY_RELEASE = "v0.1-rc1"
    APP_SECRET = "basic_auth"

    SQLALCHEMY_DATABASE_URI = ''


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://basic_auth:eJTy5mn7shrHmU9c@localhost/basic_auth'


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
