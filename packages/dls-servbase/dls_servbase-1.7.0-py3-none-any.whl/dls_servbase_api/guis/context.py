import logging

# Base class.
from dls_utilpack.client_context_base import ClientContextBase

# Things created in the context.
from dls_servbase_api.guis.guis import Guis, dls_servbase_guis_set_default

logger = logging.getLogger(__name__)


class Context(ClientContextBase):
    """
    Client context for a dls_servbase_gui object.
    On entering, it creates the object according to the specification (a dict).
    On exiting, it closes client connection.

    The aenter and aexit methods are exposed for use by an enclosing context and the base class.
    """

    # ----------------------------------------------------------------------------------------
    def __init__(self, specification):
        ClientContextBase.__init__(self, specification)

    # ----------------------------------------------------------------------------------------
    async def aenter(self):
        """ """

        # Build the object according to the specification.
        self.interface = Guis().build_object(self.specification)

        # If there is more than one gui, the last one defined will be the default.
        dls_servbase_guis_set_default(self.interface)

    # ----------------------------------------------------------------------------------------
    async def aexit(self):
        """ """

        if self.interface is not None:
            await self.interface.close_client_session()

            # Clear the global variable.  Important between pytests.
            dls_servbase_guis_set_default(None)
