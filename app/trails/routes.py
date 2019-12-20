from flask import Blueprint, render_template, redirect, flash, url_for
from flask import current_app as app
from flask import request
from flask_login import login_required, current_user
from sqlalchemy.sql import exists
from app import db
from app.trails.models import Trails
from app.status.models import Status
from app.users.models import User, reporters
from app.status.top import top_statuses
from app.trails.forms import TrailAddForm
from datetime import datetime

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
    # statuses = Status.query.order_by(Status.timestamp.desc()).limit(10)
    return render_template('index.html', statuses=statuses, status_index=status_index)


@trails_bp.route('/add_trail_system', methods=['GET', 'POST'])
@login_required
def add_trails():
    form = TrailAddForm()
    if form.validate_on_submit():
        trails = Trails(name=form.trail_name.data, trailforks=form.trailforks.data,
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
        trails.name = form.trail_name.data
        trails.city = form.city.data
        trails.province = form.province.data
        trails.trailforks = form.trailforks.data
        trails.approved = 1
        radbot = User.query.filter_by(username='RadBot').first()
        welcome_status = Status(author=radbot, body='Hi, I\'m ' + trails.name +
                                ', I\'m new here! Please update my status!', user_id=1, trail_system=trails.id)
        db.session.add(welcome_status)
        radbot.subscribe(trails)
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
    all_trail_names = [row.name for row in Trails.query.distinct().all()]
    all_trail_names.sort()
    statuses = []
    for name in all_trail_names:
        # This next line includes the not-exists filter to remove reported trails from a user's feed
        status = Status.query.join(Trails, (Status.trail_system == Trails.id)).filter(Status.active).filter(Trails.name == name).filter(
            ~ exists().where(reporters.c.reporter_id == current_user.id).where(reporters.c.reported_id == Status.id)).order_by(
            Status.timestamp.desc()).first()
        if not status:
            status = Status.query.join(Trails, (Status.trail_system == Trails.id)).filter(Status.active).filter(Trails.name == name).order_by(
                Status.timestamp.desc()).first()
            status.body = 'No unreported statuses available. Go write one!'
            status.user_id = User.query.filter_by(username='RadBot').first().id
            status.timestamp = datetime.utcnow()
        statuses.append(status)
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


@trails_bp.route('/trails/<trail_id>')
def trails(trail_id):
    page = request.args.get('page', 1, type=int)
    statuses = Status.query.filter(
        Status.trail_system == trail_id).filter(Status.active) \
        .filter(~ exists().where(reporters.c.reporter_id == current_user.id).where(reporters.c.reported_id == Status.id)) \
        .order_by(Status.timestamp.desc()).paginate(page, app.config['STATUSES_PER_PAGE'], False)
    if not statuses.items:
        statuses = Status.query.filter(
            Status.trail_system == trail_id) \
            .order_by(Status.timestamp.desc()).paginate(page, 1, False)
        statuses.items[0].user_id = User.query.filter_by(
            username='RadBot').first().id
        statuses.items[0].body = 'No unreported statuses.'
        statuses.items[0].timestamp = datetime.utcnow()

    next_url = url_for('trails_bp.trails', trail_id=trail_id,
                       page=statuses.next_num) if statuses.has_next else None
    prev_url = url_for('trails_bp.trails', trail_id=trail_id,
                       page=statuses.prev_num) if statuses.has_prev else None

    start_date = Status.query.filter_by(
        trail_system=trail_id).order_by(Status.timestamp.asc()).first()
    status_count = Status.query.filter_by(trail_system=trail_id).count()
    author_count = Status.query.filter_by(
        trail_system=trail_id).group_by(Status.user_id).count()
    trails_name = statuses.items[0].trails.name

    return render_template('trail_system.html', statuses=statuses.items,
                           title=trails_name+' Status', status_count=status_count,
                           author_count=author_count, start_date=start_date,
                           next_url=next_url, prev_url=prev_url)
