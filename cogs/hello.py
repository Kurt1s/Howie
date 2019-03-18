from discord.ext import commands


class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @commands.command()
        async def hello(self, ctx, message):
            # we do not want the bot to reply to itself
            if message.author == ctx.client.user:
                return

            if message.content.startswith('!hello'):
                msg = 'Hello {0.author.mention}'.format(message)
                await ctx.client.send_message(message.channel, msg)
