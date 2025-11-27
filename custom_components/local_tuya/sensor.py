from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN

# --- 严格配置表 ---
KNOWN_DPS_CONFIG = {
    # 电力参数 (signed=True)
    "20": {"name": "当前电压", "class": SensorDeviceClass.VOLTAGE, "unit": "V", "scaling": 0.01, "icon": "mdi:lightning-bolt"},
    "18": {"name": "当前电流", "class": SensorDeviceClass.CURRENT, "unit": "A", "scaling": 0.001, "icon": "mdi:current-ac", "signed": True},
    "19": {"name": "当前功率", "class": SensorDeviceClass.POWER, "unit": "W", "scaling": 0.01, "icon": "mdi:flash", "signed": True},
    
    # 电池 (ID 103)
    "103": {"name": "电池百分比", "class": SensorDeviceClass.BATTERY, "unit": "%", "scaling": 0.1, "icon": "mdi:battery-70"},
    
    # 容量 (无class避免Ah报错)
    "126": {"name": "累计充电容量", "unit": "Ah", "scaling": 0.001, "state_class": SensorStateClass.TOTAL_INCREASING, "icon": "mdi:battery-plus"},
    "127": {"name": "累计放电容量", "unit": "Ah", "scaling": 0.001, "state_class": SensorStateClass.TOTAL_INCREASING, "icon": "mdi:battery-minus"},
    "133": {"name": "剩余容量", "unit": "Ah", "scaling": 0.001, "icon": "mdi:battery-high"},
    
    # 电量 (kWh)
    "123": {"name": "剩余电量", "class": SensorDeviceClass.ENERGY, "unit": "kWh", "scaling": 1, "icon": "mdi:battery-charging-100"},
    
    # 温度 (ID 122 探头, ID 135 仪表)
    "122": {"name": "探头温度", "class": SensorDeviceClass.TEMPERATURE, "unit": "°C", "scaling": 0.1, "icon": "mdi:thermometer"},
    "135": {"name": "仪表温度", "class": SensorDeviceClass.TEMPERATURE, "unit": "°C", "scaling": 1, "icon": "mdi:chip"},
}

async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    device = data["device"]
    
    sensors = []
    
    # 强制创建这10个传感器
    for dps_id, config in KNOWN_DPS_CONFIG.items():
        sensors.append(TuyaLocalSensor(coordinator, device, entry.title, dps_id, config))
    
    async_add_entities(sensors)

class TuyaLocalSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, device, entry_title, dps_id, config):
        super().__init__(coordinator)
        self._device = device
        self._entry_title = entry_title
        self._dps_id = dps_id
        self._config = config
        
        self._attr_name = config['name']
        self._attr_has_entity_name = True
        self._attr_unique_id = f"{device.id}_{dps_id}"
        self._attr_device_class = config.get("class")
        self._attr_native_unit_of_measurement = config.get("unit")
        self._attr_icon = config.get("icon")
        self._attr_state_class = config.get("state_class", SensorStateClass.MEASUREMENT)

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self._device.id)},
            name=self._entry_title,
            manufacturer="Tuya (Local)",
            model="智能库仑计 (Pro 3.5)",
        )

    def _get_signed_value(self, value):
        try:
            val = int(value)
            if val > 2147483647:
                val -= 4294967296
            return val
        except:
            return value

    @property
    def native_value(self):
        raw = self.coordinator.data.get(self._dps_id)
        if raw is None: return None
        try:
            if self._config.get("signed"):
                raw = self._get_signed_value(raw)
            return float(raw) * self._config.get("scaling", 1)
        except (ValueError, TypeError):
            return raw