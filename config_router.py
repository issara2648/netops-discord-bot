"""Step 3: push configuration commands to the router and save to startup-config."""
from netmiko import ConnectHandler
from config import ROUTERS

router_r1 = ROUTERS["R1"]

config_commands = [
    'interface Loopback 0',
    'ip address 10.1.1.1 255.255.255.255',
    'description Configured_by_Python_Netmiko',
    'no shutdown'
]

try:
    net_connect = ConnectHandler(**router_r1)
    output = net_connect.send_config_set(config_commands)
    print(output)

    net_connect.save_config()
    print("\n✅ บันทึกการตั้งค่าลง Startup Config เรียบร้อย!")

    net_connect.disconnect()
except Exception as e:
    print("เกิดข้อผิดพลาด:", e)
