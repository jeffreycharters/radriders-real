from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.trails.models import Trails


class TrailAddForm(FlaskForm):
    trail_name = StringField('Trail System Name', validators=[
                             DataRequired(), Length(min=1, max=64)])
    city = StringField('Nearest City', validators=[
                       DataRequired(), Length(min=1, max=64)])
    provinces = [('ON', 'ON'), ('AB', 'AB'), ('BC', 'BC'), ('MB', 'MB'), ('NB', 'NB'), ('NL', 'NL'),
                 ('NS', 'NS'), ('NT', 'NT'), ('NU', 'NU'), ('PE', 'PE'), ('QC', 'QC'), ('SK', 'SK'), ('YT', 'YT')]
    province = SelectField('Province', choices=provinces)
    submit = SubmitField('Submit for Approval')
