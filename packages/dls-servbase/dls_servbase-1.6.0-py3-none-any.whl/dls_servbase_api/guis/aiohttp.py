import logging

# Class for an aiohttp client.
from dls_servbase_api.aiohttp_client import AiohttpClient

logger = logging.getLogger(__name__)


# ------------------------------------------------------------------------------------------
class Aiohttp(AiohttpClient):
    """
    Object implementing client side API for talking to the dls_servbase_gui server.
    Please see doctopic [A01].
    """

    # ----------------------------------------------------------------------------------------
    def __init__(self, specification):

        # We will get an umbrella specification which must contain an aiohttp_specification within it.
        AiohttpClient.__init__(
            self,
            specification["type_specific_tbd"]["aiohttp_specification"],
        )
