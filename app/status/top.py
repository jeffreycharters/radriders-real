from app.status.models import Status


# This function takes a list of trail objects and the number of updates requested
# and returns an index list of how many updates per trail system and the list of
# status objects.
def top_statuses(trails, number=3):

    # Populate a list with the IDs of the subscribed trail systems.
    trails_list = []
    for trail in trails:
        trails_list.append(trail.id)

    # Pull out the top <number> most recent updates, starting with most recent.
    status_list = []
    status_index = []
    while len(trails_list) > 0:
        most_recent = Status.query.filter(
            Status.trail_system.in_(trails_list)).filter(Status.active == True).order_by(Status.timestamp.desc()).first()
        most_recent_id = most_recent.trails.id
        most_recent_updates = Status.query.filter_by(
            trail_system=most_recent_id).filter(Status.active == True).order_by(Status.timestamp.desc()).limit(number).all()
        for update in most_recent_updates:
            status_list.append(update)
        status_index.append(len(most_recent_updates))
        trails_list.remove(most_recent_id)

    return status_index, status_list
