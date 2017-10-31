# -*- coding: utf-8 -*-
"""
:created on: '12/5/14'

:copyright: NSN
:author: Bartłomiej Idzikowski
:contact: bartlomiej.idzikowski@nsn.com
"""


import logging
from ute_cloud_common_api.common import CloudCommonApi
from ute_cloud_common_api.exception import ApiParametersValidationFailException, ApiActionNotPermittedException
from ute_cloud_dispatcher_api.exception import ApiCloudDispatcherException, ApiMaxTestExecutionCountExceededException


_logger = logging.getLogger(__name__)


class CloudDispatcherApi(CloudCommonApi):

    API_EXCEPTIONS = {
        100: ApiActionNotPermittedException,
        200: ApiParametersValidationFailException,
        300: ApiCloudDispatcherException,
        301: ApiMaxTestExecutionCountExceededException,
    }

    def __request(self, resource, data, method='post'):
        return super(CloudDispatcherApi, self)._request(resource, data, CloudDispatcherApi.API_EXCEPTIONS, method)

    def create_single_run(self, test_path, testline_type, enb_build=None, ute_build=None, sysimage_build=None, test_repository_revision=None,
                          skiprun=None, testline_type_tag=None, enb_build_tag=None, state=None, tags=None, include_tags=None):
        """Create Single Run

        :param string test_path: Test suite path. eg. testsuite/WMP/example_test.robot
        :param string testline_type: Testline type: eg. CLOUD_F
        :param string enb_build: eNB build name. By default latest active.
        :param string ute_build: UTE package build name. By default latest active.
        :param string sysimage_build: Sys. image build name. By default latest active.
        :param string test_repository_revision: Test repository revision. By default HEAD.
        :param boolean skiprun: Skip tests excluded from regression. By default False.
        :param boolean testline_type_tag: Run only selected testline type related tests. By default False.
        :param boolean enb_build_tag: Run only selected eNB build related tests. By default False.
        :param string state: eNB state. By default configured.
        :param list tags: List of tags names. By default empty.
        :param list include_tags: values for -i switch in pybot command.
        :rtype: integer
        :return: Test execution id.
        """
        resource = 'single_run/create'

        request_data = {
            "test_path": test_path,
            "testline_type": testline_type,
            "enb_build": enb_build,
            "ute_build": ute_build,
            "sysimage_build": sysimage_build,
            "test_repository_revision": test_repository_revision,
            "skiprun": skiprun,
            "testline_type_tag": testline_type_tag,
            "enb_build_tag": enb_build_tag,
            "state": state,
            "tags": tags,
            "include_tags": include_tags,
        }

        return self.__request(resource, request_data)

    def get_test_execution_status(self, execution_id):
        """Get Test execution status as text.

        Status list:
          - 'New'
          - 'Dry run pending'
          - 'Dry run started'
          - 'Dry run failure'
          - 'Execution pending'
          - 'Testline pending'
          - 'Testline confirmed'
          - 'Execution started'
          - 'Execution finished'
          - 'Execution failure'
          - 'Execution canceled'

        :param integer execution_id: Execution id.
        :rtype: string
        """
        resource = 'execution/status'

        request_data = {"id": execution_id}

        return self.__request(resource, request_data, method='get')

    def trigger_enb_build_regression(self, enb_build, ute_build=None):
        """Trigger enb build regression.

        :param string enb_build: eNB software build name
        :param string ute_build: UTE package build name. By default latest active.
        :param string test_repository_revision: Test repository revision. By default HEAD.
        """
        resource = 'regression/create'

        request_data = {
            "enb_build": enb_build,
            "ute_build": ute_build,
            "test_repository_revision": "HEAD"
        }

        return self.__request(resource, request_data)

    def notify_reservation_status_change(self, reservation_id, status):
        """Notify reservation status change.

        :param integer reservation_id: Reservation id.
        :param string status: Reservation status.
        """
        resource = 'reservation_status_changed'

        request_data = {
            "reservation_id": reservation_id,
            "status": status,
        }

        return self.__request(resource, request_data)

    def testsuite_blacklist_add(self, test_path, repository='robotlte'):
        """Add test suite to blacklist.

        :param string test_path: Test suite path in repository eg. testsuite/WMP/example.robot
        """
        resource = 'testsuite/blacklist/add'

        request_data = {
            'test_path': test_path,
            'repository': repository,
        }

        return self.__request(resource, request_data)

    def testsuite_blacklist_remove(self, test_path, repository='robotlte'):
        """Remove test suite from blacklist.

        :param string test_path: Test suite path in repository eg. testsuite/WMP/example.robot
        :rtype: string
        :return Test suite path.
        """
        resource = 'testsuite/blacklist/remove'

        request_data = {
            'test_path': test_path,
            'repository': repository,
        }

        return self.__request(resource, request_data)

    def testsuite_blacklist_list(self, offset=0, limit=10, repository='robotlte'):
        """List testsuite blacklist by add_date descending order.

        :param integer offset: Skip first `offset` results. Default: 0.
        :param integer limit: No more than `limit` results will be returned. Default: 10.
        :param string repository: Source `repository` for test path. Possible values: robotlte, Auto5G. Default: robotlte.

        :return:

        .. code-block:: python

            blacklist['test_path']          # testsuite path in repository
            blacklist['reason']             # reason why testsuite was blacklisted
            blacklist['add_date']           # date when testsuite was blacklisted

        """
        resource = 'testsuite/blacklist/list'
        request_data = {
            'offset': offset,
            'limit': limit,
            'repository': repository,
        }

        return self.__request(resource, request_data, method='get')
