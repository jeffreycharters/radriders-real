from flask import Blueprint, render_template, redirect, flash, url_for
from flask import current_app as app
from flask_login import login_required, current_user
from app import db
from app.trails.models import Trails
from app.status.models import Status
from app.status.top import top_statuses
from app.trails.forms import TrailAddForm

trails_bp = Blueprint('trails_bp', __name__,
                      template_folder='templates',
                      static_folder='static')


@trails_bp.route('/')
@trails_bp.route('/index')
def index():
    if current_user.is_anonymous:
        statuses = Status.query.order_by(
            Status.timestamp.desc()).filter_by(active=True).limit(10)
        return render_template('index.html', statuses=statuses, stranger=True)
    trails_to_get = current_user.subscribed.all()
    status_index, statuses = top_statuses(trails_to_get, 3)
    #statuses = Status.query.order_by(Status.timestamp.desc()).limit(10)
    return render_template('index.html', statuses=statuses, status_index=status_index)


@trails_bp.route('/add_trail_system', methods=['GET', 'POST'])
@login_required
def add_trails():
    form = TrailAddForm()
    if form.validate_on_submit():
        trails = Trails(name=form.trail_name.data,
                        city=form.city.data, province=form.province.data)
        db.session.add(trails)
        db.session.commit()
        flash('Trail Network has been submitted for approval.')
        return redirect(url_for('trails_bp.index'))
    return render_template('add.html', title='Add a Trail Network', form=form)


@trails_bp.route('/approve_trails', methods=['GET', 'POST'])
@login_required
def approve_trails():
    trails = Trails.query.filter_by(approved=0).first()
    form = TrailAddForm()
    if form.validate_on_submit():
        trails = Trails.query.filter_by(name=form.trail_name.data).first()
        trails.approved = 1
        welcome_status = Status(body='Hi, I\'m ' + trails.name +
                                ', I\'m new here! Please update my status!', user_id=1, trail_system=trails.id)
        db.session.add(welcome_status)
        db.session.commit()
        flash(f'{trails.name} approved!')
        return redirect(url_for('admin_bp.admin'))
    if trails is not None and current_user.admin:
        form = TrailAddForm(obj=trails, trail_name=trails.name)
        form.submit.label.text = 'Approve'
        approving = True
        trail_id = trails.id
        return render_template('add.html', title='Approve trails',
                               form=form, approving=approving, trail_id=trail_id)
    return redirect(url_for('trails_bp.index'))


@trails_bp.route('/explore_trails')
def explore_trails():
    statuses = Status.query.join(Trails, Status.trail_system == Trails.id).group_by(
        Trails.name).filter(Status.active == True).order_by(Trails.name).all()
    return render_template('explore.html', title='All of the trails', statuses=statuses, user=current_user)


@trails_bp.route('/reject_trails/<trail_id>')
@login_required
def reject_trails(trail_id):
    trails = Trails.query.filter_by(id=trail_id).first()
    flash(f'Rejected {trails.name} and removing from database..')
    Trails.query.filter_by(id=trail_id).delete()
    db.session.commit()
    flash(f'Successfully removed from database.')
    return redirect(url_for('trails_bp.approve_trails'))
