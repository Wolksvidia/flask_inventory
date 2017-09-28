# -*- coding: utf-8 -*-


class Config(object):
    SECRET_KEY = 'estasdelachingadamano'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'mi_cuenta_@gmail.com'
    MAIL_PASSWORD = 'Password'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
