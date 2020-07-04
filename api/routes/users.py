# -*- coding: utf-8 -*-
"""
Created on at 7/4/2020 10:46 AM
@author: Abhishek Kushwaha
"""

import os
from flask import request, url_for, render_template
from flask_restful import Resource
from flask_jwt_extended import jwt_optional, get_jwt_identity, jwt_required
from http import HTTPStatus
from api.utils.mailgun import MailgunApi
from api.models.user import User
from api.schemas.user import UserSchema
from api.utils.utility import generate_token, verify_token

user_schema = UserSchema()
user_public_schema = UserSchema(exclude=('email',))

mailgun = MailgunApi(domain=os.environ.get('MAILGUN_DOMAIN'),
                     api_key=os.environ.get('MAILGUN_API_KEY'))


class Registration(Resource):
    """
    This class will Register the users

    """
    def post(self):
        json_data = request.get_json()
        data, errors = user_schema.load(data=json_data)

        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        if User.get_by_username(data.get('username')):
            return {'message': 'username already used'}, HTTPStatus.BAD_REQUEST

        if User.get_by_email(data.get('email')):
            return {'message': 'email already used'}, HTTPStatus.BAD_REQUEST

        user = User(**data)
        user.save()
        token = generate_token(user.email, salt='activate')
        subject = 'Please confirm your registration.'
        link = url_for('useractivate',
                       token=token,
                       _external=True)
        text = 'Hi, Thanks for choosing our service! Please confirm your registration by clicking on the link: {}'.format(
            link)
        mailgun.send_email(to=user.email,
                           subject=subject,
                           text=text,
                           html=render_template('email/confirmation.html', link=link))
        return user_schema.dump(user).data, HTTPStatus.CREATED


class UserResource(Resource):
    @jwt_optional
    def get(self, username):
        user = User.get_by_username(username=username)
        if user is None:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND
        current_user = get_jwt_identity()

        if current_user == user.id:
            data = user_schema.dump(user).data
        else:
            data = user_public_schema.dump(user).data

        return data, HTTPStatus.OK


class MeResource(Resource):
    """
    Returns user details while validating with token
    """
    @jwt_required
    def get(self):
        user = User.get_by_id(idx=get_jwt_identity())
        return user_schema.dump(user).data, HTTPStatus.OK


class UserActivate(Resource):
    """
    This class activate users with token
    """
    def get(self, token):
        email = verify_token(token, salt='activate')
        if email is False:
            return {'message': 'Invalid token or token expired'}, HTTPStatus.BAD_REQUEST

        user = User.get_by_email(email=email)

        if not user:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

        if user.is_active is True:
            return {'message': 'The user account is already activated'}, HTTPStatus.BAD_REQUEST

        user.is_active = True
        user.save()
        return {}, HTTPStatus.NO_CONTENT


