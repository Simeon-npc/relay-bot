import discord
from discord.ext import commands
import config

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# load each cog by module path
for cog in ("cogs.relay_bot", "cogs.broadcast", "cogs.media"):
    bot.load_extension(cog)

@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")

bot.run(config.TOKEN)
