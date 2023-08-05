"""WebApi Poller for OpenThermWeb."""
from __future__ import annotations

import urllib.parse

import requests

from .const import TIMEOUT
from .opentherm_controller import OpenThermController


class OpenThermWebApi:
    """Class to communicate with OpenTherm Webapi."""

    def __init__(self, host: str, secret: str) -> None:
        """Initialize."""
        self.host = host
        self.secret = secret

    def authenticate(self) -> bool:
        """Test connection."""

        token = self.get_token
        if token:
            return True

        return False

    def get_token(self) -> str:
        """Get bearer token."""
        api_url = urllib.parse.urljoin(self.host, "/connect/token")
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        data = {
            "grant_type": "client_credentials",
            "scope": "OpenThermAPI",
        }

        response = requests.post(
            api_url,
            data=data,
            headers=headers,
            auth=("WebApi", self.secret),
            timeout=TIMEOUT,
        ).json()

        return response.get("access_token")

    def get_controller(self) -> OpenThermController:
        """Retrieve controller."""
        token = self.get_token()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }

        api_url = urllib.parse.urljoin(self.host, "/opentherm/controller")
        response = requests.get(api_url, headers=headers, timeout=TIMEOUT)

        return OpenThermController(self, response)

    def push_change(self, controller: OpenThermController) -> None:
        """Push controller."""
        token = self.get_token()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }

        api_url = urllib.parse.urljoin(self.host, "/opentherm/controller")
        data = {
            "deviceId": controller.device_id,
            "enabled": controller.enabled,
            "roomSetpoint": controller.room_setpoint,
            "dhwSetpoint": controller.dhw_setpoint,
            "away": controller.away,
        }
        requests.put(api_url, headers=headers, json=data, timeout=TIMEOUT)


