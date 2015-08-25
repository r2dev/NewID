from wtforms import StringField, SubmitField, SelectField, DateField
from wtforms.validators import Required, Length, Email, Optional, URL, Length
from flask.ext.wtf import Form
from wtforms import ValidationError
from ..models import User
from flask.ext.login import current_user
class PersonalForm(Form):
	username = StringField('Username', validators=[Required(), Length(5, 64)])
	firstname = StringField('First Name', validators=[Optional()])
	midname = StringField('Mid Name', validators=[Optional()])
	lastname = StringField('Last Name', validators=[Optional()])
	phone = StringField('Phone', validators=[Optional()])
	birthday = DateField("Birthday format(dd/mm/yyyy)", format="%d/%m/%Y", validators=[Optional()])
	gender = SelectField('Gender', default="None", choices=[
		("None", ""),
		("Male", "Male"),
		("Female", "Female")])
	location = StringField("Location", validators=[Optional()])
	website = StringField("Website", validators=[Optional(), URL()])
	skype = StringField("Skype Username", validators=[Optional()])
	instagram = StringField("Instagram username", validators=[Optional()])
	vk = StringField("http://vk.com/", validators=[Optional()])
	googleplus = StringField("Google ID", validators=[Optional()])
	github = StringField("Github Username", validators=[Optional()])
	twitch = StringField("Twitch Username", validators=[Optional()])
	tumblr = StringField("Tumblr Username", validators=[Optional()])
	reddit = StringField("Reddit Username", validators=[Optional()])
	linkedin = StringField("Linkedin ID", validators=[Optional()])
	soundcloud = StringField("Soundcloud", validators=[Optional()])
	steam = StringField("Steam", validators=[Optional()])
	pinterest = StringField("Pinterest", validators=[Optional()])
	alibaba = StringField("Alibaba Company name", validators=[Optional()])
	submit = SubmitField("Save")

	def validate_username(self, field):
		find = User.query.filter_by(username=field.data).first()
		if find and not (find == current_user):
			raise ValidationError('Username is already in use')
