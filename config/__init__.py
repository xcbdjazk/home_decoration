from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from .conf import Config


login_manager = LoginManager()
config = Config
mongo = MongoEngine()
bootstrap = Bootstrap()
