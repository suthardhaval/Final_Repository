from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError


class SubmitSongForm(FlaskForm):
    # title = StringField('Enter the Song Lyrics Below:', validators=[DataRequired()])
    # title = StringField('Comment', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')