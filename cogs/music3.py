from discord.ext import commands
from cogs.databases import Database
import discord
import asyncio
import youtube_dl
import logging
import math
import requests
from bs4 import BeautifulSoup as bs
from video import Video



class VoiceConnectionError(commands.CommandError):
    '''Custom Exception class for connection errors.'''


class InvalidVoiceChannel(VoiceConnectionError):
    ''''Exception for cases of invalid Voice Channels.'''


async def audio_playing(ctx):
    """Checks that audio is currently playing before continuing."""
    client = ctx.guild.voice_client
    if client and client.channel and client.source:
        return True
    else:
        raise commands.CommandError("Not currently playing any audio.")


async def in_voice_channel(ctx):
    """Checks that the command sender is in the same voice channel as the bot."""
    voice = ctx.author.voice
    bot_voice = ctx.guild.voice_client
    if voice and bot_voice and voice.channel and bot_voice.channel and voice.channel == bot_voice.channel:
        return True
    else:
        raise commands.CommandError(
            "You need to be in the channel to do that.")


async def is_audio_requester(ctx):
    """Checks that the command sender is the song requester."""
    music = ctx.bot.get_cog("Music")
    state = music.get_state(ctx.guild)
    permissions = ctx.channel.permissions_for(ctx.author)
    if permissions.administrator or state.is_requester(ctx.author):
        return True
    else:
        raise commands.CommandError("You need to be the song requester to do that.")


