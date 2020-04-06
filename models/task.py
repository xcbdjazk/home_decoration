from config import mongo
from mongoengine import SequenceField
from mongoengine import StringField
from mongoengine import BooleanField
from mongoengine import IntField
from mongoengine import FloatField
from mongoengine import ListField
from mongoengine import DateTimeField
from mongoengine import DENY
from mongoengine import ReferenceField
from .users import *

import datetime

__all__ = [
    'CustomerTask'
]


class Task(mongo.Document):
    meta = {'allow_inheritance': True, 'collection': 'task'}
    create_time = DateTimeField(default=datetime.datetime.now)
    alias_id = SequenceField()


class CustomerTask(Task):
    user = ReferenceField(User, reverse_delete_rule=DENY)
    # 标题
    title = StringField()
    # 图集
    images = ListField(StringField())
    # 介绍
    desc = StringField()
    # 备注
    remarks = StringField()
    # 状态
    # 0 = 发布中
    # 1 = 进行中
    # 2 = 已完成
    # -1 = 已取消 (违规)
    status = IntField(choices=(0, 1, 2, -1), default=0)
    join_user = ReferenceField(User, reverse_delete_rule=DENY)
    # 价格
    price = FloatField()
    # 工期
    work_time = FloatField()
    # 工种
    work_type = ListField(ReferenceField(WorkerType, reverse_delete_rule=DENY))

    @property
    def work_type_name(self):
        return ",".join([i.name for i in self.work_type])

    @property
    def status_name(self):
        # 0 = 发布中
        # 1 = 进行中
        # 2 = 已完成
        # -1 = 已取消 (违规)
        d = {"0": '发布中',
             "1": "进行中",
             "2": "已完成",
             "-1": "已取消(违规)",
             }

        return d.get(str(self.status))
