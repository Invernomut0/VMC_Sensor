import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import STATE_OFF, STATE_ON, STATE_UNKNOWN
from homeassistant.core import callback

_LOGGER = logging.getLogger(__name__)

DOMAIN = "vmc_sensor"


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the VMC sensor platform."""
    sensor = vmc_sensor()
    async_add_entities([sensor])

    @callback
    def handle_myhome_event(event):
        """Handle incoming myhome_message_event."""
        data = event.data
        sensor.update_state(data)

    hass.bus.async_listen("myhome_message_event", handle_myhome_event)

    return True


class vmc_sensor(SensorEntity):
    """Representation of a MyHome Sensor."""

    def __init__(self):
        """Initialize the sensor."""
        self._state = STATE_UNKNOWN
        self._attr_dehumidification = STATE_UNKNOWN
        self._attr_humidity_alarm = STATE_UNKNOWN

    @property
    def name(self):
        """Return the name of the sensor."""
        return "VMC Sensor"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            "Deumidificazione": self._attr_dehumidification,
            "Allarme_Umidità": self._attr_humidity_alarm,
        }

    @callback
    def update_state(self, data):
        """Update the sensor state based on the event data."""
        who = data.get("who")
        where = data.get("where")
        what = data.get("what")

        if who == 25 and where == "231":
            if what == 22:
                self._state = STATE_ON
            elif what == 24:
                self._state = STATE_OFF

        if who == 1 and where in ["01", "02"]:
            if what == 1:
                self._attr_dehumidification = STATE_ON
            elif what == 0:
                self._attr_dehumidification = STATE_OFF

        if who == 1 and where == "03":
            if what == 0:
                self._attr_humidity_alarm = STATE_ON
            elif what == 1:
                self._attr_humidity_alarm = STATE_OFF

        self.async_write_ha_state()
