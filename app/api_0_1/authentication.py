from flask import jsonify, g
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.login import AnonymousUserMixin
from ..models import User
from . import api
from .errors import unauthorized, forbidden
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(email_or_token, password):
	user = User.verify_auth_token(email_or_token)
	if not user:
		user = User.query.filter_by(email=email_or_token).first()
		if not user or not user.verify_password(password):
			return False
	g.user = user
	return True
@api.before_request
@auth.login_required
def before_request():
	pass

@auth.error_handler
def auth_error():
	return unauthorized('Invalid credentials')

@api.route('/token')
@auth.login_required
def get_token():
	if g.current_user.is_anonymous() or g.token_used:
		return unauthorized('Invalid credentials')
	return jsonify({'token': g.current_user.generate_auth_token()})
