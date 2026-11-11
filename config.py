"""Shared settings, loaded from the .env file (never commit .env)."""
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# Add more routers here later, e.g. "R2": {...}
ROUTERS = {
    "R1": {
        "device_type": "cisco_ios",
        "host": os.getenv("R1_HOST"),
        "username": os.getenv("R1_USERNAME"),
        "password": os.getenv("R1_PASSWORD"),
    }
}
