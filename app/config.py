import os

class Conf(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///vexillum.db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.normpath('static/uploads')
