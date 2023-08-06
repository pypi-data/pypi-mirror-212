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
import logging
from enum import Enum

from cubicweb import AuthenticationError
from cubicweb.schema_exporters import JSONSchemaExporter
from pyramid.config import Configurator
from pyramid.request import Request
from pyramid.response import Response
from pyramid.security import remember
from pyramid.view import view_config, view_defaults

from cubicweb_api.api_transaction import ApiTransactionsRepository
from cubicweb_api.auth.jwt_auth import setup_jwt
from cubicweb_api.constants import (
    API_ROUTE_NAME_PREFIX,
)
from cubicweb_api.openapi.openapi import setup_openapi
from cubicweb_api.util import get_cw_repo, get_transactions_repository

log = logging.getLogger(__name__)


class ApiRoutes(Enum):
    """
    All the available routes as listed in the openapi/openapi_template.yml file.
    """

    schema = "schema"
    rql = "rql"
    login = "login"
    current_user = "current_user"
    transaction_begin = "transaction/begin"
    transaction_execute = "transaction/execute"
    transaction_commit = "transaction/commit"
    transaction_rollback = "transaction/rollback"
    help = "help"


def get_route_name(route_name: ApiRoutes) -> str:
    """
    Generates a unique route name using the api prefix to prevent clashes with routes
    from other cubes.

    :param route_name: The route name base
    :return: The generated route name
    """
    return f"{API_ROUTE_NAME_PREFIX}{route_name.value}"


@view_defaults(
    request_method="POST",
    renderer="cubicweb_api_json",
    require_csrf=False,
    openapi=True,
    use_api_exceptions=True,
)
class ApiViews:
    def __init__(self, request: Request):
        self.request = request

    @view_config(
        route_name=get_route_name(ApiRoutes.schema),
        request_method="GET",
        anonymous_or_connected=True,
    )
    def schema_route(self):
        """
        See the openapi/openapi_template.yml file for more information on this route.
        """
        repo = get_cw_repo(self.request)
        exporter = JSONSchemaExporter()
        exported_schema = exporter.export_as_dict(repo.schema)
        return exported_schema

    @view_config(route_name=get_route_name(ApiRoutes.rql), anonymous_or_connected=True)
    def rql_route(self):
        """
        See the openapi/openapi_template.yml file for more information on this route.
        """
        request_params = self.request.openapi_validated.body
        query: str = request_params["query"]
        params: dict = request_params["params"]
        rset = self.request.cw_cnx.execute(query, params).rows
        self.request.cw_cnx.commit()
        return rset

    @view_config(
        route_name=get_route_name(ApiRoutes.login),
    )
    def login_route(self):
        """
        See the openapi/openapi_template.yml file for more information on this route.
        """
        request_params = self.request.openapi_validated.body
        login: str = request_params["login"]
        pwd: str = request_params["password"]

        repo = get_cw_repo(self.request)
        with repo.internal_cnx() as cnx:
            try:
                cwuser = repo.authenticate_user(cnx, login, password=pwd)
            except AuthenticationError:
                raise AuthenticationError("Invalid credentials")

            headers = remember(
                self.request,
                cwuser.eid,
            )
            return Response(headers=headers, status=204)

    @view_config(
        route_name=get_route_name(ApiRoutes.current_user),
        request_method="GET",
        anonymous_or_connected=True,
    )
    def current_user(self):
        """
        See the openapi/openapi_template.yml file for more information on this route.
        """
        user = self.request.cw_cnx.user
        return {"eid": user.eid, "login": user.login, "dcTitle": user.dc_title()}

    @view_config(
        route_name=get_route_name(ApiRoutes.transaction_begin),
        anonymous_or_connected=True,
    )
    def transaction_begin_route(self):
        """
        See the openapi/openapi_template.yml file for more information on this route.
        """
        transactions = get_transactions_repository(self.request)
        user = self.request.cw_cnx.user
        return transactions.begin_transaction(user)

    @view_config(
        route_name=get_route_name(ApiRoutes.transaction_execute),
        anonymous_or_connected=True,
    )
    def transaction_execute_route(self):
        """
        See the openapi/openapi_template.yml file for more information on this route.
        """
        transactions = get_transactions_repository(self.request)
        request_params = self.request.openapi_validated.body
        uuid: str = request_params["uuid"]
        query: str = request_params["query"]
        params: dict = request_params["params"]
        return transactions[uuid].execute(query, params).rows

    @view_config(
        route_name=get_route_name(ApiRoutes.transaction_commit),
        anonymous_or_connected=True,
    )
    def transaction_commit_route(self):
        """
        See the openapi/openapi_template.yml file for more information on this route.
        """
        transactions = get_transactions_repository(self.request)
        request_params = self.request.openapi_validated.body
        uuid: str = request_params["uuid"]
        return transactions[uuid].commit()

    @view_config(
        route_name=get_route_name(ApiRoutes.transaction_rollback),
        anonymous_or_connected=True,
    )
    def transaction_rollback_route(self):
        """
        See the openapi/openapi_template.yml file for more information on this route.
        """
        transactions = get_transactions_repository(self.request)
        request_params = self.request.openapi_validated.body
        uuid: str = request_params["uuid"]
        rollback_result = transactions[uuid].rollback()
        transactions.end_transaction(uuid)
        return rollback_result


def includeme(config: Configurator):
    setup_jwt(config)
    repo = get_cw_repo(config)
    repo.api_transactions = ApiTransactionsRepository(repo)
    setup_openapi(config)
    config.pyramid_openapi3_register_routes()
    config.scan()
