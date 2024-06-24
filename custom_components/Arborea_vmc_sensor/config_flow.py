import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv

DOMAIN = "vmc_sensor"


class VmcSensorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return VmcSensorOptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title=user_input["device_name"], data=user_input
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        "device_name",
                        description="Enter a unique name for your VMC device",
                    ): cv.string,
                }
            ),
            description_placeholders={"device_name": "Name of the VMC device"},
        )


class VmcSensorOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        "device_name",
                        default=self.config_entry.data.get("device_name", ""),
                        description="Update the name of the VMC device",
                    ): cv.string,
                }
            ),
            description_placeholders={
                "device_name": "Update the name of the VMC device"
            },
        )
