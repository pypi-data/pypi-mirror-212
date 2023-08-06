import asyncio
import logging
import os
import subprocess
import time

from dls_utilpack.describe import describe

from dls_servbase_api.databases.constants import CookieFieldnames, Tablenames
from dls_servbase_api.datafaces.context import Context as ClientContext

# Base class for the tester.
from tests.base_context_tester import BaseContextTester

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------
class TestCliSqlite:
    """
    Test that we can do a basic database operation through the service on sqlite databases.
    """

    def test(self, constants, logging_setup, output_directory):

        configuration_file = "tests/configurations/sqlite.yaml"
        CliTester(configuration_file).main(
            constants, configuration_file, output_directory
        )


# ----------------------------------------------------------------------------------------
class TestCliMysql:
    """
    Test that we can do a basic database operation through the service on mysql databases.
    """

    def test(self, constants, logging_setup, output_directory):

        configuration_file = "tests/configurations/mysql.yaml"
        CliTester(configuration_file).main(
            constants, configuration_file, output_directory
        )


# ----------------------------------------------------------------------------------------
class CliTester(BaseContextTester):
    """
    Class to test the dataface.
    """

    def __init__(self, configuration_file):
        BaseContextTester.__init__(self)

        self.__configuration_file = configuration_file

    async def _main_coroutine(self, constants, output_directory):
        """ """

        # Command to run the service.
        dls_servbase_server_cli = [
            "python",
            "-m",
            "dls_servbase_cli.main",
            "service",
            "--verbose",
            "--configuration",
            self.__configuration_file,
        ]

        # Let the output_directory symbol be replaced in the multiconf.
        os.environ["output_directory"] = output_directory

        # Launch the service as a process.
        logger.debug(f"launching {' '.join(dls_servbase_server_cli)}")
        process = subprocess.Popen(
            dls_servbase_server_cli,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        try:
            # Read the configuration.
            multiconf_object = self.get_multiconf()
            multiconf_dict = await multiconf_object.load()

            # Get a client context to the server in the process we just started.
            servbase_specification = multiconf_dict[
                "dls_servbase_dataface_specification"
            ]
            dls_servbase_client_context = ClientContext(servbase_specification)
            async with dls_servbase_client_context as dls_servbase_client:
                # Some easy sql query.
                all_sql = f"SELECT * FROM {Tablenames.COOKIES}"

                # Wait for process to be up.
                start_time = time.time()
                max_seconds = 5.0
                while True:
                    # Try to check the health.
                    health = await dls_servbase_client.client_report_health()

                    # Check if health report contains an exception.
                    exception = health.get("exception")
                    if exception is None:
                        logger.debug(describe("health", health))
                        # Continue with test if no exception.
                        break

                    logger.debug(f"[CONNRETRY] retrying after {exception}")

                    if process.poll() is not None:
                        raise RuntimeError(
                            "server apprently died without being able to give a health check"
                        )

                    # Too much time has elapsed?
                    if time.time() - start_time > max_seconds:
                        raise RuntimeError(
                            f"server not answering within {max_seconds} seconds"
                        )

                    await asyncio.sleep(1.0)

                # Interact with it.
                await dls_servbase_client.insert(
                    Tablenames.COOKIES,
                    [
                        {
                            CookieFieldnames.UUID: "f0",
                            CookieFieldnames.CONTENTS: "{'a': 'f000'}",
                        }
                    ],
                )

                records = await dls_servbase_client.query(all_sql)

                assert len(records) == 1
                assert records[0][CookieFieldnames.UUID] == "f0"
                assert records[0][CookieFieldnames.CONTENTS] == "{'a': 'f000'}"

                await dls_servbase_client.client_shutdown()
        finally:
            try:
                # Wait for the process to finish and get the output.
                stdout_bytes, stderr_bytes = process.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                # Timeout happens when client dies but server hasn't been told to shutdown.
                process.kill()
                stdout_bytes, stderr_bytes = process.communicate()

            # Get the return code of the process
            return_code = process.returncode
            logger.debug(f"server return_code is {return_code}")

            if len(stderr_bytes) > 0:
                logger.debug(
                    f"================================== server stderr is:\n{stderr_bytes.decode()}"
                )
            if len(stdout_bytes) > 0:
                logger.debug(
                    f"================================== server stdout is:\n{stdout_bytes.decode()}"
                )
            if len(stderr_bytes) > 0 or len(stdout_bytes) > 0:
                logger.debug("================================== end of server output")

        assert return_code == 0
