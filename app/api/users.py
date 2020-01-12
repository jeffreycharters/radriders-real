from flask import jsonify, request

from app.users.models import User
from app.users.models import Status
from app.api import bp


@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())


@bp.route('users/<int:id>/statuses', methods=['GET'])
def get_user_statuses(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Status.to_collection_dict(
        Status.query.filter_by(user_id=user.id), page, per_page, 'api.get_user_statuses', id=id)
    return jsonify(data)


@bp.route('users/<int:id>/subscriptions')
def get_user_subscriptions(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(
        user.subscribed, page, per_page, 'api.get_user_subscriptions', id=id)
    return jsonify(data)
