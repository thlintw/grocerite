import click, os
from apiflask import APIFlask
from flask_cors import CORS
from config import Config
from flask.cli import with_appcontext
from .db import db
from dotenv import load_dotenv, find_dotenv

import firebase_admin
from firebase_admin import credentials, firestore

from .routes.main import main


@click.command('init-db')
@with_appcontext
def init_db_command():
    db.create_all()
    click.echo('Initialized the database.')


def get_firebase_service_account():
    return {
        "type": "service_account",
        "project_id": "grocerite-f39ad",
        "private_key_id": os.getenv('FIREBASE_ADMIN_PRIVATE_KEY_ID', ''),
        "private_key": os.getenv('FIREBASE_ADMIN_PRIVATE_KEY', '').replace('\\n', '\n'),
        "client_email": os.getenv('FIREBASE_ADMIN_CLIENT_EMAIL', ''),
        "client_id": os.getenv('FIREBASE_ADMIN_CLIENT_ID', ''),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": os.getenv('FIREBASE_ADMIN_AUTH_PROVIDER_X509_CERT_URL', ''),
        "client_x509_cert_url": os.getenv('FIREBASE_ADMIN_CLIENT_X509_CERT_URL', ''),
        "universe_domain": "googleapis.com"
    }


def create_app():
    app = APIFlask(__name__)
        
    app.config.from_object(Config)
    app.register_blueprint(main)
    CORS(app)

    cred = credentials.Certificate(get_firebase_service_account())
    firebase_admin.initialize_app(cred)

    db.init_app(app)

    app.cli.add_command(init_db_command)
    app.fs = firestore.client()

    return app

