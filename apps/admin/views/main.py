from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template as rt
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required
from flask_login import current_user
from config import config
import os
from models.users import *
from mongoengine.queryset import Q
from uilts import rest
bp = Blueprint("admin", __name__, url_prefix='/')


@bp.route('', methods=['GET', 'POST'])
def index():

    return rt('admin_main/login.html')


@bp.route('login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = request.form
        c = User.objects(Q(mobile=form.get('mobile')) | Q(mobile=form.get('username'))).first()
        if c:
            login_user(c)
            return rest.success(data={"url": url_for('customer_main.index')})
        return rest.params_error('请检查账号密码')
    return rt('admin_main/login.html')


@bp.route('register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(request.args.get('next') or url_for('main.home'))
    if request.method == 'POST':
        data = request.form
        c = Customer()
        c.mobile = data.get('mobile', '')
        c.username = data.get('username', '')
        c.sex = data.get('sex', '')
        c.password = data.get('password', 'abc123')
        c.save()
        return redirect(url_for('customer_main.index'))
    return rt('main/register.html', a=1)


@bp.route('logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(request.referrer)