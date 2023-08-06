# copyright 2022 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact https://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""cubicweb-api automatic tests


uncomment code below if you want to activate automatic test for your cube:

.. sourcecode:: python

    from cubicweb.devtools.testlib import AutomaticWebTest

    class AutomaticWebTest(AutomaticWebTest):
        '''provides `to_test_etypes` and/or `list_startup_views` implementation
        to limit test scope
        '''

        def to_test_etypes(self):
            '''only test views for entities of the returned types'''
            return set(('My', 'Cube', 'Entity', 'Types'))

        def list_startup_views(self):
            '''only test startup views of the returned identifiers'''
            return ('some', 'startup', 'views')
"""
import json

from cubicweb.pyramid.test import PyramidCWTest
from cubicweb.schema_exporters import JSONSchemaExporter

from cubicweb_api.constants import API_PATH_DEFAULT_PREFIX


# Don't use cubicweb.devtools.BASE_URL because pyramid routes in CubicWeb < 4.x
# are mounted on the domain root instead of /cubicweb
BASE_URL = "https://testing.cubicweb/"


class ApiTC(PyramidCWTest):
    settings = {"cubicweb.includes": ["cubicweb.pyramid.auth"]}

    @classmethod
    def init_config(cls, config):
        super().init_config(config)
        config.global_set_option("base-url", BASE_URL)

    def test_get_schema(self):
        schema = self.webapp.get(
            f"{BASE_URL[:-1]}{API_PATH_DEFAULT_PREFIX}/v1/schema"
        ).json
        exporter = JSONSchemaExporter()
        exported_schema = exporter.export_as_dict(self.repo.schema)

        assert exported_schema == schema

    def test_rql_route(self):
        response = self.webapp.post(
            f"{BASE_URL[:-1]}{API_PATH_DEFAULT_PREFIX}/v1/rql",
            params=json.dumps(
                {
                    "query": "Any X Where X is CWUser, X login %(login)s",
                    "params": {"login": "anon"},
                }
            ),
            content_type="application/json",
        )
        with self.admin_access.repo_cnx() as cnx:
            rset_as_list = list(
                cnx.execute(
                    "Any X Where X is CWUser, X login %(login)s", {"login": "anon"}
                )
            )

        assert rset_as_list == response.json

    def test_sending_bad_rql_query_returns_400(self):
        response = self.webapp.post(
            f"{BASE_URL[:-1]}{API_PATH_DEFAULT_PREFIX}/v1/rql",
            params=json.dumps(
                {
                    "query": "SET X color 'red' Where X is CWUser",
                }
            ),
            content_type="application/json",
            status=400,
        ).json

        assert response == {
            "message": 'SET X color "red" WHERE X is CWUser\n** unknown relation `color`',
            "data": None,
            "title": "BadRQLQuery",
        }

    def test_401_error_on_rql_when_not_authenticated(self):
        response = self.webapp.post(
            f"{BASE_URL[:-1]}{API_PATH_DEFAULT_PREFIX}/v1/rql",
            params=json.dumps(
                {
                    "query": "SET X login 'MYLOGIN' Where X is CWUser",
                }
            ),
            content_type="application/json",
            status=401,
        ).json

        assert response == {
            "message": "You are not allowed to perform update operation on CWUser",
            "data": None,
            "title": "Unauthorized",
        }

    def test_successful_login_returns_204(self):
        self.webapp.post(
            f"{BASE_URL[:-1]}{API_PATH_DEFAULT_PREFIX}/v1/login",
            params=json.dumps({"login": self.admlogin, "password": self.admpassword}),
            content_type="application/json",
            status=204,
        )

    def test_wrong_login_returns_401(self):
        self.webapp.post(
            f"{BASE_URL[:-1]}{API_PATH_DEFAULT_PREFIX}/v1/login",
            params=json.dumps({"login": self.admlogin, "password": "INVALID PASSWORD"}),
            content_type="application/json",
            status=401,
        )

    def test_logged_user_can_insert_data(self):
        self.webapp.post(
            f"{BASE_URL[:-1]}{API_PATH_DEFAULT_PREFIX}/v1/login",
            params=json.dumps({"login": self.admlogin, "password": self.admpassword}),
            content_type="application/json",
            status=204,
        )
        group_eid = self.webapp.post(
            f"{BASE_URL[:-1]}{API_PATH_DEFAULT_PREFIX}/v1/rql",
            params=json.dumps(
                {
                    "query": "INSERT CWGroup G: G name 'test-group'",
                }
            ),
            content_type="application/json",
            status=200,
        ).json[0][0]
        with self.admin_access.repo_cnx() as cnx:
            assert cnx.entity_from_eid(group_eid).name == "test-group"

    def test_current_user_returns_user_as_json(self):
        self.webapp.post(
            f"{BASE_URL[:-1]}{API_PATH_DEFAULT_PREFIX}/v1/login",
            params=json.dumps({"login": self.admlogin, "password": self.admpassword}),
            content_type="application/json",
            status=204,
        )
        response = self.webapp.get(
            f"{BASE_URL[:-1]}{API_PATH_DEFAULT_PREFIX}/v1/current-user", status=200
        ).json

        assert response["login"] == self.admlogin
        assert response["dcTitle"] == self.admlogin
        assert type(response["eid"]) == int


if __name__ == "__main__":
    from unittest import main

    main()
