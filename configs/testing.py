from configs.base import BaseConfig


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///ticket_system_test.db'
    DEBUG = True
    TESTING = True
