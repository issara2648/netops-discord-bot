"""Step 4: save the running-config to a timestamped .txt file."""
from netmiko import ConnectHandler
from datetime import datetime
from config import ROUTERS

router_r1 = ROUTERS["R1"]

try:
    net_connect = ConnectHandler(**router_r1)
    hostname = net_connect.find_prompt().strip('#')
    running_config = net_connect.send_command("show running-config")

    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{hostname}_backup_{now}.txt"

    with open(filename, 'w') as backup_file:
        backup_file.write(running_config)

    print(f"✅ แบ็คอัพสำเร็จ! บันทึกไฟล์ชื่อ: {filename}")
    net_connect.disconnect()
except Exception as e:
    print("เกิดข้อผิดพลาด:", e)
