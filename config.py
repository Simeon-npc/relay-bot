import os
from dotenv import load_dotenv

load_dotenv()

TOKEN                  = os.getenv("DISCORD_TOKEN")
SOURCE_CHANNEL_ID      = int(os.getenv("SOURCE_CHANNEL_ID"))
TARGET_CHANNEL_ID      = int(os.getenv("TARGET_CHANNEL_ID"))
ALT_SOURCE_CHANNEL_ID  = int(os.getenv("ALT_SOURCE_CHANNEL_ID"))
ALT_TARGET_CHANNEL_ID  = int(os.getenv("ALT_TARGET_CHANNEL_ID"))
MEDIA_SOURCE_CHANNEL_ID= int(os.getenv("MEDIA_SOURCE_CHANNEL_ID"))
MEDIA_TARGET_CHANNEL_ID= int(os.getenv("MEDIA_TARGET_CHANNEL_ID"))

# This role is always pinged on !broadcast by admins
ALWAYS_PING_ROLE_ID    = 1349566425857265665
