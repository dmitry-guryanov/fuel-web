#    Copyright 2016 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import mock

from nailgun import extensions
from nailgun.test.base import BaseTestCase
from nailgun.utils import reverse


class TestExtensionHandler(BaseTestCase):

    def test_get_extensions_list(self):
        class FakeExtension(extensions.BaseExtension):
            @property
            def name(self):
                return self._name

            @property
            def version(self):
                return self._version

            @property
            def description(self):
                return self._description

            def __init__(self, name, version, description, provides):
                self._name = name
                self._version = version
                self._description = description
                self.provides = provides

        exts = [FakeExtension('ex1', '1.0.1', 'descr #1', ['method_call_1']),
                FakeExtension('ex2', '1.2.3', 'descr #2', ['method_call_2'])]

        with mock.patch('nailgun.api.v1.handlers.extension.get_all_extensions',
                        return_value=exts):

            resp = self.app.get(
                reverse('ExtensionHandler'),
                headers=self.default_headers,
            )

        self.assertEqual(resp.status_code, 200)
        expected_body = [
            {'name': 'ex1',
             'version': '1.0.1',
             'description': 'descr #1',
             'provides': ['method_call_1'],
             },
            {'name': 'ex2',
             'version': '1.2.3',
             'description': 'descr #2',
             'provides': ['method_call_2'],
             },
        ]
        self.assertEqual(len(resp.json_body), 2)
        self.assertEqual(expected_body, resp.json_body)
