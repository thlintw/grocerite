import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = True
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

