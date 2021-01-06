import os
from dotenv import load_dotenv, find_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    load_dotenv(find_dotenv())
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ["SECRET_KEY"]
    CELERY_BROKER_URL = 'amqp://localhost//'
    CELERY_BACKEND = 'db+sqlite:///site.db'
    CELERY_TASK_DEFAULT_RATE_LIMIT = '4/m'
