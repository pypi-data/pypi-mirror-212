import logging

# Utilities.
from dls_utilpack.describe import describe

from dls_servbase_lib.cookies.cookie_parser import CookieParser

logger = logging.getLogger(__name__)


class TestParseCookie:
    """
    Test parsing a raw cookie value.
    """

    # ----------------------------------------------------------------------------------------
    def test(
        self,
        constants,
        logging_setup,
        output_directory,
    ):
        """ """

        part1 = 'CookieControl={"necessaryCookies":[],"optionalCookies":{"analytics":"accepted"},"statement":{"shown":true,"updated":"20/02/2019"},"consentDate":1684481396049,"consentExpiry":90,"interactedWith":true,"user":"6621E582-416C-4069-9604-A9A9C1EC3D1C"};'
        part2 = "_ga=GA1.3.145778769.1684481396; BXFLOW_RECENT_JOBS_UX=1975b4df-8d91-4e09-ab26-3f47aabe984d; BXFLOW_JOB_SUBMIT_UX=775a8760-7a81-4f2d-824c-067b89bf4561; BXFLOW_JOB_NEWS_UX=37bdfb1b-ceba-43e8-b108-9fb5ffb29186; BXFLOW_JOB_VARIABLES_UX=58c35196-47a0-4a82-9ecc-e96ec488899a; BXFLOW_JOB_DETAILS_UX=eb72189d-481d-4d9d-af81-4c900073e10d; BXFLOW_JOB_DATA_GRID_UX=a43220f9-c997-42dd-aee5-cd44048f5f20; BXFLOW_TABS_MANAGER=89353ec2-59e8-4d73-bbfc-2d249859227a"

        cookies = CookieParser().parse_raw(part1 + " " + part2)

        logger.debug(describe("[COOKOFF] cookies", cookies))
