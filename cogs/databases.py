from discord.ext import commands
from sqlalchemy import engine, create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import datetime as dt
from tabulate import tabulate

from database.models import Base, Users, Event, Going, YoutubePlaylist


engine = create_engine('sqlite:///HAL9000.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

# If table doesn't exist, Create the database
if not engine.dialect.has_table(engine, 'event'):
    Base.metadata.create_all(engine)

class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def create(self, ctx, name: str, date: str, time: str='0:00am'):
        '''Creates an event with specified name and date
            example: !create party 12/22/2017 1:40pm
        '''

        date_time = '{} {}'.format(date, time)
        event_date = datetime.strptime(date_time, '%m/%d/%Y %I:%M%p')
        try:
            existing = session.query(Event).filter(Event.name == name, Event.date == event_date).first()
            if not existing:
                event = Event(name=name, date=event_date)
                session.add(event)
                session.commit()
                await ctx.send('Event {} created successfully for {}'.format(name, event.date))
            else:
                await ctx.send('Event {} was already created'.format(name))

        except Exception as e:
            await ctx.send('Could not complete your command')
            print(e)

    @commands.command(pass_context=True)
    async def adduser(self, ctx, username: str):
        '''Creates a user on specific date and time
            example: !adduser user
        '''
        #grab discord id from user using command
        #set it as its own variable
        #in existing check if user discord id was already in user
        #should we have it so you can change the name associated with discord id?
            #if yes than existing needs to change
            #if no than need to add discordid = session.query(Users).filter(Users.discord_id == discordidvar).first()
        userId = ctx.message.author.id
        #hi = self.get_user_info(userId)
        try:
            existing = session.query(Users).filter(Users.name == username).first()
            discordID = session.query(Users).filter(Users.discord_id == userId).first()
            if not discordID:
                date_time = dt.datetime.now().strftime("%d/%m/%Y %I:%M")
                add_date = datetime.strptime(date_time, '%d/%m/%Y %I:%M')
                user = Users(name=username, date=add_date,discord_id=userId)
                session.add(user)
                session.commit()
                await ctx.send('User {} created successfully on {}'.format(username, user.date))
            else:
                await ctx.send('User {} already made a username'.format(discordID))
        except Exception as e:
            await ctx.send('Could not complete your command')
            print(e)

    @commands.command(pass_context=True)
    async def goto(self, ctx, username: str, eventsname: str, date: str, time: str='0:00am'):
        '''Allows a user to go to an upcoming event
            example: !goto user event m/d/y h:m
        '''

        date_time = '{} {}'.format(date, time)
        event_date = datetime.strptime(date_time, '%m/%d/%Y %I:%M%p')
        try:
            user = session.query(Users).filter(Users.name == username).first()
            event = session.query(Event).filter(Event.name == eventsname, Event.date == event_date).first()

            # Verify This event exists
            if not event:
                await ctx.send('This event does not exist')
                return
            if not user:
                await ctx.send('This user does not exist')
                return
            else:
                eventid = '{} {}'.format(eventsname, event_date)
                willgo = Going(user_id= username, event_id = event.id)
                session.add(willgo)
                session.commit()
                await ctx.send('Member {} is now attending event {} on {}'.format(username, eventsname, event_date))
        except Exception as e:
            await ctx.send('Could not complete your command')
            print(e)

    @commands.command()
    async def listevents(self, ctx):
        '''Displays the list of current events
            example: !listevents
        '''
        try:
            events = session.query(Event).order_by(Event.date).all()
            headers = ['Name', 'Date and Time']
            rows = [[e.name, e.date] for e in events]
            table = tabulate(rows, headers)
            await ctx.send('```\n' + table + '```')
        except Exception as e:
            await ctx.send('Could not complete your command')
            print(e)

    @commands.command()
    async def viewevent(self, ctx,eventsname: str, date: str, time: str='0:00am'):
        '''Displays information about a specific event
            example: !viewevent party
        '''
        date_time = '{} {}'.format(date, time)
        event_date = datetime.strptime(date_time, '%m/%d/%Y %I:%M%p')
        try:
            event = session.query(Event).filter(Event.name == eventsname, Event.date == event_date).first()
            # Verify This event exists
            if not event:
                await ctx.send('This event does not exist')
                return

            attending = session.query(Going).filter(Going.event_id == event.id).count()
            info = [['Name', event.name], ['Date and Time', event.date], ['Number Attending', attending]]
            await ctx.send('```\n' + tabulate(info) + '```')
        except Exception as e:
            await ctx.send('Could not complete your command')
            print(e)


    @commands.command(pass_context=True)
    async def addsong(self, ctx, songname: str, songurl: str):
        '''Creates a song with a specific url
            example: !addsong songname songurl
        '''

        try:
            existing = session.query(YoutubePlaylist).filter(YoutubePlaylist.song == songname, YoutubePlaylist.link == songurl).first()
            if not existing:
                date_time = dt.datetime.now().strftime("%d/%m/%Y %I:%M")
                add_date = datetime.strptime(date_time, '%d/%m/%Y %I:%M')
                ytplaylist = YoutubePlaylist(song=songname, link=songurl, date=add_date)
                session.add(ytplaylist)
                session.commit()
                await ctx.send('{} added successfully on playlist on {}'.format(songname, add_date))
            else:
                await ctx.send('{} already exists'.format(songname))
        except Exception as e:
            await ctx.send('Could not complete your command')
            print(e)
