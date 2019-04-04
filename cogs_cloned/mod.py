import discord
from discord.ext import commands
import asyncio


class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_ban(self, name_or_id):
        #Get a ban in the Server
        for ban in await self.guild.bans():
            if name_or_id.isdigit():
                if ban.user.id == int(name_or_id):
                    return ban
            if str(ban.user).lower().startswith(name_or_id.lower()):
                return ban

    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason=None):
        #Kick a member from the Server
        await ctx.guild.kick(user, reason=reason)
        await ctx.send(f'Done. {user.name} was kicked.')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason=None):
        #Ban a member from the guild
        await ctx.guild.ban(user, reason=reason)
        await ctx.send(f'Done. {user.name} was banned.')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(self, ctx, name_or_id, *, reason=None):
        #Unban a member from the guild
        ban = await ctx.get_ban(name_or_id)
        if not ban:
            return await ctx.send('No user found.')
        await ctx.guild.unban(ban.user, reason=reason)
        await ctx.send(f'Unbanned *{ban.user}* from the server.')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def softban(self, ctx, member: discord.Member, *, reason=None):
        #Kicks a members and deletes their messages.
        await member.ban(reason=f'Softban - {reason}')
        await member.unban(reason='Softban unban.')
        await ctx.send(f'Done. {member.name} was softbanned.')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def hackban(self, ctx, user_id: int, *, reason=None):
        #Bans a user that is currently not in the server.
        #Only accepts user IDs.

        await ctx.guild.ban(discord.Object(id=user_id), reason=reason)
        await ctx.send(f'*{self.bot.get_user(user_id)}* just got hackbanned!')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def mute(self, ctx, user: discord.Member, time: int=15):
        #Mute a member in the guild
        secs = time * 60
        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel):
                await ctx.channel.set_permissions(user, send_messages=False)
            elif isinstance(channel, discord.VoiceChannel):
                await channel.set_permissions(user, connect=False)
        await ctx.send(f"{user.mention} has been muted for {time} minutes.")
        await asyncio.sleep(secs)
        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel):
                await ctx.channel.set_permissions(user, send_messages=None)
            elif isinstance(channel, discord.VoiceChannel):
                await channel.set_permissions(user, connect=None)
        await ctx.send(f'{user.mention} has been unmuted from the guild.')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def unmute(self, ctx, user: discord.Member):
        #Unmute a member in the guild
        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel):
                await ctx.channel.set_permissions(user, send_messages=None)
            elif isinstance(channel, discord.VoiceChannel):
                await channel.set_permissions(user, connect=None)
        await ctx.send(f'{user.mention} has been unmuted from the guild.')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, user: discord.Member, *, reason: str):
        #Warn a member via DMs
        warning = f'You have been warned in **{ctx.guild}** by **{ctx.author}** for {reason}'
        if not reason:
            warning = f'You have been warned in **{ctx.guild}** by **{ctx.author}**'
        try:
            await user.send(warning)
        except discord.Forbidden:
            return await ctx.send('The user has disabled DMs for this Server or blocked the bot.')
        await ctx.send(f'**{user}** has been **warned**')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge(self, ctx, messages: int):
        #Delete messages a certain number of messages from a channel.
        if messages > 99:
            messages = 99
        await ctx.channel.purge(limit=messages + 1)
        await ctx.send(f'{messages} messages deleted. 👌', delete_after=3)

