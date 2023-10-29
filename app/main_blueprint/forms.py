from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField


class FileuploadForm(FlaskForm):
    file = FileField(validators=[FileRequired()])
    submmit = SubmitField()