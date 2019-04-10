from cogs.music3 import Music
#from cogs.databases import Database
from discord.ext import commands
import discord

TOKEN = 'NDkxNDA3MzU4ODIwNDgzMDc0.XKdMbA.AyThgC1HJmCOawRAzBKn2kaj0Gw'

client = discord.Client()

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   description='Learning Bot')


@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')


bot.add_cog(Music(bot))

bot.run(TOKEN)
