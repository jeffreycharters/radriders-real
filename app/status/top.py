from app.status.models import Status


# This function takes a list of trail objects and the number of updates requested
# and returns an index list of how many updates per trail system and the list of
# status objects.
def top_statuses(trails, number=3):

    # Populate a list with the IDs of the subscribed trail systems.
    subscribed_trails_list = []
    for trail in trails:
        subscribed_trails_list.append(trail.id)

    # Make a list of only trail system with status updates to avoid errors.
    trails_with_statuses = Status.query.group_by(Status.trail_system).all()
    trails_with_statuses_ids = []
    for trail in trails_with_statuses:
        trails_with_statuses_ids.append(trail.trails.id)
    trails_to_display = []
    for trail in subscribed_trails_list:
        if trail in trails_with_statuses_ids:
            trails_to_display.append(trail)

    # Pull out the top <number> most recent updates, starting with most recent.
    status_list = []
    status_index = []
    while len(trails_to_display) > 0:
        most_recent = Status.query.filter(
            Status.trail_system.in_(trails_to_display)).order_by(Status.timestamp.desc()).first()
        most_recent_id = most_recent.trails.id
        most_recent_updates = Status.query.filter_by(
            trail_system=most_recent_id).order_by(Status.timestamp.desc()).limit(number).all()
        for update in most_recent_updates:
            status_list.append(update)
        status_index.append(len(most_recent_updates))
        trails_to_display.remove(most_recent_id)

    return status_index, status_list
