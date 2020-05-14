from flask import render_template, request
from chuna_lagake import app
from chuna_lagake.models import *



@app.route('/')
def index():
	return render_template('home.html')

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/products')
def products():
	return render_template('products.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/contact')
def contact():
	return render_template('contact.html')

@app.route('/login/forgot password')
def forgot_pass():
	return render_template('forgot.html')

@app.route('/login/signup')
def signup():
	return render_template('signup.html')

