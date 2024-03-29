from .forms import LoginForm, RegisterationForm
from . import auth
from .. import db
from ..models import User
from flask import render_template, redirect, flash, request, url_for
from flask.ext.login import login_user, logout_user, login_required, current_user
@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()	
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.index'))
		flash('Invalid username or password')
	return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out')
	return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterationForm()
	if form.validate_on_submit():
		user = User(email=form.email.data,
			username=form.username.data,
			password=form.password.data
			)
		db.session.add(user)
		db.session.commit()
		flash('you have registered') 
		return redirect(url_for('auth.login'))
	return render_template('auth/register.html', form=form)
