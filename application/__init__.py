from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=False)

    app.config.from_object('config.Config')

    with app.app_context():
        from application import routes
        from .users import users_routes

        app.register_blueprint(users_routes.users_bp)

    return app
