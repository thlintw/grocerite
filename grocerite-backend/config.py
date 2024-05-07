import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:

    DEBUG = True if os.getenv('APP_MODE', 'dev') == 'dev' else False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'keykey1keykkey2key3kye23k2ey34')

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db') if os.getenv('APP_MODE', 'dev') == 'dev' else os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_ENGINE_OPTIONS = {
    #     'connect_args': {
    #         'options': '-csearch_path=dev' if os.getenv('APP_MODE', 'dev') == 'dev' else '-csearch_path=public'
    #     }
    # }

