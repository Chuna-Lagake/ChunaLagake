from chuna_lagake import db

class User(db.Model):
	__tablename__ = "user"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	username = db.Column(db.String(20), nullable=False, unique=True)
	password = db.Column(db.String(256), nullable=False)
	email = db.Column(db.String(100), nullable=False, unique=True)
	feedbacks = db.relationship('Feedback', backref='user',lazy=True)
	entries = db.relationship('Entry', backref='user',lazy=True)

class Feedback(db.Model):
	__tablename__ = "feedback"
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	feedback = db.Column(db.Text, nullable=False)

class Menu(db.Model):
	__tablename__ = 'menu'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False, unique=True)
	image = db.Column(db.String, nullable=False)
	description = db.Column(db.Text, nullable=False)
	entries = db.relationship('Entry', backref='product', lazy=True)

class Entry(db.Model):
	__tablename__ = 'entry'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
	product_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)
	status = db.Column(db.Boolean)
	timestamp = db.Column(db.String, nullable=False)