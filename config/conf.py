# -*- coding:utf8 -*-
import os


class Config(object):
    DEBUG = True
    SECRET_KEY = "home_decoration"
    base_dir = os.path.dirname(os.path.dirname(__file__))

    # mongoDB
    MONGODB_DB = 'home_decoration'
    MONGODB_HOST = '127.0.0.1'
    MONGODB_PORT = 27017

    BOOTSTRAP_SERVE_LOCAL = True
