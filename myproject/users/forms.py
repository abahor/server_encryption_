from flask_wtf import FlaskForm,RecaptchaField
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length, InputRequired
from flask_wtf.file import FileField, FileAllowed
from wtforms import ValidationError

from myproject.models import Users


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'placeholder':'Email'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder':'Password'})
    submit = SubmitField('Log In')

class RegisterationForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()], render_kw={'placeholder': 'Email'})
    username = StringField('username', validators=[InputRequired()], render_kw={'placeholder': 'Username'})
    password = PasswordField('Password',
                             validators=[InputRequired(), EqualTo('pass_confirm', message='Passwords must match')],
                             render_kw={'placeholder': 'Password'})
    pass_confirm = PasswordField('Confirm Password',
                                 validators=[InputRequired()], render_kw={'placeholder': 'confirm password'})
    recaptcha = RecaptchaField()
    submit = SubmitField('Register')

    def check_email(self, field):
        if Users.query.filter_by(email=field.data).first():
            raise ValidationError('This email is already exists login instead')


class formRecover(FlaskForm):
    password = PasswordField('The new password', validators=[DataRequired()], render_kw={'placeholder': 'your new '
                                                                                                        'password'})
    submit = SubmitField('Change')

class changepassword(FlaskForm):
    password = PasswordField('your current password', validators=[DataRequired()],render_kw={'placeholder': 'current password'})
    password_new = PasswordField('The new password', validators=[DataRequired()], render_kw={'placeholder': 'your new password'})
    submit = SubmitField('change')


class yourEmail(FlaskForm):
    email = StringField('your email',validators=[DataRequired(),Email()],render_kw={"placeholder":'your Email'})
    submit = SubmitField('send')

class confirmationForm(FlaskForm):
    password = PasswordField('the code',validators=[DataRequired()],render_kw={'placeholder':'Password'})
    submit = SubmitField('confirm')

class updateForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={'placeholder':'Username'})
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'gif'])])
    submit = SubmitField('Update')

    def check_email(self, field):
        if Users.query.filter_by(email=field.data).first():
            raise ValidationError('This email is already exists login instead')
