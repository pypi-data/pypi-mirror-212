import logging

# Base class for an asyncio server context.
from dls_utilpack.server_context_base import ServerContextBase

# Things created in the context.
from dls_servbase_lib.guis.guis import Guis

logger = logging.getLogger(__name__)


thing_type = "dls_servbase_lib.dls_servbase_guis.context"


class Context(ServerContextBase):
    """
    Object representing an event dls_servbase_dataface connection.
    """

    # ----------------------------------------------------------------------------------------
    def __init__(self, specification):
        ServerContextBase.__init__(self, thing_type, specification)

    # ----------------------------------------------------------------------------------------
    async def aenter(self):
        """ """

        self.server = Guis().build_object(self.specification())

        if self.context_specification.get("start_as") == "coro":
            await self.server.activate_coro()

        elif self.context_specification.get("start_as") == "thread":
            await self.server.start_thread()

        elif self.context_specification.get("start_as") == "process":
            await self.server.start_process()

    # ----------------------------------------------------------------------------------------
    async def aexit(self, type, value, traceback):
        """ """

        if self.server is not None:
            # Put in request to shutdown the server.
            await self.server.client_shutdown()

            # Release a client connection if we had one.
            await self.server.close_client_session()
