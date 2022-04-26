from flask import flash, redirect, render_template, redirect, url_for, request
from app import app, db
from app.models import Post
from app.forms import FlaskPostForm



@app.route('/', methods=['GET', 'POST'])
def index():
    posts = []
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=app.config['POSTS_PER_PAGE'])
    return render_template('index.html', title="MicroFlaskPosts", posts=posts.items)

@app.route('/create-post', methods=['GET', 'POST'])
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
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    # When we add a user system, we need to add some validations here to be sure the 
    # active user is the post's author
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', category='success')
    return redirect(url_for('index'))