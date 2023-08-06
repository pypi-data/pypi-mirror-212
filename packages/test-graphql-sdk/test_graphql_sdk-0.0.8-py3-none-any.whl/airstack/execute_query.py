import json
import re
from send_request import SendRequest
from graphql import parse, print_ast
from generic import find_page_info, add_cursor_to_input_field, replace_cursor_value, \
    has_cursor
from constant import AirstackConstants


class AirstackClient:
    """Class to create api client for airstack api's
    """

    def __init__(self, url=None, api_key=None):
        """Init function for api client

        Args:
            url (str, optional): base url for server. Defaults to None.
            api_key (str, required): api key. Defaults to None.

        Raises:
            ValueError: _description_
        """
        self.url = AirstackConstants.API_ENDPOINT_PROD if url is None else url
        if api_key is None:
            raise ValueError("API key must be provided.")

        self.timeout = AirstackConstants.API_TIMEOUT
        self.api_key = api_key

    async def execute_query(self, query=None, variables=None):
        """Async function to run a GraphQL query and get the data

        Args:
            query (str): GraphQL query string. Defaults to None
            variables (dict, optional): Variables for the query. Defaults to
            None.

        Returns:
            Tuple: GraphQL response data or None, GraphQL response status code, error message or None
        """
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        }
        payload = {
            'query': query,
            'variables': variables
        }

        response, status_code, error = await SendRequest.send_post_request(
            url=self.url, headers=headers, data=json.dumps(payload), timeout=self.timeout)
        return response, status_code, error

    async def execute_paginated_query(self, query=None, variables=None):
        """Async function to execute paginated query.

        Args:
            query (str): GraphQL query string. Defaults to None
            variables (dict, optional): Variables for the query. Defaults to
            None.

        Returns:
            Tuple: GraphQL response data or None, GraphQL response status code, error message or None, next cursor,
            previous cursor
        """
        regex = re.compile(r'pageInfo')
        has_page_info = regex.search(query)
        if has_page_info is None:
            return None, None, "Pass query having pageInfo", None, None, None, None

        response, status_code, error = await self.execute_query(query, variables)
        page_info = {}
        for _key, value in response.items():
            page_info[_key] = find_page_info(response[_key])

        has_next_page = any(page_info['nextCursor'] != '' for page_info in page_info.values())
        has_prev_page = any(page_info['prevCursor'] != '' for page_info in page_info.values())

        async def get_next_page():
            """Func to get the next page data

            Returns:
                Tuple: GraphQL response data or None, GraphQL response status code, error message or None, next cursor,
                previous cursor
            """
            next_query = query
            for _page_info_key, _page_info_value in page_info.items():
                if _page_info_value['nextCursor'] == "":
                    continue
                document_ast = parse(next_query)
                if has_cursor(document_ast, _page_info_key):
                    replace_cursor_value(document_ast, _page_info_key, _page_info_value['nextCursor'])
                else:
                    add_cursor_to_input_field(document_ast, _page_info_key, _page_info_value['nextCursor'])
                next_query = print_ast(document_ast)
            return await self.execute_paginated_query(next_query, variables)

        async def get_prev_page():
            """Func to get the previous page data

            Returns:
                Tuple: GraphQL response data or None, GraphQL response status code, error message or None, next cursor,
                previous cursor
            """
            next_query = query
            for _page_info_key, _page_info_value in page_info.items():
                if _page_info_value['prevCursor'] == "":
                    continue
                document_ast = parse(next_query)
                if has_cursor(document_ast, _page_info_key):
                    replace_cursor_value(document_ast, _page_info_key, _page_info_value['prevCursor'])
                else:
                    add_cursor_to_input_field(document_ast, _page_info_key, _page_info_value['prevCursor'])
                next_query = print_ast(document_ast)
            return await self.execute_paginated_query(next_query, variables)

        return response, status_code, error, has_next_page, has_prev_page, get_next_page, get_prev_page
