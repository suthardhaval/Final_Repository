from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError


class SubmitUserDetailsForm(FlaskForm):
    # title = StringField('Enter the Song Lyrics Below:', validators=[DataRequired()])
    # title = StringField('Comment', validators=[DataRequired()])
    content = TextAreaField('Id', validators=[DataRequired()])
    submit = SubmitField('Submit')


class QuestionsForm(FlaskForm):
    # title = StringField('Enter the Song Lyrics Below:', validators=[DataRequired()])
    # title = StringField('Comment', validators=[DataRequired()])
    content = TextAreaField('Id', validators=[DataRequired()])
    submit = SubmitField('Submit')