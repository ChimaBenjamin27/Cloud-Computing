from logging import DEBUG


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = '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'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:CloudComputing2021@35.197.198.44/removals'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    DEBUG = True

class ProdConfig(Config):
    pass

class DevConfig(Config):
    DEBUG = True

class TestConfig(Config):
    pass