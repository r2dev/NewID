from . import main
from .forms import PersonalForm
from ..models import User, Follow
from flask import request, render_template, flash, redirect, current_app, url_for, g
from flask.ext.login import current_user, login_required
from werkzeug import secure_filename
import os


@main.route('/', methods=['POST', 'GET'])
def index():

	if current_user.is_authenticated():
		recent_connect_user = User.query.join(Follow, Follow.followed_id == User.id).filter(Follow.follower_id == current_user.id)
		form = PersonalForm(obj=current_user)
		if form.validate_on_submit():
			form.populate_obj(current_user)
			current_user.save()
			flash('Updated')
		return render_template('main/user_index.html', form=form, recent_connect_user=recent_connect_user)
	else:
		return render_template('main/index.html')
# Do not have premission on my own Windows, allow it when deploy
# def allowed_avatar_file(filename):
# 	return '.' in filename and filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']

# @main.route('/upload_avatar', methods=['POST', 'GET'])
# def upload_avatar():
# 	if current_user.is_authenticated():
# 		if request.method == 'POST':
# 			file = request.files['file']
# 			if file and allowed_avatar_file(file.filename.lower()):
# 				base = secure_filename(file.filename).rsplit('.',1)[0]

# 				file.save(current_app.config['UPLOAD_FOLDER'])
# 				flash('You have uploaded your avatar')
# 				return redirect(url_for('main.index'))
# 			else:
# 				return redirect(url_for('auth.register'))
@main.route('/user/<username>')
@login_required
def profile(username):
	user = User.query.filter_by(username=username).first_or_404()
	return render_template("main/user_profile.html", user=user)

@main.route('/user/<username>/connect')
@login_required
def connect_user(username):
	user = User.query.filter_by(username=username).first_or_404()
	current_user.follow(user)
	return redirect(url_for('main.profile', username=username))

@main.route('/user/<username>/disconnect')
@login_required
def disconnect_user(username):
	user = User.query.filter_by(username=username).first_or_404()
	current_user.unfollow(user)
	return redirect(url_for('main.profile', username=username))

@main.route('/search/<query>')
def search(query):
	results = User.query.whoosh_search(query).all()
	return render_template("main/search_result.html", results=results, query=query)
