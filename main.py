from cogs.music3 import Music
#from cogs.databases import Database
from discord.ext import commands
import discord


TOKEN = 'NTU3MDEyMTM4MDQ5NDA0OTI4.XL-8AQ.aeYaFc22710ZSUCMAeqfxaDsyDE'

client = discord.Client()

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   description='Learning Bot')


@commands.command(aliases=["resume", "p"])
async def pause(self, ctx):
    """Pauses any currently playing audio."""
    client = ctx.guild.voice_client
    self._pause_audio(client)


def _pause_audio(self, client):
    if client.is_paused():
        client.resume()
    else:
        client.pause()

@bot.event
async def on_reaction_add(reaction, user):
    # ChID = '487165969903517696'
    # if reaction.message != ChID:
    #     print("")
    print("IN ON REACTION ADD")
    print(reaction)

    data = {react.emoji: react.count for react in reaction.message.reactions}
    print(data)

    #stores the number of pause reactions
    pauseplayCount = data.__getitem__("⏯")
    rewindCount = data.__getitem__("⏮")
    fastfowardCount = data.__getitem__("⏭")

    #pauses/plays if count > 1
    if pauseplayCount > 1:
        print("PAUSING")
        # _pause_audio(self, client)

    elif rewindCount > 1:
        print("REWINDING")g

    elif fastfowardCount > 1:
        print("SKIPPING")

@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')


bot.add_cog(Music(bot))

bot.run(TOKEN)
