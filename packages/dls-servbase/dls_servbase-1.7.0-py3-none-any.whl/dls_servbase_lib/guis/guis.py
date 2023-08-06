# Use standard logging in this module.
import logging

# Class managing list of things.
from dls_utilpack.things import Things

# Exceptions.
from dls_servbase_api.exceptions import NotFound

# Types.
from dls_servbase_api.guis.constants import Types

logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------------------


class Guis(Things):
    """
    List of available dls_servbase_guis.
    """

    # ----------------------------------------------------------------------------------------
    def __init__(self, name=None):
        Things.__init__(self, name)

    # ----------------------------------------------------------------------------------------
    def build_object(self, specification):
        """"""

        dls_servbase_gui_class = self.lookup_class(specification["type"])

        try:
            dls_servbase_gui_object = dls_servbase_gui_class(specification)
        except Exception as exception:
            raise RuntimeError(
                "unable to build dls_servbase_gui object for type %s"
                % (dls_servbase_gui_class)
            ) from exception

        return dls_servbase_gui_object

    # ----------------------------------------------------------------------------------------
    def lookup_class(self, class_type):
        """"""

        if class_type == Types.AIOHTTP:
            from dls_servbase_lib.guis.aiohttp import Aiohttp

            return Aiohttp

        raise NotFound(
            "unable to get dls_servbase_gui class for type %s" % (class_type)
        )
