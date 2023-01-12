from flask import render_template, url_for
from blog import app, db
from blog.models import Post, User
from blog.forms import RegistrationForm, LoginForm, User, UserPost
from flask import redirect, request, flash
from flask_login import login_user, logout_user,  current_user, login_required





@app.route("/")

@app.route("/home", methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        posts = Post.query.all()
        userPost = UserPost()   
        return render_template('home.html', posts=posts, userPost = userPost)
    else:
        return redirect(url_for('login'))

@app.route("/about")
def about():
    if current_user.is_authenticated:
        return render_template('about.html', title='About Me')
    else:
        return redirect(url_for('login'))
    #add post page
@app.route('/add-blog', methods=['GET', 'POST'])
def add_blog():
    form = UserPost()    
    if form.validate_on_submit():

        post= Post(title=form.title.data, content=form.blogpost.data, poster_id=current_user.id)
        #clear form after submit
        form.title.data = ''
        form.blogpost.data= ''
        #add post to database
        db.session.add(post)
        db.session.commit()
        #blog confirmation message
        flash('Blog Posted Sucessfully!')
        return redirect(url_for('home'))
    return render_template('post.html',form=form)

@app.route('/post/delete/<int:id>')
def delete_post(id):
    post_to_delete= Post.query.get_or_404(id)
    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        flash('Post was deleted!')

        print('helloooo')
        return redirect(url_for('home'))
    except:
        print('snakehhhhh' )
        flash('Delete failed!')

        return redirect(url_for('home'))

@app.route('/userPost/<int:id>')
def individualpost(id):
    post = Post.query.get_or_404(id)
    return render_template('individualpost.html', post=post)

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
