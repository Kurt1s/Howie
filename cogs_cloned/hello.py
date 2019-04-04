from discord.ext import commands
import asyncio


bot = commands.Bot(command_prefix='!', description="Lance")

class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        msg = 'Hello {0.author.mention}'.format(ctx.message)
        await ctx.send(msg)
'''
    @commands.command()
    async def purge(self, ctx):
        def is_bot(message):
            return message.author == bot.user

        deleted = await ctx.channel.purge(limit=100, check=is_bot)
        #deleted = await ctx.purge_from(ctx.channel, limit=100, check=is_bot)
        await ctx.client.send_message(ctx.channel, 'Deleted {} message(s)'.format(len(deleted)))
'''