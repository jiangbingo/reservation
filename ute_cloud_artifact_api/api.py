# -*- coding: utf-8 -*-
"""
:created on: 03/03/2015

:copyright: NSN
:author: Damian Pukacz
:contact: damian.pukacz@nsn.com
"""
import logging
import os
from requests_toolbelt import MultipartEncoder
from ute_cloud_common_api.common import CloudCommonApi
from ute_cloud_common_api.exception import ApiParametersValidationFailException, ApiActionNotPermittedException
from ute_cloud_artifact_api.exception import ApiCloudArtifactException


_logger = logging.getLogger(__name__)


class CloudArtifactApi(CloudCommonApi):
    API_EXCEPTIONS = {
        100: ApiActionNotPermittedException,
        200: ApiParametersValidationFailException,
        300: ApiCloudArtifactException,
    }

    def __request(self, resource, data, method='post', content_type='application/json'):
        return self._request(resource, data, CloudArtifactApi.API_EXCEPTIONS, method, content_type)

    def add_enb_build(self, name, tag='base', status=1):
        """Create new enb build
        :param string name: eNB build name.
        :param string tag: eNB build tag.
        :param integer status: Status.
        """
        resource = 'enb_build_add'

        request_data = {
            "name": name,
            "tag": tag,
            "status": status
        }

        return self.__request(resource, request_data)

    def upload_enb_build(self, tag, files):
        """Upload and add new enb build knife
        :param string tag: build tag
        :param list files: paths to build files (build, btssm, swconfig etc.)
        """
        resource = 'enb_build_upload'
        fields = {'file_{}'.format(num): (os.path.basename(path), open(path, 'rb')) for num, path in enumerate(files)}
        fields['tag'] = tag
        request_data = MultipartEncoder(fields=self._filter_none_values(fields))
        return self.__request(resource, request_data, content_type=request_data.content_type)

    def add_sysimage_build(self, name, active=True):
        """Create new enb build
        :param string name: Sysimage build name
        :param boolean active: Tells if build is active
        """
        resource = 'sysimage_build_add'

        request_data = {
            "name": name,
            "active": active
        }

        return self.__request(resource, request_data)

    def add_ute_build(self, name, active=True):
        """Create new enb build
        :param string name: UTE build name
        :param boolean active: Tells if build is active
        """
        resource = 'ute_build/add'

        request_data = {
            "name": name,
            "active": active
        }

        return self.__request(resource, request_data)

    def deactivate_ute_build(self, name):
        """Deactivate existing ute build.

        :param string name: UTE build name
        """
        resource = 'ute_build/deactivate'

        request_data = {
            "name": name,
        }

        return self.__request(resource, request_data)

    def activate_ute_build(self, name):
        """Activate existing ute build.

        :param string name: UTE build name
        """
        resource = 'ute_build/activate'

        request_data = {
            "name": name,
        }

        return self.__request(resource, request_data)

    def enb_build_blacklist_add(self, name, tag, tags):
        """"Add eNB build to blacklist.

        :param string name: eNB build name.
        :param string tag: eNB build tag.
        :param list tags: List of tags names that build we be blacklisted with.
        """
        resource = 'enb_build_blacklist_add'
        request_data = {
            "name": name,
            "tag": tag,
            "tags": tags,
        }
        return self.__request(resource, request_data)

    def enb_build_blacklist_remove(self, name, tag, tags):
        """"Remove eNB build to blacklist.

        :param string name: eNB build name.
        :param string tag: eNB build tag.
        :param list tags: List of tags names that build should not be blacklisted with.
        """
        resource = 'enb_build_blacklist_remove'
        request_data = {
            "name": name,
            "tag": tag,
            "tags": tags,
        }
        return self.__request(resource, request_data)
