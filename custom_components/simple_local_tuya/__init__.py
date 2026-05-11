import logging
import tinytuya
import time
from datetime import timedelta
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry, ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DOMAIN, CONF_DEVICE_ID, CONF_IP_ADDRESS, CONF_LOCAL_KEY, CONF_VERSION, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """初始化集成"""
    hass.data.setdefault(DOMAIN, {})

    # 合并 data 和 options，options 优先（支持编辑后生效）
    conf = {**entry.data, **entry.options}
    device_id = conf[CONF_DEVICE_ID]
    ip_address = conf[CONF_IP_ADDRESS]
    local_key = conf[CONF_LOCAL_KEY]
    version = float(conf.get(CONF_VERSION, 3.5))

    _LOGGER.info("正在初始化涂鸦设备: %s (ID: %s, 协议: %s)", ip_address, device_id, version)

    # 创建设备对象
    try:
        device = tinytuya.OutletDevice(device_id, ip_address, local_key)
        device.set_version(version)
        device.set_socketPersistent(True)
        device.set_socketTimeout(5)
    except Exception as e:
        _LOGGER.error("对象创建失败: %s", e)
        raise ConfigEntryNotReady(f"设备对象创建失败: {e}")

    # 缓存机制
    last_known_data = {}

    async def async_update_data():
        """核心循环：读取数据"""
        nonlocal last_known_data

        def worker():
            """在后台线程中执行设备读取，失败时自动重连重试"""
            result = device.status()
            # 首次失败则关闭重连再试一次
            if 'Error' in result:
                _LOGGER.debug("首次读取失败: %s，尝试重连...", result.get('Error', ''))
                try:
                    device.close()
                except Exception:
                    pass
                time.sleep(0.3)
                result = device.status()
            return result

        try:
            data = await hass.async_add_executor_job(worker)

            if 'dps' in data:
                last_known_data = data['dps']
                _LOGGER.debug("成功获取数据: %s 个DP点", len(last_known_data))
                return last_known_data

            # 设备返回错误
            error_msg = data.get('Error', '未知错误')
            err_code = data.get('Err', '')
            _LOGGER.warning("设备返回错误: [%s] %s", err_code, error_msg)

            if last_known_data:
                _LOGGER.debug("使用缓存数据")
                return last_known_data

            raise UpdateFailed(f"设备错误 [{err_code}]: {error_msg}")

        except UpdateFailed:
            raise
        except Exception as err:
            _LOGGER.warning("连接异常: %s", err)
            if last_known_data:
                return last_known_data
            raise UpdateFailed(f"连接异常: {err}")

    # 创建协调器
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=async_update_data,
        update_interval=timedelta(seconds=UPDATE_INTERVAL),
    )

    # 首次刷新
    try:
        await coordinator.async_config_entry_first_refresh()
    except Exception as err:
        _LOGGER.warning("首次刷新失败: %s，将在下次轮询时重试", err)

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
        except Exception:
            pass
    return unload_ok

async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
