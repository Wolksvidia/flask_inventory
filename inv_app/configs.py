# -*- coding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.getenv('SECRET','chingatumadre')
    MAIL_SERVER = os.getenv('MAIL_SERVER',None)
    MAIL_PORT = int(os.getenv('MAIL_PORT',25))
    MAIL_USE_SSL = bool(int(os.getenv('MAIL_SSL',0)))
    MAIL_USERNAME = os.getenv('M_USER',None)
    MAIL_PASSWORD = os.getenv('M_SECRET',None)
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')