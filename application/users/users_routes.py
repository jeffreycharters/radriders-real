from flask import Blueprint, render_template
from flask import current_app as app

users_bp = Blueprint('users_bp', __name__,
                    template_folder='templates',
                    static_folder='static')

@users_bp.route('/user/<username>', methods=['GET'])
def user(username):
    return render_template('user.html', username=username)