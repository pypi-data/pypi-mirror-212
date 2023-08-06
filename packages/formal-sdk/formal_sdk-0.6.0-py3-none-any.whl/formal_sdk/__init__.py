from . import datastore

SERVER_URL = "https://adminv2.api.formalcloud.net"


class Client(object):
    """Formal Admin API Client"""

    def __init__(self, api_key):
        """Constructor.

        Args:
            api_key: Formal API Key
        """

        self.DataStoreClient = datastore.DataStoreService(SERVER_URL, api_key)
