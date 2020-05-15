from flask import render_template, request, flash, redirect
from chuna_lagake import app, db, bcrypt
from chuna_lagake.models import User, Feedback, Menu, Entry
from chuna_lagake.forms import LoginForm, RegistrationForm, FeedbackForm
from flask_login import login_user, current_user, logout_user, login_required


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
			return redirect('/')
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
		feedback = Feedback(user_id=current_user.id,feedback=form.feedback.data)
		db.session.add(feedback)
		db.session.commit()
		flash('Your feedback has been recorded','success')
		return redirect('/contact')
	return render_template('contact.html',form=form)

@app.route('/login/forgot password')
def forgot_pass():
	return render_template('forgot.html')

@app.route('/login/signup',methods=['GET','POST'] )
def signup():
	if current_user.is_authenticated:
		return redirect('/')
	form = RegistrationForm()
	if form.validate_on_submit() :
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data,email=form.email.data,password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created! You can now log in','success')
		return redirect('/login')
	return render_template('signup.html', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect('/') 