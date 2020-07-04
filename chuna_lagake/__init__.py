import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c0e86bb97cf45f8f36c696128d94e3bd'

#ENV = 'test'
#if ENV == 'test':
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'TEST_DATABASE_URI'
#     app.debug = True
#     pass
# app.config["SQLALCHEMY_DATABASE_URI"] = "PRODUCTION_DATABASE_URI"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "USERNAME"
app.config['MAIL_PASSWORD'] = "PASSWORD"
mail = Mail(app)

from chuna_lagake import routes
