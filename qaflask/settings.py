import os
from dotenv import load_dotenv
load_dotenv(verbose=True)


SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
SECRET_KEY = os.environ.get('SECRET_KEY')

