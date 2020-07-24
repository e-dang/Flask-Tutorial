import os
from dotenv import load_dotenv

load_dotenv()


class DevConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')


class SQLiteTestConfig:
    TESTING = True
    SECRET_KEY = 'testing'
    SQLALCHEMY_DATABASE_URI = 'sqlite://'  # in memory database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOGIN_DISABLED = True
    WTF_CSRF_ENABLED = False


class PostgreSQLTestConfig(SQLiteTestConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')  # postgres database from docker-compose


class HerokuConfig(DevConfig):
    SECRET_KEY = os.environ.get('SECURE_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


configs = {
    'dev': DevConfig,
    'sqlite_test': SQLiteTestConfig,
    'postgres_test': PostgreSQLTestConfig,
    'heroku': HerokuConfig
}
