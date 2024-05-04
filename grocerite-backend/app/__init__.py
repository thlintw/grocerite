from apiflask import APIFlask
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig
import click
from flask.cli import with_appcontext
from .db import db

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

    db.init_app(app)

    app.cli.add_command(init_db_command)

    return app

