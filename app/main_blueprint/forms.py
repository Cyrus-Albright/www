from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField


class FileuploadForm(FlaskForm):
    file = FileField(label="文件上传", validators=[FileRequired()])
    submmit = SubmitField(label="上传")
