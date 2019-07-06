from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from gymcoin.models import User

class RegistrationForm(FlaskForm):

	name = StringField('First Name', validators=[DataRequired()],
							render_kw={"placeholder": "Name"});

	username = StringField('Username', 
						   validators=[DataRequired(), Length(min=4, max=15)],
						   render_kw={"placeholder": "Username"});

	email = StringField('Email', validators=[DataRequired(), Email()],
						render_kw={"placeholder": "Email"});

	password = PasswordField('Password', validators=[DataRequired()],
							 render_kw={"placeholder": "Password"});

	confirmPassword = PasswordField('Confirm Password', 
									validators=[DataRequired(), EqualTo('password')],
									render_kw={"placeholder": "Confirm Password"});

	submit = SubmitField('Sign Up');

	def validate_username(self, username):
		user = User.query.filter_by(username = username.data).first()
		if user:
			raise ValidationError('Username already taken. Please choose another username');
	def validate_email(self, email):
		email = User.query.filter_by(email = email.data).first()
		if email:
			raise ValidationError('Email already taken. Please choose another username');



class LoginForm(FlaskForm):

	email = StringField('Email', validators=[DataRequired(), Email()],
						render_kw={"placeholder": "Email"});

	password = PasswordField('Password', validators=[DataRequired()],
						render_kw={"placeholder": "Password"});

	remember = BooleanField('Remember Me');

	submit = SubmitField('Login');

class TransactionForm(FlaskForm):

	sender = StringField('Sender', 
						   validators=[DataRequired(), Length(min=4, max=15)]);


	reciever = StringField('Reciever', 
						   validators=[DataRequired(), Length(min=4, max=15)]);

	amount = IntegerField('Amount', validators=[DataRequired()]);

	key = StringField('Key', validators=[DataRequired()]);

	dummy = StringField('Dummy');


	submit = SubmitField('Make a Transaction!');

class TransactionFormNotLoggedIn(FlaskForm):

	sender = StringField('Sender');

	reciever = StringField('Reciever');

	amount = StringField('Amount');

	key = StringField('Key');

	dummy = StringField('Dummy');


	submit = SubmitField('Sign in to make a transaction!');