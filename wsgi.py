from app.status.models import Status
from app.users.models import User
from app.trails.models import Trails
from app import db
from app import create_app


# Create the app itself.
app = create_app()


# Need this to run a flask shell, useful for debugging.
# At Bash prompt, enter 'flask shell'
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Status': Status, 'Trails': Trails}


# If this is the entry point to the app, run on this host so can get access
# From other devices on the network.
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
