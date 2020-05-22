from flask import render_template, request, flash, redirect, url_for
from chuna_lagake import app, db, bcrypt, mail
from chuna_lagake.models import User, Feedback, Menu, Entry
from chuna_lagake.forms import LoginForm, RegistrationForm, FeedbackForm, RequestResetForm, ResetPasswordForm
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Password Reset Request', sender='chunalagake.official@gmail.com', recipients=[user.email])
	msg.body = f'''To reset your password visit the following link:
{url_for('reset_token',token=token,_external=True)}
If you did not make this requeset then simply ignore this email and no changes will be made
'''
	mail.send(msg)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/login',methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit() :
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			return redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check email and password','danger')
	return render_template('login.html',form=form)

@app.route('/products')
def products():
	return render_template('products.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/contact',methods=['GET','POST'])
def contact():
	form = FeedbackForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		feedback = Feedback(user_id=user.id,feedback=form.feedback.data)
		db.session.add(feedback)
		db.session.commit()
		flash('Your feedback has been recorded','success')
		return redirect(url_for('contact'))
	return render_template('contact.html',form=form)

@app.route('/forgot password', methods=['GET','POST'])
def forgot_pass():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RequestResetForm()	
	if form.validate_on_submit():
		user= User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('Email sent with instructions to reset your password','success')
		return redirect(url_for('login'))
	return render_template('forgot.html', form=form)

@app.route('/forgot password/<token>',methods=['GET','POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	user = User.verify_reset_token(token)
	if user is None:
		flash('That is an invalid or expired token','warning')
		return redirect(url_for('forgot_pass'))
	form = ResetPasswordForm()
	if form.validate_on_submit() :
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_password
		db.session.commit()
		flash('Your password has been updated','success')
		return redirect(url_for('login'))
	return render_template('reset.html', form=form)

@app.route('/signup',methods=['GET','POST'] )
def signup():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit() :
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data,email=form.email.data,password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created! You can now log in','success')
		return redirect(url_for('login'))
	return render_template('signup.html', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home')) 
