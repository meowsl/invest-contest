from os import getenv
from dotenv import load_dotenv

load_dotenv()

# flask
FLASK_APP = getenv("FLASK_APP")
SECRET_KEY = getenv("SECRET_KEY")

# sqlalchemy
DATABASE_FILE = getenv("DATABASE_FILE")
SQLALCHEMY_DATABASE_URI = getenv("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_ECHO = getenv("SQLALCHEMY_ECHO", False)
SQLALCHEMY_TRACK_MODIFICATIONS = getenv("SQLALCHEMY_TRACK_MODIFICATIONS", False)