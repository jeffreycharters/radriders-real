from app.status.models import Status


def top_statuses(trails, number=3):
    trail_list = []
    for trail in trails:
        trail_list.append(trail.id)
    status_list = []
    status_index = []
    while len(trail_list) > 0:
        most_recent = Status.query.filter(
            Status.trail_system.in_(trail_list)).order_by(Status.timestamp.desc()).first()
        most_recent_id = most_recent.trails.id
        most_recent_updates = Status.query.filter_by(
            trail_system=most_recent_id).order_by(Status.timestamp.desc()).limit(number).all()
        for update in most_recent_updates:
            status_list.append(update)
        status_index.append(len(most_recent_updates))
        trail_list.remove(most_recent_id)

    return status_index, status_list
