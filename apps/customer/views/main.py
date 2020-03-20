from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template as rt
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required
from config import config
import os
from models.users import *
from mongoengine.queryset import Q

bp = Blueprint("customer_main", __name__, url_prefix='/customer/')


@bp.route('', methods=['GET', 'POST'])
def index():

    return rt('customer_main/index.html')
