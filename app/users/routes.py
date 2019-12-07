from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask import current_app as app
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app.users.forms import LoginForm, RegistrationForm
from app.users.models import User
from werkzeug.urls import url_parse

users_bp = Blueprint('users_bp', __name__,
                     template_folder='templates',
                     static_folder='static')


@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
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
        print('Validated')
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('users_bp.login'))
    print('No validated')
    return render_template('register.html', title='Get Registered', form=form)


@users_bp.route('/user/<username>', methods=['GET'])
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    status = [
        {'author': user, 'body': 'Test status 1'}
    ]
    return render_template('user.html', username=username)
