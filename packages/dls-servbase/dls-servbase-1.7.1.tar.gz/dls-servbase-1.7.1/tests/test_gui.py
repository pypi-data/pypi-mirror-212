import logging

# Utilities.
from dls_utilpack.describe import describe

# API constants.
from dls_servbase_api.constants import Keywords as ProtocoljKeywords

# Client context.
from dls_servbase_api.guis.context import Context as GuiClientContext
from dls_servbase_api.guis.guis import dls_servbase_guis_get_default

# Dataface server context.
from dls_servbase_lib.datafaces.context import Context as DlsServbaseDatafaceContext

# GUI constants.
from dls_servbase_lib.guis.constants import Commands, Cookies, Keywords

# Server context.
from dls_servbase_lib.guis.context import Context as GuiServerContext

# Base class for the tester.
from tests.base_context_tester import BaseContextTester

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------
class TestGui:
    """
    Test the dls_servbase gui service.

    Fetch requests from the dataface similar to what javascript ajax would do.
    """

    def test(self, constants, logging_setup, output_directory):
        """ """

        configuration_file = "tests/configurations/sqlite.yaml"
        GuiTester().main(constants, configuration_file, output_directory)


# ----------------------------------------------------------------------------------------
class GuiTester(BaseContextTester):
    """
    Class with asyncio coroutine which does the actual test.
    """

    # Called from the base class main method.
    async def _main_coroutine(self, constants, output_directory):
        """ """

        # Make a multiconf and load the context configuration file.
        multiconf = self.get_multiconf()
        multiconf_dict = await multiconf.load()

        dataface_specification = multiconf_dict["dls_servbase_dataface_specification"]
        dataface_context = DlsServbaseDatafaceContext(dataface_specification)

        gui_specification = multiconf_dict["dls_servbase_gui_specification"]
        type_specific_tbd = gui_specification["type_specific_tbd"]
        aiohttp_specification = type_specific_tbd["aiohttp_specification"]
        aiohttp_specification["search_paths"] = [output_directory]

        # Make the server context.
        gui_server_context = GuiServerContext(gui_specification)

        # Make the client context.
        gui_client_context = GuiClientContext(gui_specification)

        # Start the dataface the gui uses for cookies.
        async with dataface_context:
            # Start the gui client context.
            async with gui_client_context:
                # And the gui server context which starts the coro.
                async with gui_server_context:
                    await self.__run_the_test(constants, output_directory)

    # ----------------------------------------------------------------------------------------

    async def __run_the_test(self, constants, output_directory):
        """ """
        # Reference the xchembku object which the context has set up as the default.
        gui = dls_servbase_guis_get_default()

        # --------------------------------------------------------------------
        # Use protocolj to fetch a request from the dataface.
        # Simulates what javascript would do by ajax.

        # Load tabs, of which there are none at the start.
        # This establishes the cookie though.
        load_tabs_request = {
            Keywords.COMMAND: Commands.LOAD_TABS,
            ProtocoljKeywords.ENABLE_COOKIES: [Cookies.TABS_MANAGER],
        }

        logger.debug("---------------------- making request 1 --------------------")
        logger.debug(describe("gui", gui))
        response = await gui.client_protocolj(load_tabs_request, cookies={})

        # The response is json, with the last saved tab_id, which is None at first.
        assert Keywords.TAB_ID in response
        assert response[Keywords.TAB_ID] is None

        # We should also have cookies back.
        assert "__cookies" in response
        cookies = response["__cookies"]
        assert Cookies.TABS_MANAGER in cookies

        # Use the tabs manager cookie value in the next requests.
        cookie_uuid = cookies[Cookies.TABS_MANAGER].value

        # --------------------------------------------------------------------
        # Select a tab.
        # The response is json, but nothing really to see in it.

        select_tab_request = {
            Keywords.COMMAND: Commands.SELECT_TAB,
            ProtocoljKeywords.ENABLE_COOKIES: [Cookies.TABS_MANAGER],
            Keywords.TAB_ID: "123",
        }

        logger.debug("---------------------- making request 2 --------------------")
        response = await gui.client_protocolj(
            select_tab_request, cookies={Cookies.TABS_MANAGER: cookie_uuid}
        )

        # --------------------------------------------------------------------
        # Load tabs again, this time we should get the saved tab_id.

        logger.debug("---------------------- making request 3 --------------------")
        # Put a deliberately funky cookie string into the header.
        raw_cookie_header = (
            'BadCookie={"something"}; ' + f"{Cookies.TABS_MANAGER} = {cookie_uuid};"
        )
        response = await gui.client_protocolj(
            load_tabs_request,
            headers={"Cookie": raw_cookie_header},
        )

        logger.debug(describe("second load_tabs response", response))
        assert Keywords.TAB_ID in response
        assert response[Keywords.TAB_ID] == "123"

        # --------------------------------------------------------------------
        # Update a tab.
        # The response is json, but nothing really to see in it.

        select_tab_request = {
            Keywords.COMMAND: Commands.SELECT_TAB,
            ProtocoljKeywords.ENABLE_COOKIES: [Cookies.TABS_MANAGER],
            Keywords.TAB_ID: "456",
        }

        logger.debug("---------------------- making request 4 --------------------")
        response = await gui.client_protocolj(
            select_tab_request,
            cookies={Cookies.TABS_MANAGER: cookie_uuid},
        )

        # --------------------------------------------------------------------
        # Load tabs again, this time we should get the updated tab_id.

        logger.debug("---------------------- making request 5 --------------------")
        response = await gui.client_protocolj(
            load_tabs_request,
            cookies={Cookies.TABS_MANAGER: cookie_uuid},
        )

        logger.debug(describe("third load_tabs response", response))
        assert Keywords.TAB_ID in response
        assert response[Keywords.TAB_ID] == "456"

        # --------------------------------------------------------------------
        # Write a text file and fetch it through the http server.
        filename = "test.html"
        contents = "some test html"
        with open(f"{output_directory}/{filename}", "wt") as file:
            file.write(contents)
        logger.debug(
            "---------------------- making request 6 (html file) --------------------"
        )
        text = await gui.client_get_file(filename)
        # assert text == contents

        # Write a binary file and fetch it through the http server.
        filename = "test.exe"
        contents = "some test binary"
        with open(f"{output_directory}/{filename}", "wt") as file:
            file.write(contents)
        binary = await gui.client_get_file(filename)
        # Binary comes back as bytes due to suffix of url filename.
        assert binary == contents.encode()

        # --------------------------------------------------------------------
        # Get an html file automatically configured in guis/html.
        filename = "javascript/version.js"
        # TODO: Put proper version into javascript somehow during packaging.
        contents = "dls_servbase___CURRENT_VERSION"
        text = await gui.client_get_file(filename)
        logger.debug(f"javascript version is {text.strip()}")
        assert contents in text
