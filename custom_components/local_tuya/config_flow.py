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

        schema = vol.Schema({
            vol.Required(CONF_IP_ADDRESS): str,
            vol.Required(CONF_DEVICE_ID): str,
            vol.Required(CONF_LOCAL_KEY): str,
            vol.Optional(CONF_VERSION, default=3.5): float,
        })

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    @staticmethod
    def async_get_options_flow(config_entry):
        return SimpleLocalTuyaOptionsFlow(config_entry)


class SimpleLocalTuyaOptionsFlow(config_entries.OptionsFlow):
    """支持添加后编辑配置"""

    def __init__(self, config_entry):
        self._config_entry = config_entry

    async def async_step_init(self, user_input=None):
        errors = {}
        if user_input is not None:
            # options 保存后，触发集成重载以应用新配置
            return self.async_create_entry(title="", data=user_input)

        # 用当前配置作为默认值
        conf = {**self._config_entry.data, **self._config_entry.options}
        schema = vol.Schema({
            vol.Required(CONF_IP_ADDRESS, default=conf.get(CONF_IP_ADDRESS, "")): str,
            vol.Required(CONF_DEVICE_ID, default=conf.get(CONF_DEVICE_ID, "")): str,
            vol.Required(CONF_LOCAL_KEY, default=conf.get(CONF_LOCAL_KEY, "")): str,
            vol.Optional(CONF_VERSION, default=conf.get(CONF_VERSION, 3.5)): float,
        })

        return self.async_show_form(step_id="init", data_schema=schema, errors=errors)
