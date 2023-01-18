from flask import render_template, url_for
from blog import app, db
from blog.models import Post, User, Comments
from blog.forms import RegistrationForm, LoginForm, User, UserPost, UserComments, ProfilePicture
from flask import redirect, request, flash
from flask_login import login_user, logout_user,  current_user, login_required
from sqlalchemy import delete
from werkzeug.utils import secure_filename
import uuid as uuid
import os




@app.route("/")

@app.route("/home", methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        posts = Post.query.all()
        userPost = UserPost()   
        return render_template('home.html', posts=posts, userPost = userPost)
    else:
        return redirect(url_for('login'))

@app.route("/profile", methods=['GET','POST'])
def profile():
    if current_user.is_authenticated:
        form = ProfilePicture()
        profile_item = User.query.get_or_404(current_user.id) 
        print(form.validate_on_submit())
        if request.method == 'POST':
            profilepic=request.files['profile_pic']
            picturefilename = secure_filename(profilepic.filename)
            picture_id =str(uuid.uuid1()) + "_" + picturefilename
            saver = request.files['profile_pic']
            profile_item.image_file=picture_id
            
            try: 
                db.session.commit()
                saver.save(os.path.join(app.config['UPLOAD_FOLDER'], picture_id))
                print(saver)
            except:
                flash('Upload unsuccessful')

        return render_template('profile.html', title='profile', form=form, profile_item=profile_item)
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
    comments_to_delete =delete(Comments).where(Comments.post_id==id)
    try:
        db.session.delete(post_to_delete)
        db.session.execute(comments_to_delete)
        db.session.commit()
        flash('Post was deleted!')

        
        return redirect(url_for('home'))
    except:
       
        flash('Delete failed!')

        return redirect(url_for('home'))

@app.route('/userPost/<int:post_id>/comment/<int:id>')
def delete_comment(id, post_id):
    try:
        comment_to_delete =Comments.query.get_or_404(id)
        db.session.delete(comment_to_delete)
        db.session.commit()
        flash('Comment has been deleted!')

        return redirect(url_for('individualpost',id=post_id ))
    except:
        flash('Delete failed!')

        return redirect(url_for('individualpost', id=post_id))

@app.route('/userPost/<int:id>', methods=['GET','POST'])
def individualpost(id):
    addcomment = UserComments()
   
    post = Post.query.get_or_404(id)
    comments = Comments.query.filter_by(post_id=id).all()
    if addcomment.validate_on_submit():
        comment = Comments(comment=addcomment.comment.data,post_id=id, commenter_id=current_user.id)
        addcomment.comment.data = ''

        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('individualpost', id=id))
    return render_template('individualpost.html', post=post, comments=comments, usercomments=addcomment)

@app.route("/register",methods=['GET','POST'])
def register():
    form = RegistrationForm()
    
    if form.username.errors:
        for error in form.username.errors:
            flash(error)
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!')
        return redirect(url_for('login'))
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
            flash('Invalid username or password.')
    return render_template('login.html',title='Login',form=form)

@app.route("/logout")
def logout():
 
        logout_user()
        flash('Logout successful. See you soon!')
        return redirect(url_for('home'))
