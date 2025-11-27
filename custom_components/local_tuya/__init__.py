import logging
import tinytuya
from datetime import timedelta
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DOMAIN, CONF_DEVICE_ID, CONF_IP_ADDRESS, CONF_LOCAL_KEY, CONF_VERSION, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor", "switch"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {})

    device_id = entry.data[CONF_DEVICE_ID]
    ip_address = entry.data[CONF_IP_ADDRESS]
    local_key = entry.data[CONF_LOCAL_KEY]
    version = float(entry.data.get(CONF_VERSION, 3.5))

    try:
        device = tinytuya.OutletDevice(device_id, ip_address, local_key)
        device.set_version(version)
        device.set_socketPersistent(True)
        
        # === 后台强制开启极速刷新 (即使前端没有按钮) ===
        _LOGGER.info("后台激活极速刷新模式...")
        await hass.async_add_executor_job(device.set_value, '101', True)
        
    except Exception as e:
        _LOGGER.error(f"Tinytuya 初始化失败: {e}")
        return False

    last_known_data = {}

    async def async_update_data():
        nonlocal last_known_data
        try:
            data = await hass.async_add_executor_job(lambda: device.status())
            
            new_dps = {}
            if 'dps' in data:
                new_dps = data['dps']
                # 自动保活：如果发现 101 被关了，立即重开
                if new_dps.get('101') is False:
                     hass.async_add_executor_job(device.set_value, '101', True)
            elif 'Error' in data:
                return last_known_data

            last_known_data.update(new_dps)
            return last_known_data

        except Exception as err:
            if last_known_data:
                return last_known_data
            raise UpdateFailed(f"Connection lost: {err}")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=async_update_data,
        update_interval=timedelta(seconds=UPDATE_INTERVAL),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = {
        "device": device,
        "coordinator": coordinator
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        data = hass.data[DOMAIN].pop(entry.entry_id)
        try:
            data["device"].close()
        except:
            pass
    return unload_ok