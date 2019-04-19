from cogs.music3 import Music
#from cogs.databases import Database
from discord.ext import commands
import discord

TOKEN = 'NTU3MDEyMTM4MDQ5NDA0OTI4.XLk3PA.DGPCm21WO7rtUseO4HjnwY1yRqI'

client = discord.Client()

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   description='Learning Bot')


@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')


bot.add_cog(Music(bot))

bot.run(TOKEN)
