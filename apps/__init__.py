from flask import Flask
from config import mongo
from config import config
from config import login_manager
from config.rejister import register_jinja
from apps.customer.views import main


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    mongo.init_app(app)
    login_manager.init_app(app)

    register_jinja(app)
    register_bp(app)
    return app


def register_bp(app):
    app.register_blueprint(main.bp)