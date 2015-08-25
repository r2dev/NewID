from flask import jsonify, g, request
from . import api
from .. import db
from ..models import User, Follow
from .errors import unauthorized
from .decorators import premission_required
from .authentication import auth
import json
@api.route('/users/<username>')
def get_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return jsonify(user.to_json())
@api.route('/users/<username>/social')
def get_user_social(username):
    user = User.query.filter_by(username=username).first_or_404()
    return jsonify({
        'website': user.website,
        'vk': user.vk,
        'googleplus': user.googleplus,
        'twitch': user.twitch,
        'tumblr': user.tumblr,
        'spotify': user.spotify,
        'twitter': user.twitter,
        'instagram': user.instagram,
        'skype': user.skype
    })
@api.route('/register', methods=['POST', 'GET'])
def register():
    register_info = request.get_json()
    if (register_info == None):
        return jsonify({'status': 'failed'})
    user = User(email=register_info['email'], username=register_info['username'], password=register_info['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'status': 'successed'})

@api.route('/me')
def me():
    if not g.current_user.is_authenticated:
        return forbidden('Insufficient permissions')
    return jsonify(g.current_user.to_json());
@api.route('/connections')
def connections():
    if not g.current_user.is_authenticated:
        return forbidden('Insufficient permissions')
    connect_users = User.query.join(Follow, Follow.followed_id == User.id).filter(Follow.follower_id == g.current_user.id).all()
    print connect_users

    data = {}
    data['number'] = len(connect_users)
    for i in range(len(connect_users)):
        data[i] = connect_users[i].to_json()
    json_data = json.dumps(data)
    return json_data
