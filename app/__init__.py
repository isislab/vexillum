from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database
from os import urandom

def create_app():
    app = Flask(__name__)
    app.secret_key = urandom(24)

    from models import db
    import config

    app.config.from_object(config)

    if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']): #create database
        create_database(app.config['SQLALCHEMY_DATABASE_URI'])

    db.init_app(app) #initialize db
    db.app = app #initialize db
    db.create_all() #create tables
    app.db = db #set the app's db to db

    #from utils import init_utils, init_errors
    from core import core
    from admin import admin
    from auth import auth

    #init_utils(app)
    #init_errors(app)
    app.register_blueprint(core)
    app.register_blueprint(admin)
    app.register_blueprint(auth)

    return app

