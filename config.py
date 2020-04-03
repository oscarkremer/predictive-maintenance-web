import os
from dotenv import load_dotenv, find_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    load_dotenv(find_dotenv())
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ["SECRET_KEY"]