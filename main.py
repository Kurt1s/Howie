from cogs.music3 import Music
from cogs.databases import Database
from discord.ext import commands
import discord

#TOKEN = 'NTU3MDEyMTM4MDQ5NDA0OTI4.XMimiw.BlY32cpVB1NFMP8DYCZ3GgbWv2M'
TOKEN = 'NTU2MzAwMTA4Mjk2MjI0Nzg4.XLpCRg.CC4JN-Haw830aZbtGste6oTgNPs'

client = discord.Client()

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   description='Learning Bot')


@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')


bot.add_cog(Music(bot))
bot.add_cog(Database(bot))

bot.run(TOKEN)
