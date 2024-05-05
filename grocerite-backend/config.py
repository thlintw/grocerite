import os
from dotenv import load_dotenv
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'a default secret key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

    ABC = os.getenv('ABC')

    FIREBASE_ADMIN_SERVICE_ACCOUNT = {
        "type": "service_account",
        "project_id": "grocerite-f39ad",
        "private_key_id": os.getenv('FIREBASE_ADMIN_PRIVATE_KEY_ID'),
        "private_key": os.getenv('FIREBASE_ADMIN_PRIVATE_KEY').replace('\\n', '\n') if  os.getenv('FIREBASE_ADMIN_PRIVATE_KEY') else '',
        "client_email": os.getenv('FIREBASE_ADMIN_CLIENT_EMAIL'),
        "client_id": os.getenv('FIREBASE_ADMIN_CLIENT_ID'),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": os.getenv('FIREBASE_ADMIN_AUTH_PROVIDER_X509_CERT_URL'),
        "client_x509_cert_url": os.getenv('FIREBASE_ADMIN_CLIENT_X509_CERT_URL'),
        "universe_domain": "googleapis.com"
    }

    
    # JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_SECRET_KEY = 'oyeahyeahyeahyeah'
    
class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    pass
