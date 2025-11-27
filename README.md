# Simple Local Tuya for Atorch/Juwei Energy Meter
# 简易本地涂鸦 - 炬为/Atorch 直流库仑计版

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![version](https://img.shields.io/badge/version-1.0.0-blue.svg)]()
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
*   **Auto Fast-Refresh**: Automatically sends the "Fast Refresh" command (DP 101) in the background to ensure high-speed data updates, while keeping the UI clean (no toggle switches shown).
*   **Bi-directional Support**: Correctly parses signed integers to show **negative values** for discharging Current and Power.
*   **Accurate Mapping**: Pre-configured entities for Voltage, Current, Power, Capacity (Ah), Energy (kWh), Temperature, and Battery %.

### 📱 Supported Devices

Tested on:
*   **Atorch / Juwei (炬为) Smart DC Coulometer** (Tuya WiFi version).
*   *Likely compatible with other Tuya PRO 3.5 DC meters sharing similar DP IDs.*

### 🛠️ Installation

#### Method 1: HACS (Recommended)
1.  Open **HACS** in Home Assistant.
2.  Go to **Integrations** > click the 3 dots (top right) > **Custom repositories**.
3.  Add the URL of this repository: `https://github.com/Windear/local_tuya_3.5` (Replace with your actual repo URL).
4.  Select **Integration** as the category.
5.  Search for **Simple Local Tuya (Protocol 3.5)** and click **Download**.
6.  Restart Home Assistant.

#### Method 2: Manual
1.  Download the `custom_components` folder from this repository.
2.  Copy the `simple_local_tuya` folder into your Home Assistant's `config/custom_components/` directory.
3.  Restart Home Assistant.

### ⚙️ Configuration

1.  Go to **Settings** > **Devices & Services**.
2.  Click **Add Integration** (bottom right).
3.  Search for **Simple Local Tuya (Protocol 3.5)**.
4.  Enter the device details:
    *   **IP Address**: The local IP of your meter (Static IP recommended).
    *   **Device ID**: Obtained from Tuya IoT Platform.
    *   **Local Key**: Obtained from Tuya IoT Platform.
    *   **Protocol Version**: Default is `3.5`.
5.  Click Submit.

> **Note**: To find your `Device ID` and `Local Key`, you need to register a developer account on [iot.tuya.com](https://iot.tuya.com/) and link your Tuya Smart/Smart Life app account.

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
*   **自动极速模式**：后台自动发送指令开启设备的“极速数据刷新”模式 (DP 101)，并在前端隐藏开关，防止误触导致数据卡死。
*   **双向电流支持**：内置 32位补码转换逻辑，正确显示充电（正数）和放电（负数）的 **电流** 与 **功率**。
*   **精准映射**：已预先配置好电压、电流、功率、容量 (Ah)、电量 (kWh)、温度、电量百分比等实体，无需手动映射 DP ID。
*   **修复单位报错**：修复了 Ah 单位导致的 HA 日志报错问题。

### 📱 支持设备

已测试设备：
*   **炬为 (Juwei) / Atorch 智能直流库仑计** (涂鸦 WiFi 版)
*   *理论上支持其他采用类似 DP 定义的涂鸦 Pro 3.5 直流电表。*

### 🛠️ 安装方法

#### 方法 1: 使用 HACS (推荐)
1.  打开 Home Assistant 中的 **HACS**。
2.  点击 **集成 (Integrations)** > 右上角三个点 > **自定义存储库 (Custom repositories)**。
3.  输入本项目地址：`https://github.com/Windear/local_tuya_3.5` (请替换为您实际的仓库地址)。
4.  类别选择 **集成 (Integration)**。
5.  搜索 **Simple Local Tuya (Protocol 3.5)** 并点击下载。
6.  重启 Home Assistant。

#### 方法 2: 手动安装
1.  下载本仓库中的 `custom_components` 文件夹。
2.  将 `simple_local_tuya` 文件夹复制到您的 Home Assistant 配置目录下的 `config/custom_components/` 中。
3.  重启 Home Assistant。

### ⚙️ 配置指南

1.  进入 **配置** > **设备与服务**。
2.  点击右下角 **添加集成**。
3.  搜索 **Simple Local Tuya (Protocol 3.5)**。
4.  填入设备信息：
    *   **IP 地址 (IP Address)**：设备的局域网 IP（建议在路由器设置静态 IP）。
    *   **设备 ID (Device ID)**：从涂鸦 IoT 平台获取。
    *   **本地密钥 (Local Key)**：从涂鸦 IoT 平台获取。
    *   **协议版本**: 默认为 `3.5`。
5.  点击提交。

> **提示**：要获取 `Device ID` 和 `Local Key`，您需要在 [涂鸦 IoT 平台](https://iot.tuya.com/) 注册开发者账号，并关联您的 涂鸦智能/智能生活 App 账号。

### 📊 包含实体

| 实体名称 | 单位 | 说明 |
| :--- | :--- | :--- |
| **当前电压** | V | 实时电压 |
| **当前电流** | A | 实时电流 (负数代表放电) |
| **当前功率** | W | 实时功率 (负数代表放电) |
| **电池百分比** | % | 剩余电量百分比 |
| **剩余容量** | Ah | 电池剩余容量 |
| **剩余电量** | kWh | 电池剩余能量 |
| **累计充电容量** | Ah | 统计数据 |
| **累计放电容量** | Ah | 统计数据 |
| **仪表温度** | °C | 屏幕/系统温度 |
| **探头温度** | °C | 外置探头温度 |

---

## ☕ Support

If you find this integration useful, please consider starring the repository!
如果您觉得这个插件好用，欢迎点个 Star！

## 📄 License

MIT License