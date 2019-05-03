from flask_wtf import FlaskForm
from wtforms import MultipleFileField,validators
from flask_wtf.file import FileAllowed, FileRequired

class DocsForm(FlaskForm):
    files = MultipleFileField('Document(s) Upload',[validators.DataRequired()])
        #FileRequired(),
        #FileAllowed(['txt'], 'text files only')])

