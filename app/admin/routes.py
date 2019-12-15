from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask import current_app as app
from flask_login import current_user, login_required
from app import db
from app.status.models import Status
from app.trails.models import Trails
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


@admin_bp.route('/faq')
def faq():
    return 'coming soon.'


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
    items = Trails.query.all()
    return render_template('list_trails.html', title='Trails List', items=items)


@admin_bp.route('/list_users')
@login_required
def list_users():
    if not current_user.admin:
        return redirect(url_for('trails_bp.index'))
    items = User.query.all()
    return render_template('list_users.html', title='User List', items=items)
