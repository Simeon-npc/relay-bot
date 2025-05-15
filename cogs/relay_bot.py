import discord
from discord.ext import commands
from config import SOURCE_CHANNEL_ID, TARGET_CHANNEL_ID

class RelayBotMessages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # ignore our own messages
        if message.author == self.bot.user:
            return

        if message.channel.id == SOURCE_CHANNEL_ID and message.author.bot:
            target = self.bot.get_channel(TARGET_CHANNEL_ID)
            if not target:
                return

            if message.content.strip():
                await target.send(message.content)
            elif message.embeds:
                for embed in message.embeds:
                    await target.send(embed=embed)

def setup(bot):
    bot.add_cog(RelayBotMessages(bot))
