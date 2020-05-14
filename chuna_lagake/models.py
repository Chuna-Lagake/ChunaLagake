from chuna_lagake import db

class User(db.Model):
	__tablename__ = "Login"
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String, nullable=False)
	password = db.Column(db.String, nullable=False)
	email = db.Column(db.String, nullable=False)
