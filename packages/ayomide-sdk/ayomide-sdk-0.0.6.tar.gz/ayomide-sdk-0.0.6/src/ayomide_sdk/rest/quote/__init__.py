from ayomide_sdk.api_resources.abstract import AbstractBaseClass


class Quote:
    def __init__(self, client_sdk, api_type):
        """
        Initialize the Quote class
        """
        self.api_type = api_type
        self.client_sdk = client_sdk

    def get(self, params=None, filters={}):
        return self.client_sdk.request(
            method_type="get", params=params, api_type=self.api_type, filters=filters
        )

    def __repr__(self):
        """
        string representation
        """
        return "<ayomide_sdk.Quote>"
