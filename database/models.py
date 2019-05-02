from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import DATETIME, INTEGER, TEXT

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(INTEGER, primary_key=True, nullable=False)
    name = Column(TEXT)
    discord_id = Column(TEXT)
    date = Column(DATETIME)

# class Event(Base):
#     __tablename__ = 'event'
#     __table_args__ = {'sqlite_autoincrement': True}
#     id = Column(INTEGER, primary_key=True, nullable=False)
#     name = Column(TEXT)
#     date = Column(DATETIME)
#
# class Going(Base):
#     __tablename__ = 'going'
#     __table_args__ = {'sqlite_autoincrement': True}
#     id = Column(INTEGER, primary_key=True, nullable=False)
#     user_id = Column(TEXT)
#     event_id = Column(TEXT)

class YoutubePlaylist(Base):
    __tablename__ = 'ytplaylist'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(INTEGER, primary_key=True, nullable=False)
    user = Column(TEXT)
    song = Column(TEXT)
    url = Column(TEXT)
    date = Column(DATETIME)

# class Poll(Base):
#     __tablename__ = 'poll'
#     __table_args__ = {'sqlite_autoincrement': True}
#     id = Column(INTEGER, primary_key=True, nullable=False)
#     song = Column(TEXT)
#     vote = Column(INTEGER)

