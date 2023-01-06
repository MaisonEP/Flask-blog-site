from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'f2d927ffaf18f67a6c516b45f9609cc0d457726baae29d26'

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'blog.db')

db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)
from blog import routes