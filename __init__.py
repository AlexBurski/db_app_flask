from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "qwerty"
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://dbuser:hello@localhost:5432/db"
    db.init_app(app)
    from .auth import auth
    app.register_blueprint(auth, url_prefix='/')
    #create_database(app)  # used for once
    return app


def create_database(app):
    db.create_all(app=app)
