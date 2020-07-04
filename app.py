# -*- coding: utf-8 -*-
"""
Created on at 7/4/2020 12:13 PM 
@author: Abhishek Kushwaha
"""

import os
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from api.config import config
from api.utils.extensions import db, jwt, cache, limiter
from api.routes.users import Registration, UserResource, MeResource, UserActivate
from api.routes.token import TokenResource, RefreshResource, RevokeResource, black_list
from api.routes.models import RunModel

def create_app():
    env = os.environ.get('ENV', 'Development')

    if env == 'Production':
        config_str = config.ProductionConfig
    elif env == 'Staging':
        config_str = config.StagingConfig
    else:
        config_str = config.DevelopmentConfig

    app = Flask(__name__)
    app.config.from_object(config_str)
    register_extensions(app)
    register_resources(app)
    return app


def register_extensions(app):
    db.init_app(app)
    Migrate(app, db)
    jwt.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return jti in black_list


def register_resources(app):
    api = Api(app)
    api.add_resource(Registration, '/users')
    api.add_resource(UserActivate, '/users/activate/<string:token>')
    api.add_resource(UserResource, '/users/<string:username>')
    api.add_resource(MeResource, '/me')
    api.add_resource(TokenResource, '/token')
    api.add_resource(RefreshResource, '/refresh')
    api.add_resource(RevokeResource, '/revoke')
    api.add_resource(RunModel, '/classify')

if __name__ == '__main__':
    app = create_app()
    app.run()
