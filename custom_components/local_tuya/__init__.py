import logging
import tinytuya
import time
from datetime import timedelta
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DOMAIN, CONF_DEVICE_ID, CONF_IP_ADDRESS, CONF_LOCAL_KEY, CONF_VERSION, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor", "switch"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """初始化集成"""
    hass.data.setdefault(DOMAIN, {})

    device_id = entry.data[CONF_DEVICE_ID]
    ip_address = entry.data[CONF_IP_ADDRESS]
    local_key = entry.data[CONF_LOCAL_KEY]
    version = float(entry.data.get(CONF_VERSION, 3.5))

    _LOGGER.info(f"正在初始化涂鸦设备: {ip_address}...")

    # === 1. 创建对象 (软启动) ===
    # 即使网络不通也创建对象，确保实体能注册成功
    try:
        device = tinytuya.OutletDevice(device_id, ip_address, local_key)
        device.set_version(version)
        device.set_socketPersistent(True) # 保持长连接
        device.set_socketTimeout(2)       # 设置超时
    except Exception as e:
        _LOGGER.error(f"对象创建失败: {e}")

    # 缓存机制
    last_known_data = {}

    async def async_update_data():
        """核心循环：读取数据"""
        nonlocal last_known_data
        
        # 定义后台同步任务
        def worker():
            # 纯净读取：只读取状态，不发送任何指令
            # 避免干扰设备或造成读写冲突
            return device.status()

        try:
            # 放入后台线程执行
            data = await hass.async_add_executor_job(worker)

            # 解析数据
            if 'dps' in data:
                last_known_data.update(data['dps'])
                return last_known_data
            
            elif 'Error' in data:
                # 只有当明确收到 Error 时才记录，且返回旧数据
                if last_known_data: return last_known_data
                return {} 
            
            return last_known_data

        except Exception as err:
            # 连接断开时不抛异常，返回旧数据，防止实体变不可用
            if last_known_data:
                return last_known_data
            return {} 

    # 创建协调器
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=async_update_data,
        update_interval=timedelta(seconds=UPDATE_INTERVAL),
    )

    # 首次刷新 (忽略错误)
    try:
        await coordinator.async_config_entry_first_refresh()
    except Exception:
        pass

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