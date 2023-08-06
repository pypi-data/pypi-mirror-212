import logging

# Class for an aiohttp client.
from dls_servbase_api.aiohttp_client import AiohttpClient

# Dataface protocolj things.
from dls_servbase_api.datafaces.constants import Commands, Keywords

logger = logging.getLogger(__name__)


class Aiohttp(AiohttpClient):
    """
    Object implementing client side API for talking to the dls_servbase_dataface server.
    """

    # ----------------------------------------------------------------------------------------
    def __init__(self, specification):

        # We will get an umbrella specification which must contain an aiohttp_specification within it.
        AiohttpClient.__init__(
            self,
            specification["type_specific_tbd"]["aiohttp_specification"],
        )

    # ----------------------------------------------------------------------------------------
    def specification(self):
        return self.__specification

    # ----------------------------------------------------------------------------------------
    async def query(self, sql, subs=None, why=None):
        """"""
        return await self.__send_protocolj("query", sql, subs=subs, why=why)

    # ----------------------------------------------------------------------------------------
    async def execute(self, sql, subs=None, why=None):
        """"""
        return await self.__send_protocolj("execute", sql, subs=subs, why=why)

    # ----------------------------------------------------------------------------------------
    async def insert(self, table_name, records, why=None):
        """"""
        return await self.__send_protocolj("insert", table_name, records, why=why)

    # ----------------------------------------------------------------------------------------
    async def update(self, table_name, record, where, subs=None, why=None):
        """"""
        return await self.__send_protocolj(
            "update", table_name, record, where, subs=subs, why=why
        )

    # ----------------------------------------------------------------------------------------
    async def set_cookie(self, cookie_dict):
        """ """
        return await self.__send_protocolj("set_cookie", cookie_dict)

    # ----------------------------------------------------------------------------------------
    async def get_cookie(self, cookie_uuid):
        """
        Get single cookie from its uuid.
        Returns database record format.
        """
        return await self.__send_protocolj("get_cookie", cookie_uuid)

    # ----------------------------------------------------------------------------------------
    async def update_cookie(self, row):
        """"""
        return await self.__send_protocolj("update_cookie", row)

    # ----------------------------------------------------------------------------------------
    async def __send_protocolj(self, function, *args, **kwargs):
        """"""

        return await self.client_protocolj(
            {
                Keywords.COMMAND: Commands.EXECUTE,
                Keywords.PAYLOAD: {
                    "function": function,
                    "args": args,
                    "kwargs": kwargs,
                },
            },
        )

    # ----------------------------------------------------------------------------------------
    async def report_health(self):
        """"""
        return await self.__send_protocolj("report_health")
