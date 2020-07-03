from flask import render_template, request, flash, redirect, url_for
from chuna_lagake import app, db, bcrypt, mail
from chuna_lagake.models import User, Feedback, Menu, Ratings
from chuna_lagake.forms import LoginForm, RegistrationForm, FeedbackForm, RequestResetForm, ResetPasswordForm
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import numpy as np
from chuna_lagake.build_recommendation import *


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
	
	num_bought = []
	for i in range(Menu.query.count()):
		item = Menu.query.get(i+1)
		num_bought.append(item.times_bought)
	num_bought = np.argsort(num_bought)[::-1]
	trending_items = [str(x+1) for x in num_bought[:5]]
	
	if current_user.is_authenticated:
		if len(current_user.ratings) == 0 :
			list_of_recommendations = trending_items
		else :
			model, interactions, labels, item_features = train_model()
			list_of_recommendations = convert_to_user_recommend(model, interactions, labels, item_features, [current_user.id])
			trending_items = [str(x+1) for x in num_bought[:5]]
		return render_template('products.html', trending_items = trending_items, recommended_items = [str(x) for x in list_of_recommendations])
	
	return render_template('products.html', trending_items = trending_items)


@app.route('/products/<key_id>')
def item(key_id):

	if not 0 < int(key_id) < 51 :
		flash('Requested item does not exist','warning')
		return redirect(url_for('products'))

	item = db.session.query(Menu).get(key_id)

	try:
		ratings = request.args['ratings']
	except:
		return render_template('item.html', item = item, key = str(key_id))
	if ratings :
		return render_template('item.html', ratings=ratings, item=item , key = str(key_id))

	else :
		return render_template('item.html', item=item , key = str(key_id))

@app.route('/products/<key_id>/buy')
def buy(key_id):
	if not 0 < int(key_id) < 51 :
		flash('Requested item does not exist','warning')
		return redirect(url_for('products'))

	if current_user.is_authenticated:
		item_object = Menu.query.get(key_id)
		item_object.times_bought += 1
		db.session.commit()
		return redirect(url_for('item', ratings=True, key_id=key_id))

	flash('You have to be logged in to buy items','warning')
	return redirect(url_for('item', key_id = key_id))

@app.route('/products/<key_id>/rate/<star>')
def rate(key_id, star):
	if not 0 < int(key_id) < 51 :
		flash('Requested item does not exist','warning')
		return redirect(url_for('products'))

	if not current_user.is_authenticated:
		flash('You have to be logged in to rate items','warning')
		return redirect(url_for('item', key_id = key_id))

	if not 0 < int(star) < 6 :
		flash('Rating has to be between 1 and 5','warning')
		return redirect(url_for('item', key_id = key_id))

	user_id = current_user.id
	item_id = key_id

	rate_object = Ratings.query.filter_by(user_id=user_id, item_id=item_id).first()

	if not rate_object :
		rating = Ratings(user_id = user_id, item_id = item_id, rating = star)
		db.session.add(rating)
		db.session.commit()

	else:
		rate_object.rating = 0.4*rate_object.rating + 0.6*int(star)
		db.session.commit()

	flash('Your review has been successfully recorded','success')
	return redirect(url_for('item', key_id = key_id))

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

@app.route('/terms',methods=['GET','POST'])
def tnc():
	return render_template('tnc.html')

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home'))
