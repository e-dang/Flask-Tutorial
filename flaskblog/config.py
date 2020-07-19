import os
from dotenv import load_dotenv

load_dotenv()


class DevConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')


class HerokuConfig(DevConfig):
    SECRET_KEY = os.environ.get('SECURE_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


configs = {
    'dev': DevConfig,
    'heroku': HerokuConfig
}
