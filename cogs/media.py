import discord
from discord.ext import commands
from config import MEDIA_SOURCE_CHANNEL_ID, MEDIA_TARGET_CHANNEL_ID

class MediaLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file_types = (
            ".png",".jpg",".jpeg",".gif",".webp",
            ".mp4",".mov",".avi",".pdf",".docx",".zip"
        )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        if message.channel.id != MEDIA_SOURCE_CHANNEL_ID or not message.attachments:
            return

        valid = [a for a in message.attachments if a.filename.lower().endswith(self.file_types)]
        if not valid:
            return

        embed = discord.Embed(
            description=f"**This user (`{message.author.id}`) sent this:**",
            color=discord.Color.blurple(),
            timestamp=message.created_at
        )
        embed.set_footer(text="Media Forwarded", icon_url=self.bot.user.display_avatar.url)

        # show first image
        for a in valid:
            if a.filename.lower().endswith((".png",".jpg",".jpeg",".gif",".webp")):
                embed.set_image(url=a.url)
                break

        target = self.bot.get_channel(MEDIA_TARGET_CHANNEL_ID)
        if not target:
            return

        await target.send(embed=embed)
        # non-image files as separate messages
        for a in valid:
            if not a.filename.lower().endswith((".png",".jpg",".jpeg",".gif",".webp")):
                await target.send(a.url)

def setup(bot):
    bot.add_cog(MediaLogger(bot))
