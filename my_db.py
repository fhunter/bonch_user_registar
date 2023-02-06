# vim: set fileencoding=utf-8 :
#import secret

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, LargeBinary, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///database_.sqlite3', echo=True)
Session = sessionmaker(bind=engine)

Base = declarative_base()

#CREATE TABLE users (id integer primary key autoincrement not null, username text unique, fio text,studnum text, photo blob);
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    fio = Column(String)
    studnum = Column(String)
    photo_id = Column(Integer, ForeignKey('photos.id'))
    photo = relationship("Photo")
    quota = relationship("Quota")

    def __repr__(self):
        return "<User(username='%s', fio='%s', studnum='%s')>" % (
                            self.username, self.fio, self.studnum)

class Photo(Base):
    __tablename__ = 'photos'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User")
    photo = Column(LargeBinary)

    def __repr__(self):
        return "<Photo(user_id='%s', photo='%s')>" % (
                            self.user_id, self.photo)

#CREATE TABLE queue (id integer primary key autoincrement not null, username text not null, password text not null, date datetime not null default current_timestamp, done boolean not null default 'false',resetedby text);
class Queue(Base):
    __tablename__ = 'queue'
    id = Column(Integer, primary_key=True)
    username = Column(String) # notnull - foreign key
    password = Column(String) # notnull
    date = Column(DateTime) # notnull, default current_timestamp
    done = Column(Boolean) # default false, not null
    resetedby = Column(String)
    
    def __repr__(self):
        return "<Queue(username='%s', password='%s', date='%s' done='%s' resetby='%s')>" % (
                            self.username, self.password, self.date, self.done, self.resetedby)

#CREATE TABLE quota (id integer primary key autoincrement not null, username text not null unique, usedspace integer not null, softlimit integer not null);
class Quota(Base):
    __tablename__ = 'quota'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    usedspace = Column(Integer)
    softlimit = Column(Integer)

    def __repr__(self):
        return "<Quota(username='%s', used space='%s',  softlimit='%s')>" % (
                            self.username, self.usedspace, self.softlimit)


Base.metadata.create_all(engine)
