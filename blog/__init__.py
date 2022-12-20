from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f2d927ffaf18f67a6c516b45f9609cc0d457726baae29d26'

from blog import routes