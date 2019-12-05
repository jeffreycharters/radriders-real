from flask import Blueprint, render_template, redirect, flash, url_for
from flask import current_app as app
from app.status.models import Status

status_bp = Blueprint('status_bp', __name__,
                     template_folder='templates',
                     static_folder='static')


@status_bp.route('/status', methods=['GET', 'POST'])
def login():
    return 'Testing'