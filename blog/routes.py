from flask import render_template, url_for
from blog import app, db
from blog.models import Post, User
from blog.forms import RegistrationForm, LoginForm, User 
from flask import redirect, request, flash
from flask_login import login_user, logout_user,  current_user





@app.route("/")

@app.route("/home")
def home():
    if current_user.is_authenticated:
        posts = Post.query.all()
        return render_template('home.html', posts=posts)
    else:
        return redirect(url_for('login'))

@app.route("/about")
def about():
    if current_user.is_authenticated:
        return render_template('about.html', title='About Me')
    else:
        return redirect(url_for('login'))

@app.route("/register",methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!')
        return redirect(url_for('registered'))
    else: 
            flash('Invalid email address or password.')
        
    return render_template('register.html',title='Register',form=form)

@app.route("/registered")
def registered():
    return render_template('registered.html', title='Thanks!')

@app.route("/login",methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash('You\'ve successfully logged in.')
        return redirect(url_for('home'))
    else:
            flash('Invalid username address or password.')
    return render_template('login.html',title='Login',form=form)

@app.route("/logout")
def logout():
 
        logout_user()
        flash('Logout successful. Bye!')
        return redirect(url_for('home'))
