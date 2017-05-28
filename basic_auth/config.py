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
    GOOGLE_ID = "cloud.google.com/console and get your ID"
    GOOGLE_SECRET = "cloud.google.com/console and get the secret"


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://basic_auth:eJTy5mn7shrHmU9c@localhost/basic_auth'
    GOOGLE_ID = "898576985793-1oaem52t1huruq0k1s6hirvc91ulpm5k.apps.googleusercontent.com"
    GOOGLE_SECRET = "dflBTM76uotZw6NZh0rhQP-z"


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
