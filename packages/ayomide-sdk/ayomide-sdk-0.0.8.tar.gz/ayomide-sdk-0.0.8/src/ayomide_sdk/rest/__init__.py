from ayomide_sdk.api_resources.constants import BASE_URL_V1, BASE_URL_V2
from ayomide_sdk.api_resources.api_requester import ApiRequester
from ayomide_sdk.api_resources.helpers import full_url_query_builder


class Client(object):
    """
    A client class for accessing the Lord Of The Ring API.
    Example
    client = Client(version="v2", api_key="API-KEY")
    ### version v2 by default
    client.quote.get()
    client.movie.get()
    """

    def __init__(self, api_key=None, version="v2"):
        base_url = BASE_URL_V1 if version.lower() == "v1" else BASE_URL_V2
        if api_key is None:
            raise Exception("Api key is required")

        if version.lower() == "v1":
            raise NotImplementedError(
                "This sdk does not support version v1 , please upgrade to v2"
            )
        try:
            self.base_url = base_url.strip().lower()
        except Exception as e:
            raise Exception(str(e))
        self.headers = {"Authorization": f"Bearer {api_key}"}

    def request(self, method_type, params=None, api_type=None, filters={}):
        method_type = method_type.upper()

        # build full url
        full_url = full_url_query_builder(self.base_url, api_type)

        api_requester = ApiRequester(
            url=full_url,
            method_type=method_type,
            params=params,
            headers=self.headers,
            filters=filters,
        )

        if method_type == "GET":
            response = api_requester.get()
        elif method_type == "PUT":
            response = api_requester.put()
        elif method_type == "POST":
            response = api_requester.post()
        elif method_type == "DELETE":
            response = api_requester.delete()

        json_response = response.json()
        return {"status": response.status_code, "json": json_response}

    @property
    def quote(self):
        """
        Access the Quote Api
        """
        from ayomide_sdk.rest.quote import Quote

        quote_resp = Quote(self, "quote")
        return quote_resp

    @property
    def movie(self):
        """
        Access the Movie API
        """
        from ayomide_sdk.rest.movie import Movie

        movie_resp = Movie(self, "movie")
        return movie_resp
