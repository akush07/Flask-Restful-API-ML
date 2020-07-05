# -*- coding: utf-8 -*-
"""
Created on at 7/4/2020 10:55 AM 
@author: Abhishek Kushwaha
"""


import requests


class MailgunApi:

    API_URL = 'https://api.mailgun.net/v3/{}/messages'

    def __init__(self, domain, api_key):
        self.domain = domain
        self.key = api_key
        self.base_url = self.API_URL.format(self.domain)

    def send_email(self, to, subject, text, html=None):
        if not isinstance(to, (list, tuple)):
            to = [to, ]

        data = {
            'from': 'APIService <no-reply@{}>'.format(self.domain),
            'to': to,
            'subject': subject,
            'text': text,
            'html': html
        }
        response = requests.post(url=self.base_url,
                                 auth=('api', self.key),
                                 data=data)
        return response

