from app.status.models import Status
from app.trails.models import Trails
from app.api import bp
from flask import jsonify, request


@bp.route('/statuses', methods=['GET'])
def get_statuses():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Status.to_collection_dict(
        Status.query, page, per_page, 'api.get_statuses')
    return jsonify(data)


@bp.route('/status/<int:id>', methods=['GET'])
def get_status(id):
    return jsonify(Status.query.filter_by(id=id).first_or_404().to_dict())


@bp.route('/trails/<int:id>/latest', methods=['GET'])
def get_latest(id):
    latest = Status.query.filter_by(trail_system=id).filter(
        Status.active).order_by(Status.id.desc()).first()
    return jsonify(latest.to_dict())
