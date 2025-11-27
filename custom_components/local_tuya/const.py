"""Constants for Simple Local Tuya."""
DOMAIN = "simple_local_tuya"

CONF_DEVICE_ID = "device_id"
CONF_IP_ADDRESS = "ip_address"
CONF_LOCAL_KEY = "local_key"
CONF_VERSION = "version"

# 核心修改：改为 1 秒刷新，实现“实时”效果
UPDATE_INTERVAL = 1