from config import mongo
from mongoengine import SequenceField
from mongoengine import StringField
from mongoengine import BooleanField
from mongoengine import IntField
from mongoengine import FloatField
from mongoengine import DateTimeField
from mongoengine import ObjectIdField
from mongoengine import ListField
from mongoengine import DENY
from mongoengine import ReferenceField
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
__all__ = [

]



class Message(mongo.Document):
    meta = {'allow_inheritance': True, 'collection': 'message'}

    # 发送者
    send_user = ObjectIdField(required=True)
    # 接收者
    take_user = ObjectIdField(required=True)
    # 创建时间
    create_time = DateTimeField()
    # 内容
    content = StringField()


class ChatMessage(Message):
    is_read = BooleanField(default=False)


    def read(self):
        self.is_read = True
        self.save()

    @staticmethod
    def read_all(sid, tid):
        return