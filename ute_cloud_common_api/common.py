# -*- coding: utf-8 -*-
"""
:created on: '27/4/15'

:copyright: NSN
:author: Bartłomiej Idzikowski
:contact: bartlomiej.idzikowski@nokia.com
"""

import json
import requests
from simplejson.scanner import JSONDecodeError
from requests.exceptions import ConnectionError
from .exception import ApiUnknownException, ApiDataDecodeException, ApiConnectionException, ApiUnauthorizedException, ApiForbiddenException


class CloudCommonApi(object):
    API_EXCEPTIONS = {}
    API_URL_TEMPLATE = '%s/api/%s/%s/'

    def __init__(self, api_token, api_address='https://cloud.ute.inside.nsn.com', api_version='v1'):
        self.api_address = api_address
        self.api_token = api_token
        self.api_version = api_version

    def _build_resource_uri(self, resource):
        return CloudCommonApi.API_URL_TEMPLATE % (self.api_address, self.api_version, resource)

    def _build_request_headers(self, content_type='application/json'):
        headers = {
            'Authorization': 'Token %s' % self.api_token,
            'Content-Type': content_type
        }
        return headers

    def _decode_json_data(self, data):
        try:

            if data.status_code == 401:
                raise ApiUnauthorizedException(data.text)

            if data.status_code == 403:
                raise ApiForbiddenException(data.text)

            result = json.loads(data.json())
            error_code, error_message = None, None

            if 'result' in result:
                result = result['result']
            else:
                error_code = result['error']['code']
                error_message = result['error']['message']
                result = None

            return result, error_code, error_message
        except (KeyError, TypeError, JSONDecodeError) as e:
            raise ApiDataDecodeException(str(e))

    def _request(self, resource, data, exception_map, method='post', content_type='application/json'):
        try:
            request_func = requests.post if method == 'post' else requests.get
            json_data = request_func(
                self._build_resource_uri(resource),
                data=json.dumps(self._filter_none_values(data)) if content_type == 'application/json' else data,
                headers=self._build_request_headers(content_type)
            )
        except ConnectionError as e:
            raise ApiConnectionException(str(e))

        result, error_code, error_message = self._decode_json_data(json_data)
        if result is not None:
            return result
        else:
            exception_class = exception_map.get(error_code, ApiUnknownException)
            raise exception_class(error_message)

    def _filter_none_values(self, data):
        return {key: value for key, value in data.items() if value is not None}
