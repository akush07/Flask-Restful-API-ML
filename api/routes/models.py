# -*- coding: utf-8 -*-
"""
Created on at 7/4/2020 8:56 PM 
@author: Abhishek Kushwaha
"""

import os
from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from http import HTTPStatus


class RunModel(Resource):
    @jwt_required
    def post(self):
        json_data = request.get_json()
        images = json_data.get("images")
        return {"message": "recieved images", "images": images}, HTTPStatus.OK
