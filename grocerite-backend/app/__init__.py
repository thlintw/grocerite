import click
from apiflask import APIFlask
from flask_cors import CORS
from config import DevelopmentConfig
from flask.cli import with_appcontext
from .db import db

import firebase_admin
from firebase_admin import credentials

from .routes.main import main


@click.command('init-db')
@with_appcontext
def init_db_command():
    db.create_all()
    click.echo('Initialized the database.')

def create_app(config_class=DevelopmentConfig):
    app = APIFlask(__name__)
    app.config.from_object(config_class)
    app.register_blueprint(main)
    CORS(app)


    cred = credentials.Certificate(app.config['FIREBASE_ADMIN_SERVICE_ACCOUNT'])
    firebase_admin.initialize_app(cred)

    db.init_app(app)

    app.cli.add_command(init_db_command)

    return app

