# -*- coding: utf-8 -*-
"""
:created on: 28/04/15

:copyright: Nokia
:author: Bartłomiej Idzikowski
:contact: bartlomiej.idzikowski@nokia.com
"""

from ute_cloud_common_api.exception import ApiException


class ApiCloudDispatcherException(ApiException):
    """Base ApiCloudDispatcherException."""


class ApiMaxTestExecutionCountExceededException(ApiCloudDispatcherException):
    """ApiMaxTestExecutionCountExceededException"""
