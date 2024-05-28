import os


class JWTConfig:
    SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    ALGORITHM = 'HS256'
    EXPIRATION_DELTA = 60 * 60
