from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from main.models import User


class RegistrationForm(FlaskForm):
    firstName = StringField('First Name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    lastName = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email Address',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmPassword = PasswordField('Confirm Password',
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This Email ID already has an account')


class LoginForm(FlaskForm):
    email = StringField('Email Address',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')

    submit = SubmitField('Log In')


class UpdateForm(FlaskForm):
    firstName = StringField('First Name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    lastName = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email Address',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This Email ID already has an account')


class MessageForm(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')