from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask import current_app as app
from flask_login import current_user, login_required
from app import db
from app.status.models import Status
from app.trails.models import Trails
from app.trails.forms import TrailAddForm
from app.users.models import User
from werkzeug.urls import url_parse

admin_bp = Blueprint('admin_bp', __name__,
                     template_folder='templates',
                     static_folder='static')


@admin_bp.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if not current_user.admin:
        return redirect(url_for('trails_bp.index'))
    trails_to_approve = Trails.query.filter_by(approved=0).count()
    return render_template('admin.html', title='Administration',
                           trails_to_approve=trails_to_approve)


@admin_bp.route('/activate/<table>-<id>')
@login_required
def activate(table, id):
    if not current_user.admin:
        return redirect(url_for('trails_bp.index'))
    if table == 'user':
        item = User.query.filter_by(id=id).first()
    elif table == 'trails':
        item = Trails.query.filter_by(id=id).first()
    if item is None:
        flash('Couldn\'t find item ' + id)
        return redirect(url_for('admin_bp.list_'+table))
    item.activate()
    flash('Activated ' + table + ': ' + str(item.id))
    return redirect(url_for('admin_bp.list_'+table))


@admin_bp.route('/deactivate/<table>-<id>')
@login_required
def deactivate(table, id):
    if not current_user.admin:
        return redirect(url_for('trails_bp.index'))
    if table == 'user':
        item = User.query.filter_by(id=id).first()
    elif table == 'trails':
        item = Trails.query.filter_by(id=id).first()
    if item is None:
        flash('Couldn\'t find item ' + id)
        return redirect(url_for('admin_bp.list_'+table))
    item.deactivate()
    flash('Deactivated ' + table + ': ' + str(item.id))
    return redirect(url_for('admin_bp.list_'+table))


@admin_bp.route('/edit_trails/<trails_id>', methods=['GET', 'POST'])
def edit_trails(trails_id):
    if not current_user.admin:
        return redirect(url_for('trails_bp.index'))
    trails = Trails.query.filter_by(id=trails_id).first_or_404()
    form = TrailAddForm()
    if form.validate_on_submit():
        trails.name = form.trail_name.data
        trails.city = form.city.data
        trails.province = form.province.data
        trails.trailforks = form.trailforks.data
        db.session.commit()
        return redirect(url_for('admin_bp.list_trails'))
    elif request.method == 'GET':
        form.trail_name.data = trails.name
        form.city.data = trails.city
        form.province.data = trails.province
        form.trailforks.data = trails.trailforks
        form.submit.label.text = 'Update'
    return render_template('edit_trails.html', title='Edit Trails',
                           form=form, trails=trails)


@admin_bp.route('/list_status')
@login_required
def list_status():
    if not current_user.admin:
        return redirect(url_for('trails_bp.index'))
    items = Status.query.order_by(Status.timestamp.desc()).all()
    return render_template('list_status.html', title='Status List', items=items)


@admin_bp.route('/list_trails')
@login_required
def list_trails():
    if not current_user.admin:
        return redirect(url_for('trails_bp.index'))
    titles = Trails.__table__.columns.keys()
    items = Trails.query.all()
    return render_template('list_trails.html', title='Trails List',
                           items=items, titles=titles)


@admin_bp.route('/list_user')
@login_required
def list_user():
    if not current_user.admin:
        return redirect(url_for('trails_bp.index'))
    titles = User.__table__.columns.keys()
    items = User.query.all()
    return render_template('list_user.html', title='User List',
                           items=items, titles=titles)
