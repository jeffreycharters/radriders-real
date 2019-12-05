from flask import Blueprint, render_template, redirect, flash, url_for
from flask import current_app as app
from app.users.forms import LoginForm
from app.users.models import User

users_bp = Blueprint('users_bp', __name__,
                     template_folder='templates',
                     static_folder='static')


@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login requested for user {form.username.data}, \
              remember me={form.remember_me.data}')
        redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@users_bp.route('/user/<username>', methods=['GET'])
def user(username):
    return render_template('user.html', username=username)
