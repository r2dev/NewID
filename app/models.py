from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask import current_app, flash
from itsdangerous import JSONWebSignatureSerializer as Serializer
from flask.ext.login import AnonymousUserMixin, UserMixin
from . import db, login_manager, app
import flask.ext.whooshalchemy as wa
import qrcode
import StringIO
import base64


#contact history
class Follow(db.Model):
	__tablename__ = 'follows'
	#the people who uses phone to scan
	follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
	#the people who provides the qrcode
	followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
	timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class User(UserMixin, db.Model):
	__tablename__ = 'users'
	__searchable__ = ['username']
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(254), unique=True, nullable=False)
	username = db.Column(db.String(64), unique=True, nullable=False)
	password_hash = db.Column('password', db.String(128), nullable=False)
	firstname = db.Column(db.String(35))
	midname = db.Column(db.String(35))
	lastname = db.Column(db.String(35))
	datejoined = db.Column(db.DateTime, default=datetime.utcnow())
	phone = db.Column(db.String(25))
	birthday = db.Column(db.DateTime)
	gender = db.Column(db.String(10))
	website = db.Column(db.String(200))
	location = db.Column(db.String(100))
	lastseen = db.Column(db.DateTime)
	#avatar = db.Column(db.String(200)) not useable yet
	vk = db.Column(db.String(32))
	googleplus = db.Column(db.String(30))
	twitch = db.Column(db.String(30))
	tumblr = db.Column(db.String(35))
	spotify = db.Column(db.String(35))
	twitter = db.Column(db.String(20))
	instagram = db.Column(db.String(30))
	skype = db.Column(db.String(32))
	reddit = db.Column(db.String(20))
	linkedin = db.Column(db.String(10))
	github = db.Column(db.String(40))
	soundcloud = db.Column(db.String(255))
	steam = db.Column(db.String(20))
	pinterest = db.Column(db.String(15))
	alibaba = db.Column(db.String(30))
	followed = db.relationship('Follow', foreign_keys=[Follow.follower_id], backref=db.backref('follower', lazy='joined'), lazy='dynamic', cascade='all, delete-orphan')
	followers = db.relationship('Follow', foreign_keys=[Follow.followed_id], backref=db.backref('followed', lazy='joined'), lazy='dynamic', cascade='all, delete-orphan')

	@property
	def password(self):
	    raise AttributeError('password is not a readable attribute')
	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)
	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)
	def save(self):
		db.session.add(self)
		db.session.commit()
		return self
	def to_json(self):
		json_user = {
			'username': self.username,
			'gender': self.gender,
			'email': self.email,
			'firstname': self.firstname,
			'lastname': self.lastname,
			'midname': self.midname,
			'location': self.location,
			'phone': self.phone,
			'qrcode': qrcode_string(self.username)
		}
		return json_user
	def generate_auth_token(self):
		s = Serializer(current_app.config['SECRET_KEY'])
		return s.dumps({'id': self.id}).decode('ascii')
	@staticmethod
	def verify_auth_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return None
		return User.query.get(data['id'])

	def __repr__(self):
		return '<User %r>' % self.username
	def __init__(self, email, username, password):
		self.email = email
		self.username = username
		self.password_hash = generate_password_hash(password)
		self.lastseen = datetime.utcnow()

	#add
	def follow(self, user):
		if not self.is_following(user):
			f = Follow(follower=self, followed=user)
			db.session.add(f)
			db.session.commit()
			flash('Follow success')
		else:
			flash('Already contact')
	def unfollow(self, user):
		f = self.followed.filter_by(followed_id=user.id).first()
		if f:
			db.session.delete(f)
			db.session.commit()
			flash('Unfollow success')
		else:
			flash('unfollow fail')
	#use for displaying the history of the contact people
	def is_following(self, user):
		return self.followed.filter_by(followed_id=user.id).first() is not None
	#use for displaying
	def is_following_by(self, user):
		return self.followers.filter_by(follower_id=user.id).first() is not None


@login_manager.user_loader
def load_user(userid):
	user = User.query.get(userid)
	if user:
		return user
	else:
		return None
def qrcode_string(data, version=None, error_correction='L', box_size=10, border=0, fit=True):
	qr = qrcode.QRCode(
	version=version,
	error_correction=qrcode.constants.ERROR_CORRECT_L,
	box_size=box_size,
	border=border
	)
	qr.add_data(data)
	qr.make(fit=fit)
	# creates qrcode base64
	io = StringIO.StringIO()
	qr_img = qr.make_image()
	qr_img.save(io)
	return base64.b64encode(io.getvalue())

login_manager.anonymous_user = AnonymousUserMixin
wa.whoosh_index(app, User)
