# -*- coding: utf-8 -*-
"""
:created on: '27/4/15'

:copyright: NSN
:author: Bartłomiej Idzikowski
:contact: bartlomiej.idzikowski@nokia.com
"""


class CloudApiAuth(object):
    API_URL_TEMPLATE = '%s/api/%s/%s/'

    def __init__(self, api_token, api_address='http://cloud.ute.inside.nsn.com', api_version='v1'):
        self.api_address = api_address
        self.api_token = api_token
        self.api_version = api_version

    def _build_resource_uri(self, resource):
        return CloudApiAuth.API_URL_TEMPLATE % (self.api_address, self.api_version, resource)

    def _build_request_headers(self):
        headers = {
            'Authorization': 'Token %s' % self.api_token,
            'Content-Type': 'application/json'
        }
        return headers
