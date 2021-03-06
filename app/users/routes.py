from flask import Blueprint, render_template, redirect, flash, url_for, request, jsonify
from flask import current_app as app
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app.email import send_password_reset_email
from app.users.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm
from app.users.forms import ResetPasswordForm, EditProfileForm, ChangePasswordForm
from app.users.models import User
from app.trails.models import Trails
from app.status.models import Status
from werkzeug.urls import url_parse

users_bp = Blueprint('users_bp', __name__,
                     template_folder='templates',
                     static_folder='static')


@users_bp.route('/change_password/<user_id>', methods=['GET', 'POST'])
@login_required
def change_password(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user != current_user:
        return redirect(url_for('trails_bp.index'))
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user.set_password(form.new_password.data)
        db.session.add(user)
        db.session.commit()
        flash('Password successfully changed!')
        redirect(url_for('users_bp.users', username=user.username))
    return render_template('change_password.html', form=form, title='Change Password')


@users_bp.route('/edit_profile/<user_id>', methods=['GET', 'POST'])
@login_required
def edit_profile(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user != current_user and not current_user.admin:
        return redirect(url_for('trails_bp.index'))
    form = EditProfileForm(user.username)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
        form.about_me.data = user.about_me
    return render_template('edit_profile.html', user=user, form=form, title='Edit Profile')


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
        elif not user.is_active():
            flash('Your account has been inactivated! Let time pass or contact us.')
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
    return render_template('reset_password.html', form=form, title='Password Reset Time!')


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
def users(username):
    user = User.query.filter_by(username=username).first_or_404()
    total_count = Status.query.filter(
        Status.active).filter_by(author=user).count()
    page = request.args.get('page', 1, type=int)
    statuses = Status.query.filter(Status.active).filter_by(author=user).order_by(
        Status.timestamp.desc()).paginate(page, app.config['STATUSES_PER_PAGE'], False)

    username = user.username
    next_url = url_for('users_bp.users', username=username, page=statuses.next_num) \
        if statuses.has_next else None
    prev_url = url_for('users_bp.users', username=username, page=statuses.prev_num) \
        if statuses.has_prev else None

    return render_template('user.html', user=user, statuses=statuses.items,
                           title=user.username+'\'s Profile', total_count=total_count,
                           prev_url=prev_url, next_url=next_url)
