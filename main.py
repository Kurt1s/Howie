import discord
from cogs.music import Music
from cogs.hello import Hello
from discord.ext import commands


TOKEN = 'NDkxNDA3MzU4ODIwNDgzMDc0.D3CBHQ.9AmTEccwmjqcOSd-94CZKkB-H5g'

client = discord.Client()

#
# @client.event
# async def on_message(message):
#     # we do not want the bot to reply to itself
#     if message.author == client.user:
#         return
#
#     if message.content.startswith('!hello'):
#         msg = 'Hello {0.author.mention}'.format(message)
#         await client.send_message(message.channel, msg)


bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   description='Learning Bot')
@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')


bot.add_cog(Music(bot))
bot.add_cog(Hello(bot))
bot.run(TOKEN)