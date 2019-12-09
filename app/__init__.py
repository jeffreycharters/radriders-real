from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from config import Config
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
moment = Moment()


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=False)

    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)
    login.init_app(app)
    login.login_view = 'users_bp.login'

    with app.app_context():
        from app.errors import errors_bp
        from .users import routes as users_routes
        from .status import routes as status_routes
        from .trails import routes as trails_routes
        from .admin import routes as admin_routes

        app.register_blueprint(errors_bp)
        app.register_blueprint(admin_routes.admin_bp)
        app.register_blueprint(users_routes.users_bp)
        app.register_blueprint(status_routes.status_bp)
        app.register_blueprint(trails_routes.trails_bp)

    # Send myself emails when something breaks
    if not app.debug:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@radriders.ca',
                toaddrs=app.config['ADMINS'],
                subject='RadRiders MTB failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

    # File-based error logging
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/radriders.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('RadRiders startup')

    return app
