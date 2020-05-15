from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c0e86bb97cf45f8f36c696128d94e3bd'

ENV = 'development'
if ENV == 'prod':
	app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres://kpmrusbememplz:75e5885c2e4712e816632cb9367ed5cc3adbf60e0ff7ea1fee0770f0fffff622@ec2-52-201-55-4.compute-1.amazonaws.com:5432/d4iv58stu8uomp'
elif ENV == 'development':
	app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:qwerty123@localhost:5432/postgres'
else:
	print('uri error')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from chuna_lagake import routes