import requests
from ayomide_sdk.api_resources.helpers import build_filters


class ApiRequester:
    """
    This class implements the api calls needed in the application
    it implements get, post, put and delete methods
    """

    def __init__(self, method_type, url, headers, params, filters):
        self.method_type = method_type
        self.url = url
        self.headers = headers
        self.params = params
        self.filters = filters

    def get(self):
        filter_query = "?"

        if self.filters != {} and self.filters != None:
            filter_query = build_filters(self.filters)

        if self.params != None and self.params.get("id", None) != None:
            if self.params.get("subquery", None) == None:
                id = self.params["id"]
                endpoint = self.url + f"/{id}" + filter_query
                response = requests.get(
                    endpoint,
                    headers=self.headers,
                )
            else:
                id = self.params["id"]
                subquery = self.params["subquery"]
                endpoint = self.url + f"/{id}/{subquery}" + filter_query
                response = requests.get(
                    endpoint,
                    headers=self.headers,
                )
        else:
            endpoint = self.url + filter_query
            response = requests.get(
                endpoint,
                headers=self.headers,
            )
        return response

    def post():
        return {
            "status_code": 200,
            "json": {"message": "This method is not implemented"},
        }

    def put():
        return {
            "status_code": 200,
            "json": {"message": "This method is not implemented"},
        }

    def delete():
        return {
            "status_code": 200,
            "json": {"message": "This method is not implemented"},
        }
