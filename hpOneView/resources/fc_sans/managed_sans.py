# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2016) Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library

standard_library.install_aliases()

__title__ = 'Managed SANs'
__version__ = '0.0.1'
__copyright__ = '(C) Copyright (2012-2016) Hewlett Packard Enterprise Development LP'
__license__ = 'MIT'
__status__ = 'Development'

from hpOneView.resources.resource import ResourceClient


class ManagedSANs(object):
    URI = '/rest/fc-sans/managed-sans'

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def get_all(self, start=0, count=-1, query='', sort=''):
        """
        Retrieves the list of registered Managed SANs

        Args:
            start:
                The first item to return, using 0-based indexing.
                If not specified, the default is 0 - start with the first available item.
            count:
                The number of resources to return. A count of -1 requests all the items. The actual number of items in
                the response may differ from the requested count if the sum of start and count exceed the total number
                of items, or if returning the requested number of items would take too long
            query:
                A general query string to narrow the list of resources returned.
                The default is no query - all resources are returned.
            sort:
                The sort order of the returned data set. By default, the sort order is based
                on create time, with the oldest entry first.

        Returns:
            list: A list of Managed SANs

        """
        return self._client.get_all(start=start, count=count, query=query, sort=sort)

    def get_by_name(self, name):
        """
        Gets a Managed SAN by name.

        Args:
            name: Name of the Managed SAN

        Returns:
            dict: Managed SAN.
        """
        managed_sans = self._client.get_all()
        result = [x for x in managed_sans if x['name'] == name]
        return result[0] if result else None

    def get(self, id_or_uri):
        """
        Retrieves a single Managed SAN by id or uri

        Args:
            id_or_uri: Could be either the Managed SAN resource id or uri.

        Returns:
            dict: The Managed SAN resource.
        """
        return self._client.get(id_or_uri=id_or_uri)

    def update(self, id_or_uri, data, timeout=-1):
        """
        Updates a Managed SAN.

        It's possible:
        - Refresh the Managed SAN.
        - Updating the Managed SAN's publicAttributes.
        - Updating the Managed SAN's policy.

        Args:
            id_or_uri: Could be either the Managed SAN resource id or uri.
            data: dict object to update
            timeout:
                Timeout in seconds. Wait task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns:
            dict: SanResponse

        """
        uri = self._client.build_uri(id_or_uri)
        return self._client.update(data, uri=uri, timeout=timeout)
