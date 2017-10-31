# -*- coding: utf-8 -*-
"""
:created on: '12/5/14'

:copyright: NSN
:author: Bartłomiej Idzikowski
:contact: bartlomiej.idzikowski@nokia.com
"""


from ute_cloud_reservation_api.api import CloudReservationApi
from ute_cloud_artifact_api.api import CloudArtifactApi
from ute_cloud_dispatcher_api.api import CloudDispatcherApi


class CloudManagerApi(CloudReservationApi, CloudArtifactApi, CloudDispatcherApi):
    """CloudManagerApi"""
