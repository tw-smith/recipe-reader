from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField
from wtforms.validators import DataRequired

class UploadForm(FlaskForm):
    file = FileField('Image File', validators=[DataRequired()])
    submit = SubmitField('Upload File')
