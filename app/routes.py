from flask import flash, redirect, render_template, redirect, url_for, request
from flask_login import current_user, login_required, login_user, logout_user
from app import app, db
from app.models import Post, User
from app.forms import FlaskPostForm, LoginForm, RegisterForm


@app.route('/home', methods=['GET', 'POST'])
@login_required
def index():
    posts = []
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=app.config['POSTS_PER_PAGE'])
    return render_template('index.html', title="MicroFlaskPosts", posts=posts.items)

@app.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = FlaskPostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data)
        db.session.add(post)
        db.session.commit()
        flash('Post added successfully!', category="success")
        return redirect(url_for('index'))

    elif request.method == 'GET':
        return render_template('handle-post.html', title='Create Post', form=form)

@app.route('/posts/<post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if post.author != current_user:
        flash(message='You are not allowed to edit this post', category='info')
        return redirect(url_for('index'))
    
    form = FlaskPostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.commit()
        flash('Post has been updated successfully', category='success')
        return redirect(url_for('index'))

    elif request.method == 'GET':
        form.body.data = post.body
    
    return render_template('handle-post.html', title="Update Post", form=form, post=post)

@app.route('/posts/<post_id>')
@login_required
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if post.author != current_user:
        flash(message='You are not allowed to delete this post', category='info')
        return redirect(url_for('index'))
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', category='success')
    return redirect(url_for('index'))



# Auth routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data) == True:
            login_user(user=user)
            flash(message='Login successful', category='success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash(message='Password or username incorrect', category='danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        # Create the user instance
        user = User(username=form.username.data, email=form.email.data)
        # This hashes the password and adds the password to the user object
        user.set_password(form.password.data)
        # Add and commit user to the DB
        db.session.add(user)
        db.session.commit()
        flash(message='Registration successful. You can now log in!', category='success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)