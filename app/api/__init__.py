from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api import status, users, trails, errors, tokens