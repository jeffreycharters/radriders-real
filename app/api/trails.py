from flask import jsonify

from app.trails.models import Trails
from app.api import bp


@bp.route('/trails/<int:id>', methods=['GET'])
def get_trails(id):
    return jsonify(Trails.query.get_or_404(id).to_dict())
