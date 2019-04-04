import discord
from cogs.music import Music
from cogs.hello import Hello
from cogs.databases import Database
from discord.ext import commands


TOKEN = 'NTU3MDEyMTM4MDQ5NDA0OTI4.D31Nbw.ugjav9y2vr7YvFF2tA4hRxc2Sy0'
client = discord.Client()


bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   description='Learning Bot')
@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')


bot.add_cog(Music(bot))
bot.add_cog(Hello(bot))
bot.add_cog(Database(bot))
bot.run(TOKEN)
