from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired


class FlaskPostForm(FlaskForm):
    title = StringField(label='Title', validators=[DataRequired()])
    body = TextAreaField(label='Body', validators=[DataRequired()])