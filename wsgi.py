from app.status.models import Status
from app.users.models import User
from app import db
from app import create_app


app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Status': Status}


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
