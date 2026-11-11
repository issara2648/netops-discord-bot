"""Step 2: parse FastEthernet0/0 IP and status, then post an alert to Discord via webhook.

This script sends one alert each time it is run.
"""
import requests
from netmiko import ConnectHandler
from config import ROUTERS, DISCORD_WEBHOOK_URL

if not DISCORD_WEBHOOK_URL:
    raise SystemExit("Please set DISCORD_WEBHOOK_URL in your .env file.")

router_r1 = ROUTERS["R1"]

try:
    net_connect = ConnectHandler(**router_r1)
    output = net_connect.send_command("show ip interface brief")
    net_connect.disconnect()

    target_ip = "Unknown"
    target_status = "Unknown"

    for line in output.splitlines():
        if 'FastEthernet0/0' in line:
            parts = line.split()
            target_ip = parts[1]
            # Status can be one word ("up") or two ("administratively down"),
            # so join everything between the Method column and the Protocol column.
            target_status = " ".join(parts[4:-1])
            break

    message = (
        f"🚨 **Network Alert: R1** 🚨\n"
        f"**Port:** FastEthernet0/0\n"
        f"**IP:** {target_ip}\n"
        f"**Status:** {target_status.upper()}"
    )
    payload = {"content": message, "username": "NetOps Bot"}

    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    if response.status_code == 204:
        print("ส่งการแจ้งเตือนสำเร็จ!")
    else:
        print("ส่งไม่สำเร็จ, status code:", response.status_code)
except Exception as e:
    print("เกิดข้อผิดพลาด:", e)
