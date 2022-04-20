from flask import render_template
from app import app
from app.forms import FlaskPostForm


@app.route('/')
def index():
    form = FlaskPostForm()
    return render_template('index.html', title="MicroFlaskPosts", form=form)