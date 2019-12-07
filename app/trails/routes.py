from flask import Blueprint, render_template, redirect, flash, url_for
from flask import current_app as app
from app.trails.models import Trails

trails_bp = Blueprint('trails_bp', __name__,
                     template_folder='templates',
                     static_folder='static')

@trails_bp.route('/')
@trails_bp.route('/index')
def index():
    return render_template('index.html')

@trails_bp.route('/trails', methods=['GET'])
def trails():
    return 'Testing'