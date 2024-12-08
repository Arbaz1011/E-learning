from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class CourseForm(FlaskForm):
    title = StringField('Course Title', validators=[
        DataRequired(),
        Length(min=5, max=200, message="Title must be between 5 and 200 characters")
    ])
    description = TextAreaField('Course Description', validators=[
        DataRequired(),
        Length(min=50, max=5000, message="Description must be between 50 and 5000 characters")
    ])
    pdf_file = FileField('Course PDF', validators=[
        FileAllowed(['pdf'], 'Only PDF files are allowed!')
    ])
    submit = SubmitField('Save Course')

class LessonForm(FlaskForm):
    title = StringField('Lesson Title', validators=[
        DataRequired(),
        Length(min=3, max=200, message="Title must be between 3 and 200 characters")
    ])
    content = TextAreaField('Lesson Content', validators=[
        DataRequired(),
        Length(min=50, max=10000, message="Content must be between 50 and 10000 characters")
    ])
    file = FileField('Upload Materials (Optional)')
    submit = SubmitField('Save Lesson')
