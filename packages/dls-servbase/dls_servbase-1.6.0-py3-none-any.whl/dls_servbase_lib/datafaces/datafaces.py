# Use standard logging in this module.
import logging
from typing import Any, Dict, Type

# Class managing list of things.
from dls_utilpack.things import Things

# Class types.
from dls_servbase_api.constants import ClassTypes

# Exceptions.
from dls_servbase_api.exceptions import NotFound

logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------------------


class Datafaces(Things):
    """
    Factory for creating instances of dls_servbase_dataface.

    Since it is based on Things, it also can maintain a list of named instances.

    There are currently two class types which implement dls_servbase_dataface:
        AIOHTTP - This is a networked service with an HTTP protocol.
        NORMSQL - This is implement directly on a sqlite/mysql/postgres database.
    """

    # ----------------------------------------------------------------------------------------
    def __init__(self, name=None):
        """
        Args:
            name (_type_, optional): Name of this list used in debug messages. Defaults to None.
        """
        Things.__init__(self, name)

    # ----------------------------------------------------------------------------------------
    def build_object(self, specification: Dict) -> Any:
        """
        Build an object whose type is contained in the specification as a string.

        Args:
            specification (Dict): Specification, must contain at least the keyword "type".

        Returns:
            The dls_servbase_dataface instance.
        """

        dls_servbase_dataface_class = self.lookup_class(specification["type"])

        try:
            dls_servbase_dataface_object = dls_servbase_dataface_class(specification)
        except Exception as exception:
            raise RuntimeError(
                "unable to build dls_servbase_dataface object for type %s"
                % (dls_servbase_dataface_class)
            ) from exception

        return dls_servbase_dataface_object

    # ----------------------------------------------------------------------------------------
    def lookup_class(self, class_type: str) -> Type:
        """
        From the given class type string, return a class corresponding to the type.

        Returns:
            A class which can be instantiated.
        """

        if class_type == ClassTypes.AIOHTTP:
            from dls_servbase_lib.datafaces.aiohttp import Aiohttp

            return Aiohttp

        elif class_type == ClassTypes.NORMSQL:
            from dls_servbase_lib.datafaces.normsql import Normsql

            return Normsql

        raise NotFound(
            "unable to get dls_servbase_dataface class for type %s" % (class_type)
        )
