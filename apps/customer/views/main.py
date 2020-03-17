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
bp = Blueprint("customer_main", __name__, url_prefix='/customer/',
               template_folder=os.path.join(config.base_dir, 'apps', 'customer', 'templates'))


@bp.route('', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        form = request.form
        c = Customer.objects(mobile=form.get('mobile')).first()
        if c:
            login_user(c)
        return redirect(url_for('customer_main.index'))
    return rt('main/index.html', a=1)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        c = Customer()
        c.mobile = data.get('mobile', '')
        c.username = data.get('username', '')
        c.username = data.get('sex', '')
        c.password = "123"
        c.save()
        return redirect(url_for('customer_main.index'))
    return rt('main/register.html', a=1)