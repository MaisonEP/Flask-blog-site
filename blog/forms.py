from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField 
from blog.models import User, Comments
from wtforms.validators import DataRequired, ValidationError, EqualTo, Regexp
from wtforms.widgets import TextArea
from flask_wtf.file import FileField
from flask_ckeditor import CKEditorField



class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),  
        Regexp('^[A-Za-z0-9]{4,15}$', message='Your username should be between 4 and 15 characters long, and can only contain letters amd numbers.'),
        EqualTo('confirm_username', message='Usernames do not match. Try again')
    ])
    confirm_username = StringField('Confirm Username',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register') 

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already exist. Please choose a different one.')

class UserPost(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    blogpost = CKEditorField('BlogPost', validators=[DataRequired()])
    submit = StringField('Submit')

class UserComments(FlaskForm):
    comment = StringField('Add comment', validators=[DataRequired()], widget=TextArea ())
    submit = StringField('Submit')


class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')

class ProfilePicture(FlaskForm):
    profile_pic = FileField("Profile Picture", validators=[DataRequired()])
    submit =SubmitField('Submit')
