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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:Nilap@1234@localhost/ChunaLagake_V2Test'
    app.debug = True
#app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://kpmrusbememplz:75e5885c2e4712e816632cb9367ed5cc3adbf60e0ff7ea1fee0770f0fffff622@ec2-52-201-55-4.compute-1.amazonaws.com:5432/d4iv58stu8uomp"
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
