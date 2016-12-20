# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2016) Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###

from unittest import TestCase

import mock
import io

from hpOneView.connection import connection
from hpOneView.image_streamer.resources.artifact_bundles import ArtifactBundles
from hpOneView.resources.resource import ResourceClient
from tests.test_utils import mock_builtin


class ArtifactBundlesTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._client = ArtifactBundles(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name: ascending'

        self._client.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once_with_default_values(self, mock_get_all):
        self._client.get_all()

        mock_get_all.assert_called_once_with(0, -1, filter='', sort='')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once(self, mock_get):
        self._client.get('78836581-2b6f-4e26-9969-5667fb5837b4')

        mock_get.assert_called_once_with(
            '78836581-2b6f-4e26-9969-5667fb5837b4')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_with_uri_called_once(self, mock_get):
        uri = '/rest/artifact-bundles/78836581-2b6f-4e26-9969-5667fb5837b4'
        self._client.get(uri)

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._client.get_by('name', 'ArtifactBundle')

        mock_get_by.assert_called_once_with(
            'name', 'ArtifactBundle')

    @mock.patch.object(ResourceClient, 'get_by_name')
    def test_get_by_name_called_once(self, mock_get_by):
        self._client.get_by_name('ArtifactBundle')

        mock_get_by.assert_called_once_with('ArtifactBundle')

    @mock.patch.object(ResourceClient, 'create')
    def test_create_called_once(self, mock_create):
        information = {
            "name": "ArtifactBundle"
        }
        mock_create.return_value = {}

        self._client.create(information)
        mock_create.assert_called_once_with(information.copy(), timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_called_once(self, mock_update):
        information = {
            "name": "ArtifactBundleUpdate",
            "uri": "/rest/artifact-bundles/78836581-2b6f-4e26-9969-5667fb5837b4"
        }
        mock_update.return_value = {}

        self._client.update(information)

        default_values = {u'300': {u'type': u'ArtifactsBundle'}}

        mock_update.assert_called_once_with(information.copy(), default_values=default_values, timeout=-1)

    @mock.patch.object(ResourceClient, 'delete')
    def test_remove_called_once(self, mock_delete):
        id = '78836581-2b6f-4e26-9969-5667fb5837b4'
        self._client.delete(id)

        mock_delete.assert_called_once_with(id, timeout=-1)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_all_backups_called_once(self, mock_get):
        uri = '/rest/artifact-bundles/backups'
        self._client.get_all_backups()

        mock_get.assert_called_once_with(id_or_uri=uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_backups_by_id_called_once(self, mock_get):
        uri = '/rest/artifact-bundles/backups'
        id = '78836581-2b6f-4e26-9969-5667fb5837b4'
        self._client.get_backup(id)

        mock_get.assert_called_once_with(id_or_uri=uri + '/' + id)

    @mock.patch.object(connection, 'download_to_stream')
    @mock.patch(mock_builtin('open'))
    def test_download_called_once(self, mock_open, mock_download):
        mock_open.return_value = io.StringIO(u"binary data")

        self._client.download_artifact_bundle('0ABDE00534F', '~/image.zip')
        mock_open.assert_called_once_with('~/image.zip', 'wb')
        mock_download.assert_called_once_with(mock.ANY, mock.ANY)

    @mock.patch.object(connection, 'download_to_stream')
    @mock.patch(mock_builtin('open'))
    def test_download_archive_artifact_bundle_called_once(self, mock_open, mock_download):
        mock_open.return_value = io.StringIO(u"binary data")

        id = '78836581-2b6f-4e26-9969-5667fb5837b4'
        destination = '~/image.zip'

        self._client.download_archive_artifact_bundle(id, destination)
        mock_open.assert_called_once_with(destination, 'wb')
        mock_download.assert_called_once_with(mock.ANY, mock.ANY)

    @mock.patch.object(ResourceClient, 'create')
    def test_create_backup_called_once(self, mock_create):
        information = {
            "deploymentGroupURI": "/rest/deployment-groups/00c1344d-e4dd-43c3-a733-1664e159a36f"
        }
        mock_create.return_value = {}

        self._client.create_backup(information['deploymentGroupURI'])
        uri = '/rest/artifact-bundles/backups'
        mock_create.assert_called_once_with(information.copy(), uri=uri, timeout=-1)

    @mock.patch.object(connection, 'post_multipart')
    def test_upload_artifact_bundle_called_once(self, mock_upload):

        filename = "~/HPE-ImageStreamer-Developer-2016-09-12.zip"
        response = mock.MagicMock(status=200)
        mock_upload.return_value = response, "SUCCESS"

        self._client.upload_bundle_from_file(filename)

        expected_uri = '/rest/artifact-bundles'

        mock_upload.assert_called_once_with(expected_uri, None, filename, 'HPE-ImageStreamer-Developer-2016-09-12.zip')

    @mock.patch.object(connection, 'post_multipart')
    def test_upload_backup_artifact_bundle_called_once(self, mock_upload):
        filename = "~/HPE-ImageStreamer-Developer-2016-09-12.zip"
        response = mock.MagicMock(status=200)
        mock_upload.return_value = response, "SUCCESS"
        deployment_groups = "/rest/deployment-groups/00c1344d-e4dd-43c3-a733-1664e159a36f"

        self._client.upload_backup_bundle_from_file(filename, deployment_groups)

        expected_uri = '/rest/artifact-bundles/backups/archive?deploymentGrpUri=' + deployment_groups

        mock_upload.assert_called_once_with(expected_uri, None, filename, 'HPE-ImageStreamer-Developer-2016-09-12.zip')

    @mock.patch.object(ResourceClient, 'update')
    def test_extract_called_once(self, mock_update):
        mock_update.return_value = {}

        uri = '/rest/artifact-bundles/'
        id = '78836581-2b6f-4e26-9969-5667fb5837b4'

        uri = {'uri': uri + id}
        custom_headers = {'Content-Type': 'text/plain'}

        self._client.extract_bundle(id)

        mock_update.assert_called_once_with(uri, custom_headers=custom_headers, timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_extract_backup_bundle_called_once(self, mock_update):
        mock_update.return_value = {}

        data = {
            'deploymentGroupURI': '/rest/deployment-groups/00c1344d-e4dd-43c3-a733-1664e159a36f'
        }

        uri = '/rest/artifact-bundles/backups/archive'

        self._client.extract_backup_bundle(data['deploymentGroupURI'])

        mock_update.assert_called_once_with(data, uri=uri, timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_stop_creation_called_once(self, mock_update):
        mock_update.return_value = {}

        artifact_uri = "/rest/artifact-bundles/04939e89-bcb0-49fc-814f-1a6bc0a2f63c"
        task_uri = "/rest/tasks/A15F9270-46FC-48DF-94A9-D11EDB52877E"

        self._client.stop_artifact_creation(artifact_uri, task_uri)

        uri = artifact_uri + '/stopArtifactCreate'

        task_uri = {
            'taskUri': task_uri
        }

        mock_update.assert_called_once_with(task_uri, uri=uri)
