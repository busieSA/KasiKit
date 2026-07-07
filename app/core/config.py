import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

class Config:
    """ Base Application configuration. """

    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')

    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{os.path.join(
            BASE_DIR,
            'kasikit.db'
        )}"
    )

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "change this in production???"
    )


class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

    
