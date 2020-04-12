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
from models.task import *
bp = Blueprint("worker_main", __name__, url_prefix='/worker')


@bp.route('/', methods=['GET', 'POST'])
def index():
    status = request.args.get("status", type=int)
    page = request.args.get("page", 1, type=1)
    query = {
        'join_user':current_user.id,
    }
    if status:
        query["status"]= status
    else:
        query["status"] = 3

    pagination = CustomerTask.objects(**query).paginate(page, per_page=20)
    jieyue = CustomerTask.objects(join_user=current_user.id, status=-2).count()
    doing = CustomerTask.objects(join_user=current_user.id, status=1).count()
    succ = CustomerTask.objects(join_user=current_user.id, status=2).count()
    content = {
        "pagination":pagination,
        "jieyue":jieyue,
        "doing":doing,
        "succ":succ,
    }
    return rt('worker_main/index.html', **content)


@bp.route('/task/<tid>/jieyue', methods=['GET', 'POST'])
def task_jieyue(tid):
    c:CustomerTask = CustomerTask.objects(id=tid).first()
    c.confirm_jieyue()
    return rest.success('操作成功')



@bp.route('/task/<tid>/join', methods=['GET', 'POST'])
def task_join(tid):
    c:CustomerTask = CustomerTask.objects(id=tid).first()
    if c.join_user:
        return rest.params_error('任务已经被接受，请选择其他任务！')
    c.join_user = current_user.id
    c.doing()
    return rest.success('操作成功,请前往工单管理查看',data={"url":url_for('admin.index')})