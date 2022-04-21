from flask import flash, redirect, render_template, redirect, url_for, request
from app import app, db
from app.models import Post
from app.forms import FlaskPostForm


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
    post = Post.query.filter_by(id=post_id).first()
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', category='success')
    return redirect(url_for('index'))