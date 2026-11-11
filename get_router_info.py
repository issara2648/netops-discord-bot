"""Step 1: connect to a Cisco router over SSH (Netmiko) and read interface status."""
from netmiko import ConnectHandler
from config import ROUTERS

router_r1 = ROUTERS["R1"]

print("กำลังเชื่อมต่อไปที่ Router...")
try:
    net_connect = ConnectHandler(**router_r1)
    print("เชื่อมต่อสำเร็จ!\n")

    output = net_connect.send_command("show ip interface brief")
    print("--- ผลลัพธ์จากคำสั่ง show ip interface brief ---")
    print(output)

    net_connect.disconnect()
    print("\nปิดการเชื่อมต่อเรียบร้อยแล้ว")
except Exception as e:
    print("เกิดข้อผิดพลาด:", e)
