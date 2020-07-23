from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from main.models import User, Room


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
    college = StringField('College')
    work = StringField("Work")
    phone = StringField("Mobile No.")
    intro = TextAreaField('Tell us something about yourself..')

    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This Email ID already has an account')


class PostForm(FlaskForm):
    title = TextAreaField('Title', validators=[DataRequired()])
    information = TextAreaField('Information', validators=[DataRequired()])
    submit = SubmitField('Post')


class RequestResetForm(FlaskForm):
    email = StringField('Email Address',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request password reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('This email id does not have an account')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    confirmPassword = PasswordField('Confirm New Password',
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class CreateRoomForm(FlaskForm):
    room_name = StringField('Room Name', validators=[DataRequired()])
    submit = SubmitField('Add')


class DeleteRoomForm(FlaskForm):
    room_name = StringField('Room Name', validators=[DataRequired()])
    submit = SubmitField('Delete')

    def validate_room(self, room_name):
        room = Room.query.filter_by(room_name=room_name.data).first()
        if room is None:
            raise ValidationError('This room does not exist')