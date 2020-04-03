from flask import Flask
from config import mongo
from config import config
from config import login_manager
from config import bootstrap
from config.rejister import register_jinja
from config.rejister import register_data
from apps.customer.views import main as customer_admin
from apps.admin.views import main as admin_main


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    mongo.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)

    register_jinja(app)
    register_bp(app)
    register_data(app)
    return app


def register_bp(app):
    app.register_blueprint(admin_main.bp)
    app.register_blueprint(customer_admin.bp)
