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
bp = Blueprint("admin", __name__, url_prefix='/')


@bp.route('', methods=['GET', 'POST'])
def index():

    return redirect(request.args.get('next') or url_for('customer_main.index'))


@bp.route('login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = request.form
        c:User = User.objects(Q(mobile=form.get('mobile')) | Q(mobile=form.get('username'))).first()
        if c and c.verify_password(form.get('password')):
            login_user(c)
            return rest.success(data={"url": url_for('customer_main.index')})
        return rest.params_error('请检查账号密码')
    return rt('admin_main/login.html')


@bp.route('register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(request.args.get('next') or url_for('customer.index'))
    if request.method == 'POST':
        data = request.form

        if session['images_code'] != data['code'].lower():
            return rest.params_error('验证码错误')
        for i in list(data.keys()):
            if not data[i]:
                return rest.params_error('请确认填写信息')
        if len(data['mobile']) != 11:
            return rest.params_error('手机号长度不正确')
        if User.objects(mobile=data['mobile']).count():
            return rest.params_error('手机号已经被注册')
        if not (6 <= len(data['password']) <= 12):
            return rest.params_error('密码长度6-12位')
        c = Customer()
        c.mobile = data.get('mobile', '')
        c.username = data.get('username', '')
        c.sex = data.get('sex', '')
        c.password = data.get('password', 'abc123')
        c.save()
        return rest.success('注册成功!')
    return rt('admin_main/register.html', a=1)


@bp.route('verify/code')
def verify_code():
    # 验证码
    image, string = ValidCodeImg().getValidCodeImg()
    session['images_code'] = string.lower()
    response = make_response(image)
    response.headers["Content-Type"] = "image/png"
    return response


@bp.route('logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(request.args.get('next') or url_for('customer_main.index'))


@bp.route('upload', methods=['GET', 'POST'])
@login_required
def upload():
    base_dir = os.path.join(config.base_dir, 'apps', 'static', 'user_file')
    urls = []
    for i in request.files.getlist('file'):
        filename = random_filename(i.filename)
        i.save(os.path.join(base_dir, filename))
        urls.append(os.path.join(
            '/static', 'user_file',
            filename
        ))
    return {
    "errno": 0,
    "data": urls
}