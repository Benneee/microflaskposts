from flask import flash, redirect, render_template, redirect, url_for, request
from flask_login import current_user, login_required, login_user
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
    # When we add a user system, we need to add some validations here to be sure the 
    # active user is the post's author
    form = FlaskPostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.commit()
        flash('Post has been updated successfully', category='success')
        return redirect(url_for('index'))

    elif request.method == 'GET':
        form.title.data = post.title
        form.body.data = post.body
    
    return render_template('handle-post.html', title="Update Post", form=form, post=post)

@app.route('/posts/<post_id>')
@login_required
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    # When we add a user system, we need to add some validations here to be sure the 
    # active user is the post's author
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
        if user and user.check_password(form.password.data) != True:
            login_user(user=user)
            flash(message='Login successful')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash(message='Password or username incorrect', category='danger')
    return render_template('login.html', title='Login', form=form)
