import logging
from http import cookies
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class CookieParser:

    # ----------------------------------------------------------------------------------------
    def parse_raw(self, raw: Optional[str]) -> Dict:
        """ """

        cookie_dict = {}
        if raw is not None:
            items = raw.split(";")

            for item in items:
                parts = item.split("=", 1)

                if len(parts) == 2:
                    cookie_dict[parts[0].strip()] = parts[1].strip()

        return cookie_dict

    # ----------------------------------------------------------------------------------------
    def __parse_raw_WITH_HTTP_COOKIES(self, raw: str) -> Dict:
        """
        This doesn't work when raw is like: 'Something="{something}"; X=Y;'
        """

        http_cookies: cookies.SimpleCookie = cookies.SimpleCookie()

        http_cookies.load(raw)

        cookie_dict = {}
        for key, morsel in http_cookies.items():
            cookie_dict[key] = morsel.value

        return cookie_dict
