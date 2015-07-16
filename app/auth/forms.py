from flask.ext.wtf import Form, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(Form):
	email = StringField('Email', validators=[Required(), Length(1,64), Email()])
	password = PasswordField('Password', validators=[Required()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Log In')
    

class RegisterationForm(Form):
    email = StringField('Email', validators=[Required(), Length(1,64), Email()])
    username = StringField('Username', validators=[Required(), Length(1,64), 
		Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Invalid username')])
    password = PasswordField('New Password', 
    	validators=[Required(), EqualTo('confirm', 'Passwords must match')])
    confirm = PasswordField('Repeat Password')
    recaptcha = RecaptchaField()
    submit = SubmitField('Register')


    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Emailn already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')