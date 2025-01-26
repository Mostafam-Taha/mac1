import os
import platform
import psutil
import uuid
import socket
import re
from datetime import datetime

def get_wifi_mac():
    """Get the MAC address of the Wi-Fi interface."""
    try:
        result = os.popen("ipconfig /all").read()  # For Windows
        wifi_mac = re.search(r"Wireless LAN adapter.*?Physical Address[ .]*: ([\w\-]*)", result, re.S)
        if wifi_mac:
            return wifi_mac.group(1)
        else:
            return "Wi-Fi MAC Address not found"
    except Exception as e:
        return f"Error: {e}"

def get_device_mac():
    """Get the MAC address of the device."""
    mac = hex(uuid.getnode()).replace("0x", "").upper()
    return ":".join(mac[i:i+2] for i in range(0, len(mac), 2))

def get_system_info():
    """Get basic system information."""
    system_info = {
        "System": platform.system(),
        "Node Name": platform.node(),
        "Release": platform.release(),
        "Version": platform.version(),
        "Machine": platform.machine(),
        "Processor": platform.processor(),
        "CPU Count": psutil.cpu_count(logical=False),  # Physical cores
        "Logical CPU Count": psutil.cpu_count(logical=True),  # Logical cores
        "CPU Frequency": psutil.cpu_freq().current,  # CPU Frequency in MHz
        "Total Memory": round(psutil.virtual_memory().total / (1024 * 1024 * 1024), 2),  # in GB
        "Available Memory": round(psutil.virtual_memory().available / (1024 * 1024 * 1024), 2),  # in GB
        "Used Memory": round(psutil.virtual_memory().used / (1024 * 1024 * 1024), 2),  # in GB
        "Memory Percentage": psutil.virtual_memory().percent,
        "Disk Usage": psutil.disk_usage('/').percent,
        "Battery Status": psutil.sensors_battery(),
        "Network Name": socket.gethostname(),
        "IP Address": socket.gethostbyname(socket.gethostname()),
        "MAC Address": get_device_mac(),
        "Wi-Fi MAC Address": get_wifi_mac(),
        "Boot Time": datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"),
        "Current Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Uptime": str(datetime.now() - datetime.fromtimestamp(psutil.boot_time())).split('.')[0],
        "Processes Count": len(psutil.pids()),
        "Disk Partitions": psutil.disk_partitions(),
        "Disk Usage on Root": psutil.disk_usage('/').percent,
        "Network Stats": psutil.net_if_addrs(),
        "Active Connections": len(psutil.net_connections())
    }
    return system_info

# Display all system information
system_info = get_system_info()
for key, value in system_info.items():
    print(f"{key}: {value}")
