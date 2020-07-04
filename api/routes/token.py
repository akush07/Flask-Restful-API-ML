# -*- coding: utf-8 -*-
"""
Created on at 7/4/2020 12:16 PM 
@author: Abhishek Kushwaha
"""


from http import HTTPStatus
from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    jwt_refresh_token_required,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)
from api.utils.utility import check_password
from api.models.user import User

black_list = set()


class TokenResource(Resource):
    """
    This class returns token for valid user upon login or request
    """
    def post(self):
        json_data = request.get_json()
        email = json_data.get('email')
        password = json_data.get('password')
        user = User.get_by_email(email=email)

        if not user or not check_password(password, user.password):
            return {'message': 'username or password is incorrect'}, HTTPStatus.UNAUTHORIZED

        if user.is_active is False:
            return {'message': 'The user account is not activated yet'}, HTTPStatus.FORBIDDEN

        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(identity=user.id)
        return {'access_token': access_token, 'refresh_token': refresh_token}, HTTPStatus.OK


class RefreshResource(Resource):
    """
    This class generates new token and return when refresh token is provided.
    """
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        token = create_access_token(identity=current_user, fresh=False)
        return {'token': token}, HTTPStatus.OK


class RevokeResource(Resource):
    """
    This class revoke token access and add blacklist's user
    """
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        black_list.add(jti)
        return {'message': 'Successfully logged out'}, HTTPStatus.OK
