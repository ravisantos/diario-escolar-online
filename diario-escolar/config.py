import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-troque-depois')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database', 'diario.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    
os.makedirs(os.path.join(BASE_DIR, 'database'), exist_ok=True)