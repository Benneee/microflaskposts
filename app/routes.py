from flask import flash, redirect, render_template, redirect, url_for
from app import app, db
from app.models import Post
from app.forms import FlaskPostForm


@app.route('/', methods=['GET', 'POST'])
def index():
    form = FlaskPostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data)
        db.session.add(post)
        db.session.commit()
        flash('Post added successfully!', category="success")
        return redirect(url_for('index'))
    return render_template('index.html', title="MicroFlaskPosts", form=form)