from flask import Blueprint
from flask import current_app as app

errors_bp = Blueprint('errors', __name__)

from app.errors import handlers