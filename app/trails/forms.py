from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.trails.models import Trails


class TrailAddForm(FlaskForm):
    trail_name = StringField('Trail System Name', validators=[
                             DataRequired(), Length(min=1, max=64)])
    city = StringField('Nearest City', validators=[
                       DataRequired(), Length(min=1, max=64)])
    provinces = [('ON', 'Ontario'), ('AB', 'Alberta'), ('BC', 'British CColumbia'), ('MB', 'Manitoba'), ('NB', 'New Brunswick'), ('NL', 'Newfoundland & Labrador'),
                 ('NS', 'Nove Scotia'), ('NT', 'Northwest Territories'), ('NU', 'Nunavut'), ('PE', 'Prince Edward Island'), ('QC', 'Québec'), ('SK', 'Saskatchewan'), ('YT', 'Yukon')]
    province = SelectField('Province', choices=provinces)
    trailforks = StringField(
        'Trailforks Link (e.g. https://www.trailforks.com/dir/trails)',
        render_kw={'placeholder': 'Leave blank if feeling lazy.'})
    submit = SubmitField('Submit for Approval')
