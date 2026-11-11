"""Step 5: ChatOps Discord bot. Check status and back up routers from chat.

Commands:
    !status <router>   show ip interface brief
    !backup <router>   send the running-config as a .txt file
"""
import discord
from discord.ext import commands
from netmiko import ConnectHandler
from datetime import datetime
from config import ROUTERS, DISCORD_TOKEN

if not DISCORD_TOKEN:
    raise SystemExit("Please set DISCORD_TOKEN in your .env file.")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'✅ บอท {bot.user.name} ออนไลน์พร้อมลุย!')


@bot.command()
async def status(ctx, router_name: str):
    router_name = router_name.upper()
    if router_name not in ROUTERS:
        await ctx.send(f"❌ ไม่พบอุปกรณ์ชื่อ `{router_name}`")
        return

    await ctx.send(f"⏳ กำลังตรวจสอบสถานะของ `{router_name}`...")
    try:
        net_connect = ConnectHandler(**ROUTERS[router_name])
        output = net_connect.send_command("show ip interface brief")
        net_connect.disconnect()
        await ctx.send(f"📊 **Network Status: {router_name}** 📊\n```text\n{output}\n```")
    except Exception as e:
        await ctx.send(f"⚠️ เกิดข้อผิดพลาด: `{e}`")


@bot.command()
async def backup(ctx, router_name: str):
    router_name = router_name.upper()
    if router_name not in ROUTERS:
        await ctx.send(f"❌ ไม่พบอุปกรณ์ชื่อ `{router_name}`")
        return

    await ctx.send(f"⏳ กำลังดึง Running Config จาก `{router_name}` รอสักครู่นะครับ...")
    try:
        net_connect = ConnectHandler(**ROUTERS[router_name])
        hostname = net_connect.find_prompt().strip('#')
        output = net_connect.send_command("show running-config")
        net_connect.disconnect()

        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{hostname}_backup_{now}.txt"
        with open(filename, 'w') as f:
            f.write(output)

        await ctx.send(
            f"✅ สำรองข้อมูลสำเร็จ! ดาวน์โหลดไฟล์ Config ของ `{router_name}` ได้เลยครับ",
            file=discord.File(filename),
        )
    except Exception as e:
        await ctx.send(f"⚠️ เกิดข้อผิดพลาด: `{e}`")


bot.run(DISCORD_TOKEN)
