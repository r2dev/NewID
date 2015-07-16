from flask import jsonify, g
from . import api
from ..models import User
from .errors import unauthorized
@api.route('/users/<profile_url>')
def get_user(profile_url):
    user = User.query.filter_by(profile_url=profile_url).first_or_404()
    return jsonify(user.to_json())
@api.route('/users/')
def user_profile():
    if g.current_user.is_anonymous():
        return unauthorized("Invalid credentials")
    return jsonify(g.current_user.to_json())
