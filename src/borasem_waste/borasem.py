import argparse
import logging
import sys

from borasem_waste import __version__

from typing import List

from . import auth
from . import wastepickup
from . import borasem_const
import json

__author__ = "Daniel Oldberg"
__copyright__ = "Daniel Oldberg"
__license__ = "MIT"

_logger = logging.getLogger(__name__)

class BorasEM:
    """Class to communicate with the Borås Energi och Miljö Waste API."""

    def __init__(self, auth: auth.Auth):
        """Initialize the API and store the auth so we can make requests."""
        self.auth = auth

    async def async_get_schedule(self) -> List[wastepickup.WastePickup]:
        """Return the schedule of the containers."""
        resp = await self.auth.request("get", (borasem_const.WASTE_PATH + "/" + borasem_const.SCHEDULE_PATH + "?" + borasem_const.ADDRESS_PARAM + "=Häglared Lunden 2, Dalsjöfors (44195547)"))
        resp.raise_for_status()
        response = await resp.json()
        return [wastepickup.WastePickup(schedule_data, self.auth) for schedule_data in response['RhServices']]

    async def async_get_address(self, address: str) -> List[str]:
        """Return any matching addresses."""
        resp = await self.auth.request("post", (borasem_const.WASTE_PATH + "/" + borasem_const.ADDRESSSEARCH_PATH), json={'searchText': address })
        resp.raise_for_status()
        response = await resp.json()
        return response['Buildings']