from datetime import datetime
from blog import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import uuid as uuid

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(40), nullable=True, default='default.jpg')
    poster_id = db.Column(db.VARCHAR(36), db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.date}', '{self.title}', '{self.content}')"
    


class User(UserMixin,db.Model):
    id = db.Column(db.VARCHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(15), unique=True, nullable=False)
    hashed_password = db.Column(db.String(128))
    post = db.relationship('Post', backref='post', lazy=True)
    image_file = db.Column(db.String(200), nullable=True, default='Default_User_pic.jpg')
    userCommentsRelationship =  db.relationship('Comments', backref='userCommentsRelationship', lazy=True)
    

    def __repr__(self):
        return f"User('{self.username}')"
        
    @property
    def password(self):
        raise AttributeError('Password is not readable.')
    @password.setter
    def password(self,password):
        self.hashed_password=generate_password_hash(password)
    def verify_password(self,password):
        return check_password_hash(self.hashed_password, password)

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    commenter_id = db.Column(db.VARCHAR(36), db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)