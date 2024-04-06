import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a default secret key'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres.ufsizzoygpymnrfdpolv:ptISlB5KOjNko1EHbtE1S4UFjeC@aws-0-eu-central-1.pooler.supabase.com:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
    #     'sqlite://'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres.ufsizzoygpymnrfdpolv:ptISlB5KOjNko1EHbtE1S4UFjeC@aws-0-eu-central-1.pooler.supabase.com:5432/postgres'

class ProductionConfig(Config):
    pass
