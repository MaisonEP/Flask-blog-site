from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_ckeditor import CKEditorField, CKEditor



app = Flask(__name__)
app.config['SECRET_KEY'] = 'f2d927ffaf18f67a6c516b45f9609cc0d457726baae29d26'
ckeditor = CKEditor(app)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c22028814:newStud01!@csmysql.cs.cf.ac.uk:3306/c22028814_dynamicwebapp'

app.config['UPLOAD_FOLDER'] = 'blog/static'
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)
from blog import routes