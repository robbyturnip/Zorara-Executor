from flask_wtf          	import FlaskForm
from flask_wtf.file     	import FileField, FileRequired
from wtforms            	import StringField, TextAreaField, SubmitField, PasswordField, IntegerField, SelectField
from wtforms.validators 	import InputRequired, Email, DataRequired, NumberRange
from wtforms.fields.html5 	import DateField

class LoginForm(FlaskForm):
	username    = StringField  (u'Username'        , validators=[DataRequired()])
	password    = PasswordField(u'Password'        , validators=[DataRequired()])

class RegisterForm(FlaskForm):
	username    = StringField  (u'Username'  , validators=[DataRequired()])
	password    = PasswordField(u'Password'  , validators=[DataRequired()])

class CrawlingForm(FlaskForm):
	keyword    = StringField  	(u'Keyword'  	,  	validators=[DataRequired()])
	startdate  = DateField		(u'Start Date'	, 	format='%Y-%m-%d')
	enddate    = DateField		(u'End Date'	,   format='%Y-%m-%d')
	maxtweet   = IntegerField	(u'Max Tweet'	, 	validators=[NumberRange(min=0, max=100000)], default=0)

	def validate_on_submit(self):
		result = super(CrawlingForm, self).validate()

		if 	self.startdate.data and self.enddate.data:

			if (self.startdate.data>self.enddate.data) or not self.keyword.data:
				return False
			else:
				return result
		else:
			return True

class TrainingForm(FlaskForm):
	centroid    = StringField  	(u'Id Centoroid Cluster'  	,  	validators=[DataRequired()])
	cluster     = IntegerField  	(u'Cluster Name'  	,  	validators=[DataRequired()])
