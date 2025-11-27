import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_DEVICE_ID, CONF_IP_ADDRESS, CONF_LOCAL_KEY, CONF_VERSION

class SimpleLocalTuyaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(
                title=f"Tuya {user_input[CONF_IP_ADDRESS]}",
                data=user_input
            )

        default_ip = "" 
        default_id = ""
        default_key = ""
        
        schema = vol.Schema({
            vol.Required(CONF_IP_ADDRESS, default=default_ip): str,
            vol.Required(CONF_DEVICE_ID, default=default_id): str,
            vol.Required(CONF_LOCAL_KEY, default=default_key): str,
            vol.Optional(CONF_VERSION, default=3.5): float,
        })

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)