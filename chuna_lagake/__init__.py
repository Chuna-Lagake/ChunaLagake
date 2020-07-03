import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c0e86bb97cf45f8f36c696128d94e3bd'

ENV = 'test'
if ENV == 'test':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:Nilap@1234@localhost/ChunaLagake'
    app.debug = True
    pass
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://krcpkqjstfskjv:7b5286aa792b9e323a6e343f435ad712648ba157e6cd00377d8eed783fab0949@ec2-52-200-119-0.compute-1.amazonaws.com:5432/dn3hh3d4lh1a0"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "chunalagake.official@gmail.com"
app.config['MAIL_PASSWORD'] = "paanwithshaan"
mail = Mail(app)

from chuna_lagake import routes
