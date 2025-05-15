import discord
from discord.ext import commands
import os
import re
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
SOURCE_CHANNEL_ID = int(os.getenv("SOURCE_CHANNEL_ID"))           # Bot logs
TARGET_CHANNEL_ID = int(os.getenv("TARGET_CHANNEL_ID"))
ALT_SOURCE_CHANNEL_ID = int(os.getenv("ALT_SOURCE_CHANNEL_ID"))   # User messages (!broadcast)
ALT_TARGET_CHANNEL_ID = int(os.getenv("ALT_TARGET_CHANNEL_ID"))
MEDIA_SOURCE_CHANNEL_ID = int(os.getenv("MEDIA_SOURCE_CHANNEL_ID"))
MEDIA_TARGET_CHANNEL_ID = int(os.getenv("MEDIA_TARGET_CHANNEL_ID"))

ALWAYS_PING_ROLE_ID = 1349566425857265665  # Always ping this role on !broadcast

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


def sanitize_mentions(text, allow_everyone_roles):
    if allow_everyone_roles:
        return text
    text = re.sub(r'@everyone', '@\u200beveryone', text)
    text = re.sub(r'<@&\d+>', '', text)
    return text


@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # 1. Relay bot messages from SOURCE_CHANNEL_ID automatically
    if message.channel.id == SOURCE_CHANNEL_ID and message.author.bot:
        target_channel = bot.get_channel(TARGET_CHANNEL_ID)
        if target_channel:
            if message.content.strip():
                await target_channel.send(message.content)
            elif message.embeds:
                for embed in message.embeds:
                    await target_channel.send(embed=embed)

    # 2. Relay user !broadcast messages from ALT_SOURCE_CHANNEL_ID
    elif message.channel.id == ALT_SOURCE_CHANNEL_ID and message.content.startswith("!broadcast"):
        content = message.content[len("!broadcast"):].strip()
        if not content and not message.attachments:
            return

        is_admin = False
        if message.guild:
            member = message.guild.get_member(message.author.id)
            if member and member.guild_permissions.administrator:
                is_admin = True

        content = sanitize_mentions(content, is_admin)

        if content and not (content.startswith("**") and content.endswith("**")):
            content = f"**{content}**"

        embed = discord.Embed(
            description=content or "*No text provided*",
            color=discord.Color.red(),
            timestamp=message.created_at
        )
        embed.set_footer(text=f"Sent by {message.author.display_name}", icon_url=bot.user.display_avatar.url)

        for attachment in message.attachments:
            if attachment.filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp")):
                embed.set_image(url=attachment.url)
                break

        alt_target_channel = bot.get_channel(ALT_TARGET_CHANNEL_ID)
        if alt_target_channel:
            allowed_mentions = discord.AllowedMentions(
                everyone=is_admin,
                roles=is_admin,
                users=False
            )

            mention_text_parts = []
            if is_admin:
                role = message.guild.get_role(ALWAYS_PING_ROLE_ID)
                if role:
                    mention_text_parts.append(role.mention)
                mention_text_parts.extend(mention.mention for mention in message.role_mentions)

            mention_text = " ".join(set(mention_text_parts))
            await alt_target_channel.send(content=mention_text, embed=embed, allowed_mentions=allowed_mentions)

    # 3. Media logging section
    elif message.channel.id == MEDIA_SOURCE_CHANNEL_ID and message.attachments:
        media_target = bot.get_channel(MEDIA_TARGET_CHANNEL_ID)
        if media_target:
            file_types = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".mp4", ".mov", ".avi", ".pdf", ".docx", ".zip")
            valid_attachments = [a for a in message.attachments if a.filename.lower().endswith(file_types)]

            if valid_attachments:
                embed = discord.Embed(
                    description=f"**This user (`{message.author.id}`) sent this:**",
                    color=discord.Color.blurple(),
                    timestamp=message.created_at
                )
                embed.set_footer(text="Media Forwarded", icon_url=bot.user.display_avatar.url)

                for attachment in valid_attachments:
                    if attachment.filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp")):
                        embed.set_image(url=attachment.url)
                        break

                await media_target.send(embed=embed)
                for file in valid_attachments:
                    if not file.filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp")):
                        await media_target.send(file.url)


bot.run(TOKEN)
