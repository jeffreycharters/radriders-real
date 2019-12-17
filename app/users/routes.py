from flask import Blueprint, render_template, redirect, flash, url_for, request, jsonify
from flask import current_app as app
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app.email import send_password_reset_email
from app.users.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm
from app.users.forms import ResetPasswordForm
from app.users.models import User
from app.trails.models import Trails
from app.status.models import Status
from werkzeug.urls import url_parse

users_bp = Blueprint('users_bp', __name__,
                     template_folder='templates',
                     static_folder='static')


@users_bp.route('/edit_profile/<user_id>')
@login_required
def edit_profile(user_id):
    return 'coming soon!'


@users_bp.route('/faq')
def faq():
    return render_template('faq.html')


@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('trails_bp.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('users_bp.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('trails_bp.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@users_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('trails_bp.index'))


@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('users_bp.login'))
    return render_template('register.html', title='Get Registered', form=form)


@users_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('trails_bp.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('trails_bp.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset')
        return redirect(url_for('users_bp.login'))
    return render_template('reset_password.html', form=form)


@users_bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for instruction to reset your password')
        return redirect(url_for('users_bp.login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


@users_bp.route('/subscribe/<trail_id>', methods=['GET', 'POST'])
def subscribe(trail_id):
    trails = Trails.query.filter_by(id=trail_id).first()
    if trails is not None:
        current_user.subscribe(trails)
    return jsonify({'response': 'Subscribed!'})


@users_bp.route('/unsubscribe/<trail_id>', methods=['GET', 'POST'])
def unsubscribe(trail_id):
    trails = Trails.query.filter_by(id=trail_id).first()
    if trails is not None:
        current_user.unsubscribe(trails)
    return jsonify({'response': 'Unsubscribed!'})


@users_bp.route('/users/<username>', methods=['GET'])
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    total_count = Status.query.filter_by(author=user).count()
    statuses = Status.query.filter_by(author=user).order_by(
        Status.timestamp.desc()).paginate(1, 3, False)
    return render_template('user.html', user=user, statuses=statuses.items,
                           title=user.username+'\'s Profile', total_count=total_count)
