# -*- coding:utf8 -*-
import os

class Config(object):
    DEBUG = True
    SECRET_KEY = "JWKY"
    base_dir = os.path.dirname(os.path.dirname(__file__))

    # mongoDB
    MONGODB_DB = 'home_decoration'
    MONGODB_HOST = 'mongo'
    MONGODB_PORT = 27017

    # redis
    REDIS_HOST = 'redis'
    REDIS_SOCKETIO = 'redis://{0}:6379/{1}'.format(REDIS_HOST, 0)
