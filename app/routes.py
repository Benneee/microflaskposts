from flask import flash, redirect, render_template, redirect, url_for, request
from app import app, db
from app.models import Post
from app.forms import FlaskPostForm


# Consider a refactor here
# We move the creation of posts to its own method
# This method should now only cater for displaying of posts on the homepage

# For the create_post method
# It takes all the code here necessary for creating a new post
# On the UI, we add a button on the navbar to add new post that navigates to the page for new post
@app.route('/', methods=['GET', 'POST'])
def index():
    form = FlaskPostForm()
    posts = []
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data)
        db.session.add(post)
        db.session.commit()
        flash('Post added successfully!', category="success")
        return redirect(url_for('index'))
    elif request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('index.html', title="MicroFlaskPosts", form=form, posts=posts.items)


@app.route('/posts/<post_id>')
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    # When we add a user system, we need to add some validations here to be sure the 
    # active user is the post's author
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', category='success')
    return redirect(url_for('index'))


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
    
    return render_template('update-post.html', title="Update Post", form=form, post=post)