from config import mongo
from mongoengine import SequenceField
from mongoengine import StringField
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from config import login_manager
__all__ = [
    'Customer',
    'Worker',
]


@login_manager.user_loader
def load_user(user_id):
    # login_manager 登录
    return User.objects(id=user_id).first()


class User(mongo.Document):
    meta = {'allow_inheritance': True, 'collection': 'user'}

    alias_id = SequenceField()
    username = StringField()
    password_hash = StringField()
    mobile = StringField()

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
    pass


class Worker(User):
    pass

