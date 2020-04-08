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
from utils import rest
from models.users import *
from models.task import *
from mongoengine.queryset import Q
from bson import ObjectId

bp = Blueprint("customer_main", __name__, url_prefix='/customer')


@bp.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1)
    pagination = CustomerTask.objects(status=0).order_by('-id').paginate(page, per_page=10)
    content = dict(
        pagination=pagination
    )
    return rt('customer_main/index.html', **content)


@bp.route('/index/task/<tid>', methods=['GET', 'POST'])
def index_task_detail(tid):
    c = CustomerTask.objects(id=tid).first()
    content = dict(
        c=c
    )

    return rt('customer_main/index_task_detail.html', **content)


@bp.route('/task/detail', methods=['GET', 'POST'])
def task_detail():
    page = request.args.get('page', 1)
    status = request.args.get('status',0,type=int)
    s = request.args.get('s', '')
    q = {}
    if status:
        q["status"] = status
    if s:

        pagination = CustomerTask.objects(Q(title__icontains=s) | Q(desc__icontains=s),user=current_user.id,  **q).paginate(page, per_page=20)
    else:
        pagination = CustomerTask.objects(user=current_user.id, **q).paginate(page, per_page=20)
    content = dict(
        pagination=pagination
    )
    return rt('customer_main/task_detail.html', **content)


@bp.route('/add/task', methods=['GET', 'POST'])
def task_add():
    if request.method == 'POST':
        data = request.form
        c = CustomerTask()
        c.title = data['title']
        c.work_type = [ObjectId(i) for i in data.getlist('work_type[]')]
        c.work_time = float(data['work_time'])
        c.price = float(data['price'])
        c.desc = data['desc']
        c.images = data.getlist('images[]')
        c.user = current_user.id
        c.save()
        return rest.success(data={"url": url_for(".task_detail")})
    wts = WorkerType.objects.all()
    content = {"wts": wts}
    return rt('customer_main/task_add.html',**content)


@bp.route('/edit/task/<tid>', methods=['GET', 'POST'])
def task_update(tid):
    c = CustomerTask.objects(user=current_user.id, id=tid).first()
    if request.method == 'POST':
        data = request.form
        c.title = data['title']
        c.work_type = [ObjectId(i) for i in data.getlist('work_type[]')]
        c.work_time = float(data['work_time'])
        c.price = float(data['price'])
        c.desc = data['desc']
        c.images = data.getlist('images[]')
        c.user = current_user.id
        c.save()
        return rest.success(data={"url": url_for(".task_detail")})

    wts = WorkerType.objects.all()
    content = {"wts": wts, "c": c}
    return rt('customer_main/task_update.html', **content)


@bp.route('/delete/task/<tid>', methods=['GET', 'POST'])
def task_delete(tid):
    c = CustomerTask.objects(user=current_user.id, id=tid).first()
    if c:
        c.delete()
    return redirect(request.referrer)