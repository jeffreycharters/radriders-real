from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.trails.models import Trails


class NewStatusForm(FlaskForm):
    trails = SelectField('Trail Network', coerce=int)
    body = TextAreaField('Status', validators=[DataRequired(), Length(min=1, max=280)],
                         render_kw={'placeholder': 'How are the trails?'})
    submit = SubmitField('Add Status')

    def validate_trails(self, trails):
        if trails.data == -666:
            raise ValidationError('Come on, pick a real trail.')
