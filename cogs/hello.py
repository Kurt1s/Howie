import discord
from discord.ext import commands
from random import randint
import requests

bot = commands.Bot(command_prefix='!', description="Kurtis' Commands")


class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        msg = 'Hello {0.author.mention}'.format(ctx.message)
        await ctx.send(msg)


    @commands.command()
    async def goodbye(self, ctx):
        msg = 'Goodbye {0.author.mention}'.format(ctx.message)
        await ctx.send(msg)

    @commands.command()
    async def countdown(self, ctx):
        await ctx.send("3\n2\n1\nTime's up!", tts=True)

    @commands.command()
    async def quote(self, ctx):
        url  = "http://www.forbes.com/forbesapi/thought/uri.json?enrich=true&query=50&relatedlimit=50"
        response = requests.get(url)
        data = response.json()
        num = randint(0, 50)
        quote = data['thought']['relatedAuthorThoughts'][num]['quote']
        print(response.json())

        await ctx.send(quote.format(ctx.message), tts=True)

    @commands.command()
    async def btc(self, ctx):
        url = "https://api.coindesk.com/v1/bpi/currentprice.json"
        response = requests.get(url)
        data = response.json()
        price = data['bpi']['USD']['rate']
        # format_currency(float(price), 'USD', locale='en_US')
        await ctx.send(price, tts=True)

    @commands.command()
    async def eth(self, ctx):
        url = "https://api.coinmarketcap.com/v1/ticker/ethereum/"
        response = requests.get(url)
        data = response.json()
        price = data[0]['price_usd']
        # format_currency(float(price), 'USD', locale='en_US')
        await ctx.send(price, tts=True)

    @commands.command()
    async def ascii(self, ctx):
        msgstr = ctx.message.content
        imgurl = msgstr.split(" ")[1:][0]
        url = "https://process.filestackapi.com/Azpx6p198SVK6pkDUxH4vz/ascii=colored:true/" + imgurl
        await ctx.send(url, tts=True)


    @commands.command()
    async def poll(self, ctx, text, *emojis: discord.Emoji):
        msg = ctx.message
        msg = await ctx.send(msg.content)  # added this
        for emoji in emojis:
            await msg.add_reaction(emoji)
        # await asynio

    @commands.command()
    async def commands(self, ctx):
        helpstr = '''```Users
         _____                                           _      
        / ____|                                         | |     
        | |     ___  _ __ ___  _ __ ___   __ _ _ __   __| |___  
        | |    / _ \| '_ ` _ \| '_ ` _ \ / _` | '_ \ / _` / __| 
        | |___| (_) | | | | | | | | | | | (_| | | | | (_| \__ \ 
         \_____\___/|_| |_| |_|_| |_| |_|\__,_|_| |_|\__,_|___/ 
                                                        
                                                        
        !hello - Get a Greeting
        !goodbye - Get a goodbye
        !quote - Get a random quote about thought
        !btc - Get bitcoin price
        !eth - Get etherium price
        !stream <URL> - Have the Bot play a song from desired URL
        !join <ChannelName> - Have the Bot join the desired Channel
        !poll <PollName> <Emojis>
        !event .............
        !ascii <ImageURL> - Returns a link to the ascii version of the image
        ```'''

        await ctx.send(helpstr, tts=True)

