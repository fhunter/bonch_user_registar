# vim: set fileencoding=utf-8 :
#import secret

""" Database access abstraction module """

import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, LargeBinary, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///database_.sqlite3', echo=True)
Session = sessionmaker(bind=engine)

Base = declarative_base()

def db_exec_sql(*params):
    raise Exception("Not implemented %s" % (params))

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable =False)
    fio = Column(String, nullable = False, default = "")
    studnum = Column(String, nullable = False, default ="")
    photo = relationship("Photo")
    quota = relationship("Quota")
    queue = relationship("Queue")

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

class Queue(Base):
    __tablename__ = 'queue'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    password = Column(String,nullable=False)
    date = Column(DateTime,nullable=False, default=datetime.datetime.now())
    done = Column(Boolean, nullable=False, default=False)
    resetedby = Column(String)

    def __repr__(self):
        return "<Queue(username='%s', password='%s', date='%s' done='%s' resetby='%s')>" % (
                            self.user_id, self.password, self.date, self.done, self.resetedby)

class Quota(Base):
    __tablename__ = 'quota'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    usedspace = Column(Integer, nullable=False, default=0)
    softlimit = Column(Integer, nullable=False, default=0)

    def __repr__(self):
        return "<Quota(username='%s', used space='%s',  softlimit='%s')>" % (
                            self.user_id, self.usedspace, self.softlimit)


Base.metadata.create_all(engine)
