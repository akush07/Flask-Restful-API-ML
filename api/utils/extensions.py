# -*- coding: utf-8 -*-
"""
Created on at 7/2/2020 11:51 PM 
@author: Abhishek Kushwaha
"""


from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


db = SQLAlchemy()
jwt = JWTManager()
cache = Cache()
limiter = Limiter(key_func=get_remote_address)
