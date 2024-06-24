import logging
import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME, STATE_UNKNOWN
from homeassistant.core import callback
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import async_track_state_change_event
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

CONF_DEVICE_NAME = "device_name"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_DEVICE_NAME): cv.string,
    }
)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    return


async def async_setup_entry(hass, config_entry, async_add_entities):
    device_name = config_entry.data[CONF_DEVICE_NAME]

    vmc_sensor = VmcSensor(device_name)
    dehumidification_sensor = DehumidificationSensor(device_name)
    humidity_alarm_sensor = HumidityAlarmSensor(device_name)
    last_message_sensor = LastMessage(device_name)
    async_add_entities(
        [
            vmc_sensor,
            dehumidification_sensor,
            humidity_alarm_sensor,
            last_message_sensor,
        ]
    )


class VmcSensor(Entity):
    def __init__(self, device_name):
        self._name = f"{device_name} VMC Sensor"
        self._state = STATE_UNKNOWN
        self._device_name = device_name

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    async def async_added_to_hass(self):
        self.hass.bus.async_listen("myhome_message_event", self.handle_event)

    @callback
    def handle_event(self, event):
        data = event.data
        who = data.get("who")
        where = data.get("where")
        what = data.get("what")

        if who == 25 and where == "231":
            if what == 22:
                self._state = "off"
            elif what == 24:
                self._state = "on"
            self.async_write_ha_state()


class LastMessage(Entity):
    def __init__(self, device_name):
        self._name = f"{device_name} LastMessage"
        self._state = STATE_UNKNOWN
        self._device_name = device_name

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    async def async_added_to_hass(self):
        self.hass.bus.async_listen("myhome_message_event", self.handle_event)

    @callback
    def handle_event(self, event):
        self._state = str(event.data)
        self.async_write_ha_state()


class DehumidificationSensor(Entity):
    def __init__(self, device_name):
        self._name = f"{device_name} Deumidificazione"
        self._state = STATE_UNKNOWN
        self._device_name = device_name

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    async def async_added_to_hass(self):
        self.hass.bus.async_listen("myhome_message_event", self.handle_event)

    @callback
    def handle_event(self, event):
        data = event.data
        who = data.get("who")
        where = data.get("where")
        what = data.get("what")

        if who == 1 and where in [1, 2]:
            if what == 1:
                self._state = "on"
            elif what == 0:
                self._state = "off"
            self.async_write_ha_state()


class HumidityAlarmSensor(Entity):
    def __init__(self, device_name):
        self._name = f"{device_name} Allarme Umidità"
        self._state = STATE_UNKNOWN
        self._device_name = device_name

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    async def async_added_to_hass(self):
        self.hass.bus.async_listen("myhome_message_event", self.handle_event)

    @callback
    def handle_event(self, event):
        data = event.data
        who = data.get("who")
        where = data.get("where")
        what = data.get("what")

        if who == 1 and where == 3:
            if what == 0:
                self._state = "on"
            elif what == 1:
                self._state = "off"
            self.async_write_ha_state()
