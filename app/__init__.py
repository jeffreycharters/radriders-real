from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, instance_relative_config=False)

    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from app import routes
        from .users import routes as users_routes
        from .status import routes as status_routes

        app.register_blueprint(users_routes.users_bp)
        app.register_blueprint(status_routes.status_bp)

    return app
