from flask import render_template, request, flash, redirect
from chuna_lagake import app
from chuna_lagake.models import User, Feedback, Menu, Entry
from chuna_lagake.forms import LoginForm, RegistrationForm, FeedbackForm



@app.route('/')
def home():
	return render_template('home.html')

@app.route('/login',methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit() :
		if form.email.data == 'admin@blog.com' and form.password.data == 'password':
			flash('Logged in!','success')
			return redirect('/')
	return render_template('login.html',form=form)

@app.route('/products')
def products():
	return render_template('products.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/contact')
def contact():
	form = FeedbackForm()
	return render_template('contact.html',form=form)

@app.route('/login/forgot password')
def forgot_pass():
	return render_template('forgot.html')

@app.route('/login/signup',methods=['GET','POST'] )
def signup():
	form = RegistrationForm()
	if form.validate_on_submit() :
		flash(f'Account created for {form.username.data}!','success')
		return redirect('/')
	return render_template('signup.html',form=form)

