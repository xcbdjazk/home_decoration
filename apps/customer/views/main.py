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
from models.message import *
from mongoengine.queryset import Q
from bson import ObjectId

bp = Blueprint("customer_main", __name__, url_prefix='/customer')


@bp.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1)
    query = dict(status=0)
    if current_user.is_authenticated:
        query['user__ne'] = current_user.id
    k = request.args.get('k', '')
    work_type = request.args.get('worktype', '')
    if work_type:
        query['work_type'] = work_type
    if k:
        pagination = CustomerTask.objects(Q(title__icontains=k) | Q(desc__icontains=k),**query).paginate(page, per_page=20)
    else:
        pagination = CustomerTask.objects(**query).order_by('-id').paginate(page, per_page=10)

    wts = WorkerType.objects.all()

    content = dict(
        pagination=pagination,
        wts=wts,
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
    status = request.args.get('status', 0, type=int)
    s = request.args.get('s', '')
    q = {}
    if status:
        q["status"] = status
    if s:

        pagination = CustomerTask.objects(Q(title__icontains=s) | Q(desc__icontains=s), user=current_user.id,
                                          **q).paginate(page, per_page=20)
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
    return rt('customer_main/task_add.html', **content)


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


@bp.route('/task/success/<tid>', methods=['GET', 'POST'])
def task_success(tid):
    c = CustomerTask.objects(user=current_user.id, id=tid).first()
    if c:
        c.success()
    return rest.success('操作成功')


@bp.route('/task/jieyue/<tid>', methods=['GET', 'POST'])
def task_jieyue(tid):
    c = CustomerTask.objects(user=current_user.id, id=tid).first()
    if c:
        c.jieyue(request.form.get('text'))
    return rest.success('操作成功')


@bp.route('/delete/task/<tid>', methods=['GET', 'POST'])
def task_delete(tid):
    c = CustomerTask.objects(user=current_user.id, id=tid).first()
    if c:
        c.delete()
    return redirect(request.referrer)


@bp.route('/message/list', methods=['GET', 'POST'])
def message_list():
    users = Customer.objects(id__ne=current_user.id).all()
    content = dict(
        users=users
    )
    return rt('customer_main/message_list.html', **content)


@bp.route('/message/count', methods=['GET', 'POST'])
def message_count():
    if not current_user.is_authenticated:
        return rest.success()
    count = ChatMessage.objects(take_user=current_user.id, is_read=False).count()
    content = dict(
        count=count
    )
    return rest.success(data=content)


@bp.route('/message/<uid>', methods=['GET', 'POST'])
def message(uid):
    u = Customer.objects(id=uid).first()
    if request.method == 'POST':
        data = request.form
        msg = data.get('message', '')
        date = data.get('date', '')
        cm = ChatMessage()
        cm.send_user = current_user.id
        cm.take_user = u.id
        cm.content = msg
        cm.date = date
        cm.save()
        return {}

    messages = ChatMessage.objects(send_user=u.id, take_user=current_user.id, is_read=False).order_by('id').all()
    messages.update(is_read=True)
    messages = ChatMessage.objects(Q(send_user=u.id, take_user=current_user.id) |
                                   Q(take_user=u.id, send_user=current_user.id)).order_by('id').all()
    content = dict(
        u=u,
        messages=messages
    )

    return rt('customer_main/message.html', **content)


@bp.route('/message/get/<uid>', methods=['GET', 'POST'])
def message_get(uid):
    u = Customer.objects(id=uid).first()
    messages = ChatMessage.objects(send_user=u.id, take_user=current_user.id, is_read=False).order_by('id').all()
    data = []

    for msg in messages:
        msg: ChatMessage
        data.append({
            "msg": msg.content,
            'date': msg.date
        })
    messages.update(is_read=True)
    print(data)

    return rest.success(data={
        "messages": data
    })

@bp.route('/rate/<tid>', methods=['GET', 'POST'])
def rate(tid):
    if request.method == 'POST':
        data = request.form
        c: CustomerTask = CustomerTask.objects(user=current_user.id, id=tid).first()
        c.is_rate = True
        c.jishu_score = float(data.get('jishu_score')[0])
        c.time_score = float(data.get('time_score')[0])
        c.attitude_score = float(data.get('attitude_score')[0])
        c.rate_desc = data.get('rate_desc')
        c.save()
        c.join_user.worker.ref_score(c.jishu_score, c.time_score, c.attitude_score)
    return rest.success('评价成功')