from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField 
from wtforms.validators import DataRequired 
from blog.models import User
from wtforms.validators import ValidationError, EqualTo, Regexp


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    confirm_username = StringField('Confirm Username',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register') 

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already exist. Please choose a differentone.')
        username = StringField('Username',validators=[DataRequired(),
        Regexp('^[a-z]{6,8}$',message='Your username should be between 6 and 8 characters long, and can only contain lowercase letters.')])
        username = StringField('Username', validators=[DataRequired(),
        Regexp(...),EqualTo('confirm_username', message='Usernames do not match. Try again')])

class UserPost(FlaskForm):
    blogpost = StringField('BlogPost')
    submit = StringField('Submit')


class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')