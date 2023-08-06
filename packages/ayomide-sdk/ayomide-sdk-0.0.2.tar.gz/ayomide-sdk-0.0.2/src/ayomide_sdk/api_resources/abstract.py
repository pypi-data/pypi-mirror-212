class AbstractBaseClass(object):

    def __init__(self, client_sdk):
        self.client_sdk = client_sdk

    def get(self, params=None):
        return self.client_sdk.request("get", params=params)

    
