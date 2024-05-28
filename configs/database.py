import os

from config import basedir


class DatabaseConfig:
    SQLITE = 'sqlite'
    POSTGRESQL = 'postgresql'


class SQLiteConfig:
    DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'app.db')}"


class PostgreSQLConfig:
    DATABASE_URI = os.environ.get('DATABASE_URL')
