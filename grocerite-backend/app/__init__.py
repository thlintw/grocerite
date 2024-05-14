import click, os, base64
from apiflask import APIFlask
from flask_cors import CORS
from config import Config
from flask.cli import with_appcontext
from .db import db

import firebase_admin
from firebase_admin import credentials, firestore

from .routes.main import main


def create_app():
    app = APIFlask(__name__)
        
    app.config.from_object(Config)
    app.register_blueprint(main)
    CORS(app)

    cred = credentials.Certificate(get_firebase_service_account())
    firebase_admin.initialize_app(cred)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['DEBUG'] = True if os.getenv('APP_MODE', 'dev') == 'dev' else False
    
    db.init_app(app)

    app.cli.add_command(init_db_command)
    app.fs = firestore.client()

    return app


@click.command('init-db')
@with_appcontext
def init_db_command():
    db.create_all()
    click.echo('Initialized the database.')

    

def get_firebase_service_account():
    decodedKey = base64.b64decode(os.getenv('FIREBASE_ADMIN_PRIVATE_KEY'))
    decodedKey = decodedKey.decode('utf-8')
    return {
        "type": "service_account",
        "project_id": "grocerite-f39ad",
        "private_key_id": os.getenv('FIREBASE_ADMIN_PRIVATE_KEY_ID', ''),
        "private_key": decodedKey.replace('\\n', '\n'),
        "client_email": os.getenv('FIREBASE_ADMIN_CLIENT_EMAIL', ''),
        "client_id": os.getenv('FIREBASE_ADMIN_CLIENT_ID', ''),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": os.getenv('FIREBASE_ADMIN_AUTH_PROVIDER_X509_CERT_URL', ''),
        "client_x509_cert_url": os.getenv('FIREBASE_ADMIN_CLIENT_X509_CERT_URL', ''),
        "universe_domain": "googleapis.com"
    }