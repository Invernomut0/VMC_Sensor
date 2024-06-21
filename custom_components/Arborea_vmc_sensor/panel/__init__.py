DOMAIN = "vmc_sensor"

async def async_setup(hass, config):
    hass.http.register_static_path("/vmc_panel", hass.config.path("custom_components/vmc_sensor/panel"), False)
    hass.components.frontend.async_register_built_in_panel(
        "iframe", "VMC Panel", "mdi:fan", DOMAIN, {"url": "/local/community/vmc_sensor/panel.html"}
    )
    return True