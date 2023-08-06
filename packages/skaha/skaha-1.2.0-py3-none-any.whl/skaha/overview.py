"""Skaha Overview."""

import defusedxml.ElementTree as ET
from requests.models import Response

from skaha.client import SkahaClient
from skaha.utils import logs

log = logs.get_logger(__name__)


class Overview(SkahaClient):
    """Skaha Overview Client."""

    def availaibility(self) -> bool:
        """Check if the server backend is available.

        Returns:
            bool: True if the server is available, False otherwise.
        """
        response: Response = self.session.get(url=self.server + "/availability")  # type: ignore # noqa
        response.raise_for_status()  # type: ignore
        # Parse the XML string
        root = ET.fromstring(response.text)  # type: ignore
        available = root.find(
            ".//{http://www.ivoa.net/xml/VOSIAvailability/v1.0}available"
        ).text  # type: ignore
        log.info(f"Server available: {available}")
        if available == "true":
            return True
        return False
