from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from .conf import Config


login_manager = LoginManager()
config = Config
mongo = MongoEngine()
