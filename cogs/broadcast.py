import discord
from discord.ext import commands
from config import ALT_SOURCE_CHANNEL_ID, ALT_TARGET_CHANNEL_ID, ALWAYS_PING_ROLE_ID
from utils import sanitize_mentions

class Broadcast(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        if message.channel.id != ALT_SOURCE_CHANNEL_ID:
            return
        if not message.content.startswith("!broadcast"):
            return

        content = message.content[len("!broadcast"):].strip()
        if not content and not message.attachments:
            return

        # admin check
        is_admin = (
            message.guild
            and message.guild.get_member(message.author.id)
            and message.author.guild_permissions.administrator
        )

        content = sanitize_mentions(content, is_admin)
        if content and not (content.startswith("**") and content.endswith("**")):
            content = f"**{content}**"

        embed = discord.Embed(
            description=content or "*No text provided*",
            color=discord.Color.red(),
            timestamp=message.created_at
        )
        embed.set_footer(
            text=f"Sent by {message.author.display_name}",
            icon_url=self.bot.user.display_avatar.url
        )

        # embed first image, if any
        for att in message.attachments:
            if att.filename.lower().endswith((".png",".jpg",".jpeg",".gif",".webp")):
                embed.set_image(url=att.url)
                break

        target = self.bot.get_channel(ALT_TARGET_CHANNEL_ID)
        if not target:
            return

        # build allowed_mentions and mention text
        allowed = discord.AllowedMentions(everyone=is_admin, roles=is_admin, users=False)
        mentions = []
        if is_admin:
            role = message.guild.get_role(ALWAYS_PING_ROLE_ID)
            if role:
                mentions.append(role.mention)
            mentions += [r.mention for r in message.role_mentions]

        await target.send(
            content=" ".join(set(mentions)),
            embed=embed,
            allowed_mentions=allowed
        )

def setup(bot):
    bot.add_cog(Broadcast(bot))
