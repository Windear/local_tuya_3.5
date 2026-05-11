"""Constants for Simple Local Tuya."""
DOMAIN = "simple_local_tuya"

CONF_DEVICE_ID = "device_id"
CONF_IP_ADDRESS = "ip_address"
CONF_LOCAL_KEY = "local_key"
CONF_VERSION = "version"

FAST_UPDATE_INTERVAL = 1     # 极速模式：1秒轮询
SLOW_UPDATE_INTERVAL = 10    # 正常模式：10秒轮询
FAST_MODE_TIMEOUT = 180      # 极速模式3分钟后自动关闭
