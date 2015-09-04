from flask import jsonify, g
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.login import AnonymousUserMixin, current_user
from ..models import User
from . import api_bp
from .errors import unauthorized, forbidden

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(email_or_token, password):
	if email_or_token == '':
		g.user = AnonymousUserMixin()
		return True
	if password == '':
		g.current_user = User.verify_auth_token(email_or_token)
		g.token_used = True
		return g.current_user is not None
	user = User.query.filter_by(email=email_or_token).first()
	if not user:
		return False
	g.current_user = user
	g.token_used = False
	return user.verify_password(password)

@api_bp.before_request
@auth.login_required
def before_request():
	pass

@auth.error_handler
def auth_error():
	return unauthorized('Invalid credentials')

# @api.route('/token')
# @auth.login_required
# def get_token():
# 	if g.current_user.is_anonymous():
# 		return unauthorized('Invalid credentials')
# 	return jsonify({'token': g.current_user.generate_auth_token()})
