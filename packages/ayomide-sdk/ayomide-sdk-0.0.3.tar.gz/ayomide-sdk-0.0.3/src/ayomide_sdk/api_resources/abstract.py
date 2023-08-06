class AbstractBaseClass(object):
    """
    This is an abstract class for implementing abstract classes
    """

    def __init__(self, client_sdk):
        self.client_sdk = client_sdk

    def get(self, params=None, filters={}):
        """
        params contains things like id , subquery, etc
        filters contain filters for pagination e.g limit, page and offset
        """
        return self.client_sdk.request(
            method_type="get", params=params, api_type=self.api_type, filters=filters
        )
