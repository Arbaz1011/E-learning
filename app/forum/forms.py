from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class TopicForm(FlaskForm):
    title = StringField('Title', validators=[
        DataRequired(),
        Length(min=5, max=200)
    ])
    content = TextAreaField('Content', validators=[
        DataRequired(),
        Length(min=10, max=10000)
    ])
    submit = SubmitField('Create Topic')

class PostForm(FlaskForm):
    content = TextAreaField('Content', validators=[
        DataRequired(),
        Length(min=1, max=10000)
    ])
    submit = SubmitField('Post Reply')
