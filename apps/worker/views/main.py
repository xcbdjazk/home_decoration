from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from flask import make_response
from flask import session
from flask import render_template as rt
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required
from flask_login import current_user
from config import config
import os
from models.users import *
from mongoengine.queryset import Q
from utils import rest
from utils.utils import ValidCodeImg
from utils.utils import random_filename
from bson import ObjectId

bp = Blueprint("worker_main", __name__, url_prefix='/worker')


@bp.route('/', methods=['GET', 'POST'])
def index():

    return rt('worker_main/index.html')
