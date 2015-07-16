import os
basedir = os.path.abspath(os.path.dirname(__name__))
class Config:
	DEBUG = True
	SECRET_KEY = 'test'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_RECORD_QUERIES = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
	NEW_ID_SLOW_DB_QUERY_TIME = 0.5
	NEW_ID_CONTACT_PER_PAGE = 10
	SSL_DISABLE = True
	WTF_CSRF_ENABLED = True
	#RECAPTCHA_PARAMETERS = {'hl': 'zh', 'render': 'explicit'}
	#RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}
	RECAPTCHA_PUBLIC_KEY = '6Ld0rAgTAAAAAOaWD7UQkataeDWLBTRoUjmWMIS1'
	RECAPTCHA_PRIVATE_KEY = '6Ld0rAgTAAAAAKtv3eZI_AVXBmE3AB06uwriu0yB'
	UPLOAD_FOLDER = os.path.join(basedir, 'avatar')
	#avatar entensions
	ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
	#whoosh
	WHOOSH_BASE = os.path.join(basedir, 'search.db')

config = Config()
