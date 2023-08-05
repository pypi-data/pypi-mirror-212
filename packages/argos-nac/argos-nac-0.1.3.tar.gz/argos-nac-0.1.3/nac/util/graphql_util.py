import ssl
from pathlib import Path
from typing import Any
from urllib.request import urlopen

from sgqlc.endpoint.http import HTTPEndpoint

from nac.constants import ROOT_DIR

from .jinja_util import JinjaUtil
from ..model import *


class GraphQLUtil:
    @staticmethod
    def get_site_data(graphql_url: str, token: str, site_id: int, ignore_ssl: bool = False) -> Site:
        data = GraphQLUtil._send_request(graphql_url, token, site_id, ignore_ssl)
        return GraphQLUtil._parse_query_data(data, site_id)

    @staticmethod
    def _parse_query_data(data: dict, site_id: int) -> Site:
        # Gather & init prerequisites
        vrf_list = GraphQLUtil._get_or_raise(data, "vrf_list")
        interface_list = GraphQLUtil._get_or_raise(data, "interface_list")
        bgp_mesh_list = GraphQLUtil._get_or_raise(data, "bgp_mesh_list")
        QueryPrerequisites(
            vrf_list=vrf_list,
            interface_list=interface_list,
            bgp_mesh_list=bgp_mesh_list,
        )  # Initializing is enough to init datastructure map

        # Gather site data
        site_data = data.get("site", None)
        if site_data is None:
            raise Exception(f'Site with ID "{site_id}" does not appear to exist.')
        return Site(**site_data)

    @staticmethod
    def _get_or_raise(data: dict, field_name: str) -> Any:
        field = data.get(field_name, None)
        if field is None:
            raise Exception(f'Expected "{field_name}" element.')
        return field

    @staticmethod
    def _send_request(graphql_url: str, token: str, site_id: int, ignore_ssl: bool) -> dict:
        query_string = JinjaUtil.render_jinja_template(
            root_file=ROOT_DIR / "queries" / "main.gql",
            site_id=site_id,
        )
        headers = {"Authorization": f"Token {token}", "Accept": "application/json"}

        endpoint = HTTPEndpoint(
            graphql_url,
            headers,
            urlopen=GraphQLUtil.__urlopen_without_ssl_check if ignore_ssl else None,
            method="GET",
        )
        response = endpoint(query=query_string)
        errors = response.get("errors", None)
        if errors is not None:
            raise Exception("Errors in grapql query:\n" + "\n".join((e["message"] for e in errors)))
        return response.get("data", {})

    @staticmethod
    def __urlopen_without_ssl_check(*args, **kvargs) -> Any:
        '''
        Used to onkeypatch ssl certificate verification in case of locally running NetBox instance.
        '''
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        return urlopen(*args, context=ssl_context, **kvargs)  # type: ignore
