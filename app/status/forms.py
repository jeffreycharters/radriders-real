from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.trails.models import Trails


class NewStatusForm(FlaskForm):
    trails = SelectField('Trail Network', coerce=int)
    body = TextAreaField('Status', validators=[DataRequired()])
    submit = SubmitField('Add Status')
