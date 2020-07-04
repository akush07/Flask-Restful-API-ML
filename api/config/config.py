# -*- coding: utf-8 -*-
"""
Created on at 7/2/2020 11:53 PM 
@author: Abhishek Kushwaha
"""

import os

basedir = os.path.abspath(os.getcwd())


class Config:
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ERROR_MESSAGE_KEY = 'message'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    UPLOADED_IMAGES_DEST = 'static/images'
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 10 * 60
    RATELIMIT_HEADERS_ENABLED = True


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'super-secret-key'
    POSTGRES = {
        'user': 'postgres',
        'pw': 'admin',
        'db': 'smilecook',
        'host': 'localhost',
        'port': '5432',
    }
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES


class StagingConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class ProductionConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')