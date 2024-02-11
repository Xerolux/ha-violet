"""This script fetches data from an API and creates sensors in Home Assistant."""

import re
import requests
from homeassistant.helpers.typing import HomeAssistantType

API_URL = "https://violet.pooldigital.de/getReadings?ALL"

def fetch_data():
    """Fetch data from the API."""
    response = requests.get(API_URL)
    return response.json()

def create_sensors(hass: HomeAssistantType, data: dict):
    """Create sensors in Home Assistant."""
    for key, value in data.items():
        if match := re.match(
            r"([a-zA-Z]+)(\d+)?_(value|state|runtime|last_on|last_off)?", key
        ):
            sensor_type, sensor_num, sensor_property = match.groups()
            friendly_name = f"{sensor_type.capitalize()} {sensor_num}" if sensor_num else sensor_type.capitalize()
            unit_of_measurement = ""
            # Determine unit of measurement for specific sensors
            if sensor_property == "value":
                unit_of_measurement = "°C" if sensor_type.startswith("onewire") else ""
            elif sensor_property == "runtime":
                unit_of_measurement = "h m s"
            elif sensor_property in ["last_on", "last_off"]:
                unit_of_measurement = "timestamp"
            # Set up the sensor entity
            sensor_name = f"sensor.{key}"
            hass.states.set(sensor_name, value, {
                "unit_of_measurement": unit_of_measurement,
                "friendly_name": friendly_name
            })
        else:
            # Default handling if no regex match
            friendly_name = key.replace("_", " ").title()
            sensor_name = f"sensor.{key}"
            hass.states.set(sensor_name, value, {
                "friendly_name": friendly_name
            })

def setup(hass: HomeAssistantType):
    """Set up the Home Assistant integration."""
    data = fetch_data()
    create_sensors(hass, data)
    return True

if __name__ == "__main__":
    # Replace None with your Home Assistant instance
    #hass_instance = YourHomeAssistantInstance()
    setup(hass_instance)