import discord
import requests
from babel.numbers import format_currency


TOKEN = 'NTU3MDEyMTM4MDQ5NDA0OTI4.D3CFxQ.llBOmngDv4c0FHeJQffsM4RcKUA'

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

    # if message.content.startswith('!play'):
    #     msg = 'Ok I will play some music for you'.format(message)
    #     await client.send_message(message.channel, msg)

    # Kurtis
    if message.content.startswith('!info'):
        info = client.application_info()
        msg = info
        await client.send_message(message.channel, msg)

    # Kurtis
    if message.content.startswith('!321'):
        await client.send_message(message.channel, "3\n2\n1\nTime's up!", tts=True)

    # Kurtis
    if message.content.startswith('!quote'):
        url = "http://www.forbes.com/forbesapi/thought/uri.json?enrich=true&query=1&relatedlimit=5"
        response = requests.get(url)
        data = response.json()
        quote = data['thought']["quote"]

        await client.send_message(message.channel, quote.format(message), tts=True)

    # Kurtis
    if message.content.startswith('!btc'):
        url = "https://api.coindesk.com/v1/bpi/currentprice.json"
        response = requests.get(url)
        data = response.json()
        price = data['bpi']['USD']['rate']
        # format_currency(float(price), 'USD', locale='en_US')
        await client.send_message(message.channel, price, tts=True)


    # Kurtis
    if message.content.startswith('!eth'):
        url = "https://api.coinmarketcap.com/v1/ticker/ethereum/"
        response = requests.get(url)
        data = response.json()
        price = data[0]['price_usd']
        # format_currency(float(price), 'USD', locale='en_US')
        await client.send_message(message.channel, price, tts=True)




@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)