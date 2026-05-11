# Simple Local Tuya for Atorch/Juwei Energy Meter
# 简易本地涂鸦 - 炬为/Atorch 直流库仑计版

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![version](https://img.shields.io/badge/version-1.3.0-blue.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)]()

[English](#english) | [中文说明](#中文说明)

---

<a name="english"></a>
## 🇬🇧 English Description

A lightweight, dedicated Home Assistant custom component designed specifically for **Tuya-based Smart DC Coulometers/Energy Meters** (commonly branded as **Atorch** or **Juwei/炬为**).

This integration solves common issues found in the standard `LocalTuya` or official `Tuya` integrations when using these specific devices, such as lack of bi-directional current support, slow refresh rates, or Protocol 3.5 connection failures.

### ✨ Key Features

*   **Local Control**: Uses local TCP connections via `tinytuya`. No cloud dependence, no latency.
*   **Protocol 3.5 Support**: Optimized for newer devices using Tuya Protocol 3.4/3.5 which require persistent connections.
*   **Real-time Refresh**: Polls data every **1 second** for instant feedback.
*   **Bi-directional Support**: Correctly parses signed integers to show **negative values** for discharging Current and Power.
*   **Accurate Mapping**: Pre-configured entities for Voltage, Current, Power, Capacity (Ah), Energy (kWh), Temperature, and Battery %.
*   **Auto Reconnect**: Automatically retries on connection failure with built-in cache to prevent entity unavailability.
*   **Editable Config**: Modify IP, Device ID, Local Key anytime after setup via the Configure button.

### 📱 Supported Devices

Tested on:
*   **Atorch / Juwei (炬为) Smart DC Coulometer** (Tuya WiFi version).
*   *Likely compatible with other Tuya PRO 3.5 DC meters sharing similar DP IDs.*

### 🛠️ Installation

#### Method 1: HACS (Recommended)
1.  Open **HACS** in Home Assistant.
2.  Go to **Integrations** > click the 3 dots (top right) > **Custom repositories**.
3.  Add the URL of this repository: `https://github.com/Windear/local_tuya_3.5`
4.  Select **Integration** as the category.
5.  Search for **Simple Local Tuya (Protocol 3.5)** and click **Download**.
6.  Restart Home Assistant.

#### Method 2: Manual
1.  Download the `custom_components/local_tuya` folder from this repository.
2.  Copy it into your Home Assistant's `config/custom_components/` directory (the final path should be `config/custom_components/local_tuya/`).
3.  Restart Home Assistant.

### 🔑 How to Get Device ID and Local Key

You need both the **Device ID** and **Local Key** to connect. Here's how to get them:

#### Step 1: Register on Tuya IoT Platform
1.  Go to [iot.tuya.com](https://iot.tuya.com/) and register a developer account.
2.  Log in and go to **Cloud** → **Create Project** (choose "Smart Home" as the development type).
3.  In the project settings, link your **Tuya Smart** or **Smart Life** app account (the same account your device is bound to). This will sync your devices to the cloud project.

#### Step 2: Find Device ID
1.  In your project, go to **Devices** → **Device Management**.
2.  Find your coulometer in the list. The **Device ID** is displayed there.

#### Step 3: Find Local Key
1.  Click on your device in the device list.
2.  Click the **View** button (eye icon) next to the **Local Key** field.
3.  Copy the Local Key exactly as shown (it may contain special characters like `]`, `~`, `#`, etc.).

> **Important**: If you previously connected the device through another Tuya developer project, the Local Key may have changed. Always use the Local Key from the most recently created project.

#### Step 4: Find Device IP Address
1.  Check your router's admin page for the device IP (look for the device name or match the MAC address).
2.  Or use the Tuya Smart / Smart Life app → Device Info to find the IP.
3.  **Recommend**: Set a static IP on your router so the IP doesn't change after reboot.

### ⚙️ Configuration

1.  Go to **Settings** > **Devices & Services**.
2.  Click **Add Integration** (bottom right).
3.  Search for **炬为库伦计** or **Simple Local Tuya**.
4.  Enter the device details:
    *   **IP Address**: The local IP of your meter (e.g. `192.168.1.100`).
    *   **Device ID**: Obtained from Tuya IoT Platform.
    *   **Local Key**: Obtained from Tuya IoT Platform.
    *   **Protocol Version**: Default is `3.5`. Only change if you know your device uses a different version.
5.  Click Submit.

#### Editing Configuration After Setup
1.  Go to **Settings** > **Devices & Services**.
2.  Find the integration and click **Configure**.
3.  Modify IP, Device ID, Local Key, or Protocol Version as needed.
4.  Click Submit — the integration will automatically reload with the new settings.

### 📊 Entities

| Entity Name | Unit | Description |
| :--- | :--- | :--- |
| **Voltage** | V | Real-time voltage |
| **Current** | A | Real-time current (Negative = Discharging) |
| **Power** | W | Real-time power (Negative = Discharging) |
| **Battery Level** | % | Remaining battery percentage |
| **Remaining Capacity** | Ah | Remaining battery capacity |
| **Remaining Energy** | kWh | Remaining energy |
| **Total Charge** | Ah | Cumulative charge capacity |
| **Total Discharge** | Ah | Cumulative discharge capacity |
| **Meter Temp** | °C | Screen/System temperature |
| **Probe Temp** | °C | External probe temperature |

---

<a name="中文说明"></a>
## 🇨🇳 中文说明

这是一个专为 **涂鸦系直流智能库仑计/电能表**（常见品牌为 **炬为/Juwei** 或 **Atorch**）设计的 Home Assistant 自定义集成。

该集成解决了使用通用 `LocalTuya` 或官方 `Tuya` 集成连接此类设备时常见的问题，例如无法显示负电流（放电）、刷新速度慢、或协议 3.5 连接不稳定等。

### ✨ 功能亮点

*   **完全本地化**：基于 `tinytuya` 进行本地 TCP 直连。无需云端依赖，无延迟。
*   **支持协议 3.5**：专为使用涂鸦协议 3.4/3.5 的新款设备优化，支持长连接保活。
*   **秒级刷新**：数据更新频率为 **1秒**，实现真正的实时监控。
*   **双向电流支持**：内置 32位补码转换逻辑，正确显示充电（正数）和放电（负数）的 **电流** 与 **功率**。
*   **精准映射**：已预先配置好电压、电流、功率、容量 (Ah)、电量 (kWh)、温度、电量百分比等实体，无需手动映射 DP ID。
*   **修复单位报错**：修复了 Ah 单位导致的 HA 日志报错问题。
*   **自动重连**：连接失败时自动重试，内置数据缓存防止实体变为不可用状态。
*   **可编辑配置**：添加集成后随时可以修改 IP、Device ID、Local Key 等参数。

### 📱 支持设备

已测试设备：
*   **炬为 (Juwei) / Atorch 智能直流库仑计** (涂鸦 WiFi 版)
*   *理论上支持其他采用类似 DP 定义的涂鸦 Pro 3.5 直流电表。*

### 🛠️ 安装方法

#### 方法 1: 使用 HACS (推荐)
1.  打开 Home Assistant 中的 **HACS**。
2.  点击 **集成 (Integrations)** > 右上角三个点 > **自定义存储库 (Custom repositories)**。
3.  输入本项目地址：`https://github.com/Windear/local_tuya_3.5`
4.  类别选择 **集成 (Integration)**。
5.  搜索 **炬为库伦计** 或 **Simple Local Tuya** 并点击下载。
6.  重启 Home Assistant。

#### 方法 2: 手动安装
1.  下载本仓库中的 `custom_components/local_tuya` 文件夹。
2.  将其复制到 Home Assistant 配置目录下的 `config/custom_components/` 中（最终路径应为 `config/custom_components/local_tuya/`）。
3.  重启 Home Assistant。

### 🔑 如何获取 Device ID 和 Local Key

连接设备需要 **Device ID（设备ID）** 和 **Local Key（本地密钥）**，获取步骤如下：

#### 第一步：注册涂鸦 IoT 平台
1.  访问 [iot.tuya.com](https://iot.tuya.com/)，注册一个开发者账号。
2.  登录后进入 **云开发** → **创建项目**（开发方式选择"智能生活"）。
3.  在项目设置中，关联你的 **涂鸦智能** 或 **智能生活** App 账号（即设备绑定的账号），这会将你的设备同步到云端项目。

#### 第二步：获取 Device ID
1.  在项目中进入 **设备** → **设备管理**。
2.  在设备列表中找到你的库仑计，**Device ID** 就显示在设备信息中。

#### 第三步：获取 Local Key(AI生成，如有出入，请自己百度搜索相关操作内容步骤)
1.  在设备列表中点击你的设备。
2.  点击 **Local Key** 字段旁边的 **查看** 按钮（眼睛图标）。
3.  **完整复制** Local Key 的值（注意：可能包含 `]`、`~`、`#` 等特殊字符，请务必完整复制，不要遗漏）。

> **重要提示**：如果你之前在其他涂鸦开发者项目中接入过该设备，Local Key 可能已经变更。请始终使用 **最新创建的项目** 中的 Local Key。

#### 第四步：获取设备 IP 地址
1.  登录路由器管理页面，查找设备列表中的库仑计 IP（可通过设备名称或 MAC 地址识别）。
2.  也可以在涂鸦智能 / 智能生活 App 中查看设备信息获取 IP。
3.  **强烈建议**：在路由器中为库仑计设置静态 IP，避免重启后 IP 变化导致连接失败。

### ⚙️ 配置指南

1.  进入 **配置** > **设备与服务**。
2.  点击右下角 **添加集成**。
3.  搜索 **炬为库伦计** 或 **Simple Local Tuya**。
4.  填入设备信息：
    *   **IP 地址 (IP Address)**：设备的局域网 IP（例如 `192.168.50.54`）。
    *   **设备 ID (Device ID)**：从涂鸦 IoT 平台获取。
    *   **本地密钥 (Local Key)**：从涂鸦 IoT 平台获取（注意完整复制特殊字符）。
    *   **协议版本**：默认为 `3.5`，除非你确认设备使用其他版本，否则不要修改。
5.  点击提交。

#### 添加后修改配置
1.  进入 **配置** > **设备与服务**。
2.  找到已添加的集成，点击 **配置** 按钮。
3.  修改 IP、Device ID、Local Key 或协议版本。
4.  点击提交，集成会自动重载并使用新配置。

### 📊 包含实体

| 实体名称 | 单位 | 说明 |
| :--- | :--- | :--- |
| **当前电压** | V | 实时电压 |
| **当前电流** | A | 实时电流 (负数代表放电) |
| **当前功率** | W | 实时功率 (负数代表放电) |
| **电池百分比** | % | 剩余电量百分比 |
| **剩余容量** | Ah | 电池剩余容量 |
| **剩余电量** | kWh | 电池剩余能量 |
| **累计充电容量** | Ah | 累计统计数据 |
| **累计放电容量** | Ah | 累计统计数据 |
| **仪表温度** | °C | 屏幕/系统温度 |
| **探头温度** | °C | 外置探头温度 |

### ❓ 常见问题

**Q: 实体全部显示"未知"怎么办？**
- 检查 IP 地址是否正确，设备是否在线（在路由器中确认设备连通）。
- 检查 Device ID 和 Local Key 是否正确复制（特别注意特殊字符，如 `]`、`~`、`#`）。
- 确保 HA 和库仑计在同一局域网内。
- 查看 HA 日志（配置 → 系统 → 日志）中的具体错误信息。

**Q: 设备重启后 IP 变了，连接不上怎么办？**
- 在路由器中为库仑计设置静态 IP 绑定。
- 然后在 HA 集成中点击"配置"修改 IP 地址即可，无需删除重建。

**Q: 电流/功率显示为负数正常吗？**
- 正常。负数表示电池正在放电，正数表示正在充电。这是双向电流的正确表现。

**Q: Local Key 从哪里获取？**
- 参见上方 [如何获取 Device ID 和 Local Key](#-如何获取-device-id-和-local-key) 章节。

---

## ☕ Support

If you find this integration useful, please consider starring the repository!
如果您觉得这个插件好用，欢迎点个 Star！

## 📄 License

MIT License
