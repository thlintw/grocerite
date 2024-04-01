from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig
import click
from flask.cli import with_appcontext
from .db import db

from .routes.main import main
from .routes.household import household


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    db.create_all()
    click.echo('Initialized the database.')

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.register_blueprint(main)

    db.init_app(app)

    app.cli.add_command(init_db_command)

    return app
