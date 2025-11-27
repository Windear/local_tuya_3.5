from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

async def async_setup_entry(hass, entry, async_add_entities):
    # 返回空列表，彻底不创建任何开关实体
    # 之前创建的开关需要你删除集成重装才会消失
    async_add_entities([])