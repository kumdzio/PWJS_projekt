from flask import Flask
app= Flask(__name__)
import os
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app.config.update(
    DEBUG = True,
    SECRET_KEY='sekretny_klucz'
)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
db = SQLAlchemy(app)

from app import routes