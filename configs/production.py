from configs.base import BaseConfig


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/ticket_system'
    DEBUG = False
    TESTING = False
