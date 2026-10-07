from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from dotenv import find_dotenv, load_dotenv


db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    load_dotenv()
    print("Reading", find_dotenv(), "| MYSQL_DB =", os.getenv("MYSQL_DB"), flush=True)
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    mysql_host = os.getenv('MYSQL_HOST')
    mysql_user = os.getenv('MYSQL_USER')
    mysql_password = os.getenv('MYSQL_PASSWORD')
    mysql_db = os.getenv('MYSQL_DB')

    if mysql_host and mysql_user and mysql_password and mysql_db:
        app.config['SQLALCHEMY_DATABASE_URI'] = (
            f'mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}'
        )
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

    db.init_app(app)

    with app.app_context():
        from .models import User
        db.create_all()

    return app