class Music(commands.Cog):
    """Bot commands to help play music."""

    def __init__(self, bot):
        self.bot = bot
        self.states = {}

    def get_state(self, guild):
        """Gets the state for `guild`, creating it if it does not exist."""
        if guild.id in self.states:
            return self.states[guild.id]
        else:
            self.states[guild.id] = GuildState()
            return self.states[guild.id]

    @commands.command(aliases=["stop"])
    @commands.has_permissions(administrator=True)
    async def leave(self, ctx):
        """Leaves the voice channel, if currently in one."""
        client = ctx.guild.voice_client
        state = self.get_state(ctx.guild)
        if client and client.channel:
            await client.disconnect()
            state.playlist = []
            state.now_playing = None
        else:
            raise commands.CommandError("Not in a voice channel.")

    @commands.command(aliases=["resume", "p"])
    @commands.check(audio_playing)
    @commands.check(in_voice_channel)
    @commands.check(is_audio_requester)
    async def pause(self, ctx):
        """Pauses any currently playing audio."""
        client = ctx.guild.voice_client
        self._pause_audio(client)

    def _pause_audio(self, client):
        if client.is_paused():
            client.resume()
        else:
            client.pause()

    @commands.command(aliases=["vol", "v"])
    @commands.check(audio_playing)
    @commands.check(in_voice_channel)
    @commands.check(is_audio_requester)
    async def volume(self, ctx, volume: int):
        """Change the volume of currently playing audio (values 0-250)."""
        state = self.get_state(ctx.guild)

        # make sure volume is nonnegative
        if volume < 0:
            volume = 0

        max_vol = 80
        if max_vol > -1:  # check if max volume is set
            # clamp volume to [0, max_vol]
            if volume > max_vol:
                volume = max_vol

        client = ctx.guild.voice_client

        state.volume = float(volume) / 100.0
        client.source.volume = state.volume  # update the AudioSource's volume to match

    @commands.command()
    @commands.check(audio_playing)
    @commands.check(in_voice_channel)
    async def skip(self, ctx):
        """Skips the currently playing song, or votes to skip it."""
        state = self.get_state(ctx.guild)
        client = ctx.guild.voice_client
        if ctx.channel.permissions_for(ctx.author).administrator or state.is_requester(ctx.author):
            # immediately skip if requester or admin
            client.stop()
        else:
            # vote to skip song
            channel = client.channel
            self._vote_skip(channel, ctx.author)
            # announce vote
            users_in_channel = len([member for member in channel.members if not member.bot])  # don't count bots
            required_votes = math.ceil(.5 * users_in_channel)
            await ctx.send(f"{ctx.author.mention} voted to skip ({len(state.skip_votes)}/{required_votes} votes)")

    def _vote_skip(self, channel, member):
        """Register a vote for `member` to skip the song playing."""
        logging.info(f"{member.name} votes to skip")
        state = self.get_state(channel.guild)
        state.skip_votes.add(member)
        users_in_channel = len([member for member in channel.members if not member.bot])  # don't count bots

        if (float(len(state.skip_votes)) / users_in_channel) >= .5: # enough members have voted to skip, so skip the song
            logging.info(f"Enough votes, skipping...")
            channel.guild.voice_client.stop()

    '''useless"
    @commands.command(name='vote')
    async def vote(self, ctx):
        #await ctx.send("Please Vote", delete_after=20)
        await ctx.message.add_reaction('\N{CROSS MARK}')
        await asyncio.sleep(10)  # wait for 10 Seconds
        print("Waited")
        if ctx.message.reactions.count > 0:
            print("Skip")
            await self.skip_()
        print("so skip")
'''
    def _play_song(self, client, state, song):
        state.now_playing = song
        state.skip_votes = set()  # clear skip votes
        source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(song.stream_url), volume=state.volume)

        def after_playing(err):
            if len(state.playlist) > 0:
                next_song = state.playlist.pop(0)
                self._play_song(client, state, next_song)
            else:
                asyncio.run_coroutine_threadsafe(client.disconnect(), self.bot.loop)

        client.play(source, after=after_playing)

    @commands.command(aliases=["np"])
    @commands.check(audio_playing)
    async def nowplaying(self, ctx):
        """Displays information about the current song."""
        state = self.get_state(ctx.guild)
        #message =
        await ctx.send("", embed=state.now_playing.get_embed())
        #await self._add_reaction_controls(message)

    @commands.command(aliases=["q", "playlist"])
    @commands.check(audio_playing)
    async def queue(self, ctx):
        """Display the current play queue."""
        state = self.get_state(ctx.guild)
        await ctx.send(self._queue_text(state.playlist))

    def _queue_text(self, queue):
        """Returns a block of text describing a given song queue."""
        if len(queue) > 0:
            message = [f"{len(queue)} songs in queue:"]
            message += [f"  {index + 1}. **{song.title}** (requested by **{song.requested_by.name}**)"
                for (index, song) in enumerate(queue)
            ]  # add individual songs
            return "\n".join(message)
        else:
            return "The play queue is empty."

    @commands.command(aliases=["cq"])
    @commands.check(audio_playing)
    @commands.has_permissions(administrator=True)
    async def clearqueue(self, ctx):
        """Clears the play queue without leaving the channel."""
        state = self.get_state(ctx.guild)
        state.playlist = []

    @commands.command(aliases=["jq"])
    @commands.check(audio_playing)
    @commands.has_permissions(administrator=True)
    async def jumpqueue(self, ctx, song: int, new_index: int):
        """Moves song at an index to `new_index` in queue."""
        state = self.get_state(ctx.guild)  # get state for this guild
        if 1 <= song <= len(state.playlist) and 1 <= new_index:
            song = state.playlist.pop(song - 1)  # take song at index...
            state.playlist.insert(new_index - 1, song)  # and insert it.

            await ctx.send(self._queue_text(state.playlist))
        else:
            raise commands.CommandError("You must use a valid index.")

    @commands.command(brief="Plays audio from <url>.")
    async def play(self, ctx, *, url):
        """Plays audio hosted at <url> (or performs a search for <url> and plays the first result)."""

        client = ctx.guild.voice_client
        state = self.get_state(ctx.guild)  # get the guild's state

        if client and client.channel:
            try:
                video = Video(url, ctx.author)
            except youtube_dl.DownloadError as e:
                logging.warn(f"Error downloading video: {e}")
                await ctx.send(
                    "There was an error downloading your video, sorry.")
                return
            state.playlist.append(video)
            #message = \
            await ctx.send("Added to queue.", embed=video.get_embed())
            #await self._add_reaction_controls(message)
        else:
            if ctx.author.voice != None and ctx.author.voice.channel != None:
                channel = ctx.author.voice.channel
                try:
                    video = Video(url, ctx.author)
                except youtube_dl.DownloadError as e:
                    await ctx.send("There was an error downloading your video, sorry.")
                    return
                client = await channel.connect()
                self._play_song(client, state, video)
                #message =
                await ctx.send("", embed=video.get_embed())
                #await self._add_reaction_controls(message)
                logging.info(f"Now playing '{video.title}'")
            else:
                raise commands.CommandError("You need to be in a voice channel to do that.")
        author = ctx.author.name
        await Database.addsong(self, ctx, author, url, video.video_url)


    #client.wait_for('reaction_add', check=lambda r, u: u.id == 176995180300206080)
    # async def on_reaction_add(self, ctx, reaction, user):
    #     """Responds to reactions added to the bot's messages, allowing reactions to control playback."""
    #     message = reaction.message
    #     if user != self.bot.user and message.author == self.bot.user:
    #         await message.remove_reaction(reaction, user)
    #         if message.guild and message.guild.voice_client:
    #             user_in_channel = user.voice and user.voice.channel and user.voice.channel == message.guild.voice_client.channel
    #             permissions = message.channel.permissions_for(user)
    #             guild = message.guild
    #             state = self.get_state(guild)
    #             if permissions.administrator or (user_in_channel and state.is_requester(user)):
    #                 client = message.guild.voice_client
    #                 if reaction.emoji == "⏯":
    #                     # pause audio
    #
    #                     if reaction.count > 1:
    #                         self.pause(self)
    #                         ctx.send(reaction.count)
    #                 elif reaction.emoji == "⏭":
    #                     # skip audio
    #                     if reaction.count > 1:
    #                         client.stop()
    #                 elif reaction.emoji == "⏮":
    #                     if reaction.count > 1:
    #                         state.playlist.insert(0, state.now_playing)  # insert current song at beginning of playlist
    #                         client.stop()  # skip ahead
    #             elif reaction.emoji == "⏭"and user_in_channel and message.guild.voice_client and message.guild.voice_client.channel: # ensure that skip was pressed the user is in the channel, and that the bot is in a voice channel
    #                 voice_channel = message.guild.voice_client.channel
    #                 self._vote_skip(voice_channel, user)# announce vote
    #                 channel = message.channel
    #                 users_in_channel = len([
    #                     member for member in voice_channel.members
    #                     if not member.bot
    #                 ])  # don't count bots
    #                 required_votes = math.ceil(.5 * users_in_channel)
    #                 await channel.send(f"{user.mention} voted to skip ({len(state.skip_votes)}/{required_votes} votes)")

    # async def _add_reaction_controls(self, message):
    #     """Adds a 'control-panel' of reactions to a message that can be used to control the bot."""
    #
    #     CONTROLS = ["⏮", "⏯", "⏭"]
    #     for control in CONTROLS:
    #         await message.add_reaction(control)

    @commands.command(brief="Plays audio from <url> playlist.")
    async def ytplaylist(self, ctx, *, url):
        """Plays audio hosted at <url> (or performs a search for <url> and plays the first result)."""
        count = 0
        channel = ctx.author.voice.channel
        client = ctx.guild.voice_client
        state = self.get_state(ctx.guild)
        sourceCode = requests.get(url).text
        soup = bs(sourceCode, 'html.parser')
        domain = 'https://www.youtube.com'
        for link in soup.find_all("a", {"dir": "ltr"}):
            href = link.get('href')
            if href.startswith('/watch?'):
                print(link.string.strip())
            song = (domain + href)
            # count = count+1
            # video = Video(song, ctx.author)
            # state.playlist.append(song)
            await ctx.send(song)
            # self._play_song(client,state,video)
            # await ctx.send("", embed=video.get_embed())
            # logging.info(f"Now playing '{video.title}'")

        # client = ctx.guild.voice_client
        # state = self.get_state(ctx.guild)  # get the guild's state
        #
        # if client and client.channel:
        #     try:
        #         video = Video(url, ctx.author)
        #     except youtube_dl.DownloadError as e:
        #         logging.warn(f"Error downloading videos in playlist: {e}")
        #         await ctx.send(
        #             "There was an error downloading your videos, sorry.")
        #         return
        #     r = requests.get(url)
        #     page = r.text
        #     soup = bs(page, 'html.parser')
        #     res = soup.find_all('a', {'class': 'pl-video-title-link'})
        #     for l in res:
        #         await ctx.send(l.get("href"))
        #         self.play("http.youtube.com"+l.get("href"))
        #
        #
        #     state.playlist.append(video)
        #     #message =
        #     await ctx.send("Added to queue.", embed=video.get_embed())
        #     #await self._add_reaction_controls(message)
        # else:
        #     if ctx.author.voice != None and ctx.author.voice.channel != None:
        #         channel = ctx.author.voice.channel
        #         r = requests.get(url)
        #         page = r.text
        #         soup = bs(page, 'html.parser')
        #         res = soup.find_all('a', {'class': 'pl-video-title-link'})
        #         for l in res:
        #             song = "http.youtube.com"+l.get("href")
        #             try:
        #                 video = Video(song, ctx.author)
        #             except youtube_dl.DownloadError as e:
        #                 await ctx.send("There was an error downloading your video, sorry.")
        #                 return
        #             client = await channel.connect()
        #             await ctx.send(l.get("href"))
        #             self._play_song(client, state, video)
        #             # message =
        #             await ctx.send("", embed=video.get_embed())
        #             # await self._add_reaction_controls(message)
        #             logging.info(f"Now playing '{video.title}'")
        #     else:
        #         raise commands.CommandError("You need to be in a voice channel to do that.")

    @commands.command()
    async def voteup(self, ctx, member, song: int):
        state = self.get_state(ctx.guild)
        await ctx.send(self._queue_text(state.playlist))
        state.priority_votes.add(song, member)


    #needs to be redone with sets?
    async def reorganize_playlist(self, ctx):
        state = self.get_state(ctx.guild)
        current = state.priority_votes
        key_values = []
        new_playlist = []
        for key in current.keys(): #take values from current and puts them in key_values
            key_values.add(len(current.get(key)))
        key_values.sort(reverse=True) #sorts key_Values from largest to smallest
        for key in key_values:
            #not rishgt
            new_playlist.add(current.get(key)) # creates a new playlist

        state.playlist = new_playlist
        await ctx.send(self._queue_text(state.playlist))

    @commands.command(name='connect', aliases=['join'])
    async def connect_(self, ctx, *, channel: discord.VoiceChannel = None):
        # Connect to voice
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise InvalidVoiceChannel('No channel to join. Please either specify a valid channel or join one.')

        vc = ctx.voice_client

        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'Moving to channel: <{channel}> timed out.')
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'Connecting to channel: <{channel}> timed out.')

        await ctx.send(f'Connected to: **{channel}**', delete_after=20)


class GuildState:
    """Helper class managing per-guild state."""

    def __init__(self):
        self.volume = 1.0
        self.playlist = []
        self.skip_votes = set()
        self.now_playing = None
        self.priority_votes = dict()

    def is_requester(self, user):
        return self.now_playing.requested_by == user
