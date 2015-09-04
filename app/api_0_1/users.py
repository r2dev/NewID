from flask import jsonify, g, request
from flask.ext.sqlalchemy import sqlalchemy
from . import api
from .. import db
from ..models import User, Follow
from .errors import unauthorized
from .decorators import premission_required
from .authentication import auth
import json
from flask_restful import Resource, reqparse


class ViewUser(Resource):
    def get(self, username):
        user = User.query.filter_by(username=username).first()
        try:
            response = user.to_json()
        except:
            return {"status": "failed"}, 404
        else:
            return response, 200
    def put(self, username):
        pass

class MakeNewUser(Resource):
    #register module
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        self.reqparse.add_argument('email', type=str, location='json', required=True, help='invaild email')
        self.reqparse.add_argument('username', type=str, location='json', required=True, help='invaild username')
        self.reqparse.add_argument('password', type=str, location='json', required=True, help='invalid password')
        super(MakeNewUser, self).__init__()

    def post(self):
        register = self.reqparse.parse_args()
        user = User(email=register['email'], username=register['username'], password=register['password'])
        try:
            db.session.add(user)
            db.session.commit()
        except:
            db.session.rollback()
            return {"status": "invalid data"}, 404
        else:
            return {"status": "ok"}, 200

class ConnectUser(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        self.reqparse.add_argument('follower', type=int, location='json', required=True)
        self.reqparse.add_argument('followed', type=int, location='json', required=True)
        super(ConnectUser, self).__init__()
    def post(self):
        result = self.reqparse.parse_args()
        f = Follow(follower_id=result['follower'], followed_id=result['followed'])
        try:
            db.session.add(f)
            db.session.commit()
        except:
            db.session.rollback()
            return {"status": "invalid data"}, 404
        else:
            return {"status": "ok"}, 200
class ViewConnection(Resource):
    def get(self, username):
        user = User.query.filter_by(username=username).first()
        recent_connect_user = User.query.join(Follow, Follow.followed_id == User.id).filter(Follow.username == username)
        print recent_connect_user
        return {"hello": "ok"}
api.add_resource(MakeNewUser, '/users', endpoint='users')
api.add_resource(ViewUser, '/users/<string:username>', endpoint='user')
api.add_resource(ConnectUser, '/connection', endpoint='connect')
api.add_resource(ViewConnection, '/connection/<string:username>', endpoint='connection')



#
# @api.route('/users/<username>')
# def get_user(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     return jsonify(user.to_json())
# @api.route('/users/<username>/social')
# def get_user_social(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     return jsonify({
#         'website': user.website,
#         'vk': user.vk,
#         'googleplus': user.googleplus,
#         'twitch': user.twitch,
#         'tumblr': user.tumblr,
#         'spotify': user.spotify,
#         'twitter': user.twitter,
#         'instagram': user.instagram,
#         'skype': user.skype
#     })
# @api.route('/register', methods=['POST', 'GET'])
# def register():
#     register_info = request.get_json()
#     if (register_info == None):
#         return jsonify({'status': 'failed'})
#     user = User(email=register_info['email'], username=register_info['username'], password=register_info['password'])
#     db.session.add(user)
#     db.session.commit()
#     return jsonify({'status': 'successed'})
#
# @api.route('/me')
# def me():
#     if not g.current_user.is_authenticated:
#         return forbidden('Insufficient permissions')
#     return jsonify(g.current_user.to_json());
# @api.route('/connections')
# def connections():
#     if not g.current_user.is_authenticated:
#         return forbidden('Insufficient permissions')
#     connect_users = User.query.join(Follow, Follow.followed_id == User.id).filter(Follow.follower_id == g.current_user.id).all()
#     print connect_users
#
#     data = {}
#     data['number'] = len(connect_users)
#     for i in range(len(connect_users)):
#         data[i] = connect_users[i].to_json()
#     json_data = json.dumps(data)
#     return json_data
