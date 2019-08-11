from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, IntegerField
from wtforms.validators import *

class LoginForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')



class SignUpForm(FlaskForm):
	firstname = StringField('First Name')
	lastname = StringField('Last Name')
	zipcode = IntegerField('Zip Code')
	gender = StringField('Gender')
	username = StringField('UserName', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
	submit = SubmitField('Sign Up')

class ZipSearchForm(FlaskForm):
	zipcode = IntegerField('Zip Code', validators=[DataRequired()])
	submit = SubmitField('Search this area')

class SlotDateSearchForm(FlaskForm):
	starttime = IntegerField('Start Time(24-hr clock)', validators=[DataRequired()])
	zipcode = IntegerField('End Time(24-hr clock)', validators=[DataRequired()])
	eventdate = StringField('Date', validators=[DataRequired()])
	submit = SubmitField('Search Events')

class VenueDateForm(FlaskForm):
	zipcode = IntegerField('Zip Code', validators=[DataRequired()])
	eventdate = StringField('Date', validators=[DataRequired()])
	submit = SubmitField('Search Events')

# class StartEventForm():
	# c=common()
	# venuelist=c.get_all_venues()
	# venues=forms.ChoiceField(choices=venuelist)
	# class Meta:
	# 	model = Events
	# 	fields={
	# 		'eventname','eventdesc','eventdate','starttime','endtime','eventcapacity','genderoption'
	# 	}

	# 	labels = {
	# 			'genderoption': "Gender (Optional)",
	# 			'eventname': "Event Name",
	# 			'eventdesc': "Event Description",
	# 			'starttime': "Start Time(in 24-hour format)",
	# 			'endtime': "End Time(in 24-hour format)",
	# 			'eventcapacity': "Event Capacity",
	# 			'venues': "Choose Venue"
	# 	  }