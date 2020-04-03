from config import mongo
from mongoengine import SequenceField
from mongoengine import StringField
from mongoengine import BooleanField
from mongoengine import IntField
from mongoengine import FloatField
from mongoengine import ListField
from mongoengine import DENY
from mongoengine import ReferenceField
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from config import login_manager
from flask_login import UserMixin
__all__ = [
    'Customer',
    'Worker',
    'User',
    'WorkerType',
]


@login_manager.user_loader
def load_user(user_id):
    # login_manager 登录
    return User.objects(id=user_id).first()



class User(mongo.Document, UserMixin):
    meta = {'allow_inheritance': True, 'collection': 'user'}

    alias_id = SequenceField()
    username = StringField()
    password_hash = StringField()
    sex = StringField()
    mobile = StringField()
    is_admin = BooleanField(default=False)

    @property
    def password(self):
        raise ValueError("密码不可读取")

    @password.setter
    def password(self, pwd):
        # 默认生成哈希密码
        self.password_hash = generate_password_hash(pwd)

    def verify_password(self, password):
        # 校验密码

        return check_password_hash(self.password_hash, password)


class Customer(User):

    @property
    def is_worker(self):
        return bool(Worker.objects(user=self).count())


class WorkerType(mongo.Document):
    meta = {'collection': 'worker_type'}

    name = StringField()


class Worker(mongo.Document):
    meta = {'allow_inheritance': True, 'collection': 'worker'}
    user = ReferenceField(User, reverse_delete_rule=DENY)
    # 服务次数
    service_count = FloatField(default=0)
    # 技术得分
    jishu_score = FloatField(default=0)
    # 用时得分
    time_score = FloatField(default=0)
    # 态度得分
    attitude_score = FloatField(default=0)
    # 平均分
    avg_score = FloatField(default=0)
    # 工种
    work_type = ListField(ReferenceField(WorkerType, reverse_delete_rule=DENY))
    # 自我介绍
    desc = StringField()
    # 0 = 审核中
    # 1 = 正常
    # -1 = 违规
    status = IntField(default=0)

    def save_self(self):
        pass

    @staticmethod
    def format_float(f: float):
        return float("%.1f" % f)

    def ref_score(self, jishu_score, time_score, attitude_score):
        all_jishu_score = self.jishu_score * self.service_count + jishu_score
        self.jishu_score = self.format_float(all_jishu_score / (self.service_count + 1))
        all_time_score = self.time_score * self.service_count + time_score
        self.time_score = self.format_float(all_time_score / (self.service_count + 1))
        all_attitude_score = self.attitude_score * self.service_count + attitude_score
        self.attitude_score = self.format_float(all_attitude_score / (self.service_count + 1))
        self.service_count += 1
        self.avg_score = self.format_float(
            (self.jishu_score + self.time_score + self.attitude_score) / 3 / self.service_count)
        self.save()


class Admin(User):
    is_admin = BooleanField(default=True)
