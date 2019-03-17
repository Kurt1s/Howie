import discord

TOKEN = 'NDkxNDA3MzU4ODIwNDgzMDc0.D3A1gg.2phYPvETPzMs4smj2CqO9X5Avl4'

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!goodbye'):
        msg = 'Goodbye {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!play'):
        msg = 'Ok I will play some music for you'.format(message)
        await client.send_message(message.channel,msg)
        await client.send_typing(message.channel,msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)