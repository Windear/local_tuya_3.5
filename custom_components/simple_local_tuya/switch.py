import time as time_module
from datetime import timedelta
from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.event import async_track_time_interval
from .const import DOMAIN, FAST_UPDATE_INTERVAL, SLOW_UPDATE_INTERVAL, FAST_MODE_TIMEOUT


async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    device = data["device"]
    async_add_entities([FastRefreshSwitch(hass, coordinator, device, entry.title)])


class FastRefreshSwitch(SwitchEntity):
    _attr_name = "极速刷新"
    _attr_has_entity_name = True
    _attr_icon = "mdi:speedometer"

    def __init__(self, hass, coordinator, device, entry_title):
        self._hass = hass
        self._coordinator = coordinator
        self._device = device
        self._entry_title = entry_title
        self._attr_unique_id = f"{device.id}_fast_refresh"
        self._fast_unsub = None
        self._auto_off_handle = None

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self._device.id)},
            name=self._entry_title,
            manufacturer="Tuya (Local)",
            model="智能库仑计 (Pro 3.5)",
        )

    @property
    def is_on(self):
        return self._fast_unsub is not None

    async def _fast_refresh(self, _now=None):
        """极速模式：1秒读取 + 直接推送数据"""
        def _read():
            result = self._device.status()
            if 'Error' in result:
                try:
                    self._device.close()
                except Exception:
                    pass
                time_module.sleep(0.3)
                result = self._device.status()
            return result

        try:
            data = await self._hass.async_add_executor_job(_read)
            if 'dps' in data:
                merged = dict(self._coordinator.data or {})
                for k, v in data['dps'].items():
                    if v is not None:
                        merged[k] = v
                self._coordinator.async_set_updated_data(merged)
        except Exception:
            pass

    async def async_turn_on(self, **kwargs):
        # 1. 通知设备开启极速上报
        def _enable():
            return self._device.set_value(101, True)
        try:
            await self._hass.async_add_executor_job(_enable)
        except Exception:
            pass

        # 2. 启动1秒轮询定时器
        self._fast_unsub = async_track_time_interval(
            self._hass,
            self._fast_refresh,
            timedelta(seconds=FAST_UPDATE_INTERVAL),
        )
        await self._fast_refresh()

        # 3. 3分钟自动关闭
        self._schedule_auto_off()
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        # 1. 停止1秒轮询
        self._cancel_fast_refresh()
        self._cancel_auto_off()

        # 2. 通知设备关闭极速上报
        def _disable():
            return self._device.set_value(101, False)
        try:
            await self._hass.async_add_executor_job(_disable)
        except Exception:
            pass

        # 3. 恢复正常轮询
        self._coordinator.update_interval = timedelta(seconds=SLOW_UPDATE_INTERVAL)
        await self._coordinator.async_request_refresh()
        self.async_write_ha_state()

    def _cancel_fast_refresh(self):
        if self._fast_unsub is not None:
            self._fast_unsub()
            self._fast_unsub = None

    def _schedule_auto_off(self):
        self._cancel_auto_off()
        self._auto_off_handle = self._hass.loop.call_later(
            FAST_MODE_TIMEOUT,
            lambda: self._hass.async_create_task(self._auto_turn_off()),
        )

    def _cancel_auto_off(self):
        if self._auto_off_handle is not None:
            self._auto_off_handle.cancel()
            self._auto_off_handle = None

    async def _auto_turn_off(self):
        if self.is_on:
            await self.async_turn_off()

    async def async_will_remove_from_hass(self):
        self._cancel_fast_refresh()
        self._cancel_auto_off()
