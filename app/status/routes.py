from flask import Blueprint, render_template, redirect, flash, url_for
from flask import current_app as app, request
from flask_login import login_required, current_user
from app import db
from app.status.models import Status
from app.status.forms import NewStatusForm
from app.trails.models import Trails

status_bp = Blueprint('status_bp', __name__,
                      template_folder='templates',
                      static_folder='static')


@status_bp.route('/new_status', methods=['GET', 'POST'])
@login_required
def new_status():
    form = NewStatusForm()
    all_trail_names = Trails.query.distinct(
        Trails.name).order_by(Trails.name.asc()).all()
    form.trails.choices = [(t.id, t.name) for t in all_trail_names]
    if form.validate_on_submit():
        trail_network = Trails.query.filter_by(id=form.trails.data).first()
        status = Status(author=current_user,
                        trails=trail_network, body=form.body.data)
        db.session.add(status)
        db.session.commit()
        flash('Status updated successfully!')
        return redirect(url_for('trails_bp.index'))
    return render_template('new.html', title='New Trail Status', form=form)


@status_bp.route('/report/<status_id>')
def report_status(status_id):
    status = Status.query.filter_by(id=status_id).first()
    if status:
        status.reported += 1
        if status.reported > 4:
            status.deactivate()
        db.session.commit()
        flash('This status has been brought to the moderators\' attention. Justice will \
            be administered swiftly and harshly. Thank you for narcking.')
    else:
        flash('Error! Not reported.')
    return redirect(url_for('trails_bp.index'))


@status_bp.route('/status', methods=['GET', 'POST'])
def login():
    return 'Testing'
