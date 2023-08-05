from .opentherm_web_api import OpenThermWebApi
from requests import Response

class OpenThermController:
    """Class that represents the data object that holds the data."""

    web_api: OpenThermWebApi

    def __init__(self, web_api: OpenThermWebApi, response: Response) -> None:
        """Initiatlize."""
        self.web_api = web_api
        json = response.json()
        self.device_id = json.get("deviceId")
        self.dhw_setpoint = json.get("dhwSetpoint")
        self.chw_setpoint = json.get("chwSetpoint")
        self.room_setpoint = json.get("roomSetpoint")
        self.away = json.get("away")
        self.enabled = json.get("enabled")
        self.chw_temperature = json.get("chwTemperature")
        self.dhw_temperature = json.get("dhwTemperature")
        self.room_temperature = json.get("roomTemperature")
        self.outside_temperature = json.get("outsideTemperature")
        self.chw_active = json.get("chwActive")
        self.dhw_active = json.get("dhwActive")

    def set_room_temperature(self, temperature: float) -> None:
        """Set room temperature."""
        self.room_setpoint = temperature
        self.web_api.push_change(self)

    def set_dhw_temperature(self, temperature: float) -> None:
        """Set domestic hot water temperature."""
        self.dhw_setpoint = temperature
        self.web_api.push_change(self)

    def set_away_mode(self, away_mode: bool) -> None:
        """Set away mode."""
        self.away = away_mode
        self.web_api.push_change(self)

    def set_hvac_mode(self, enabled: bool) -> None:
        """Set HVAC mode."""
        self.enabled = enabled
        self.web_api.push_change(self)
