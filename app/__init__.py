from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.qrcode import QRcode
from flask.ext.oauthlib.client import OAuth
from werkzeug.contrib.fixers import ProxyFix
import flask.ext.whooshalchemy as whooshalchemy
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()
oauth = OAuth()
login_manager = LoginManager()


login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
app = Flask(__name__)
def create_app():
	app.config.from_object(config)
	bootstrap.init_app(app)
	db.init_app(app)
	oauth.init_app(app)
	QRcode(app)
	login_manager.init_app(app)
	if not app.config['SSL_DISABLE']:
		from flask.ext.sslify import SSLify
		sslify = SSLify(app)
	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint, url_prefix='/auth')
	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)
	from .api_0_1 import api_bp as api_0_1_blueprint
	app.register_blueprint(api_0_1_blueprint, url_prefix='/api/v0.1')
	from .social import social as social_blueprint
	app.register_blueprint(social_blueprint, url_prefix='/social')
	return app
