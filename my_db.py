# vim: set fileencoding=utf-8 :
import secret

""" Database access abstraction module """

import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func

engine = create_engine(f"mysql+pymysql://{secret.USERNAME}:{secret.PASSWORD}@localhost/{secret.DATABASE}?charset=utf8mb4", echo=False)
Session = sessionmaker(bind=engine)

Base = declarative_base()

def db_exec_sql(*params):
    raise Exception("Not implemented %s" % (params))

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable =False)
    fio = Column(String(512), nullable = False, default = "")
    studnum = Column(String(64), nullable = False, default ="")
    quota = relationship(
        "Quota",
        uselist = False,
        back_populates="username",
        cascade="all, delete-orphan")
    queue = relationship("Queue", back_populates="username", cascade="all, delete-orphan")

    def __repr__(self):
        return "<User(username='%s', fio='%s', studnum='%s')>" % (
                            self.username, self.fio, self.studnum)

class Queue(Base):
    __tablename__ = 'queue'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    username = relationship("User", back_populates="queue")
    password = Column(String(512),nullable=False)
    date = Column(DateTime,nullable=False, default=func.now())
    done = Column(Boolean, nullable=False, default=False)
    resetedby = Column(String(512))

    def __repr__(self):
        return "<Queue(username='%s', password='%s', date='%s' done='%s' resetby='%s')>" % (
                            self.user_id, self.password, self.date, self.done, self.resetedby)

class Quota(Base):
    __tablename__ = 'quota'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    username = relationship("User", back_populates="quota")
    usedspace = Column(Integer, nullable=False, default=0)
    softlimit = Column(Integer, nullable=False, default=0)
    hardlimit = Column(Integer, nullable=False, default=0)
    grace     = Column(Integer, nullable=False, default=0)

    def __repr__(self):
        return "<Quota(username='%s', used space='%s',  softlimit='%s', hardlimit='%s', grace ends='%s')>" % (
                            self.user_id, self.usedspace, self.softlimit, self.hardlimit, self.grace)

#class 
##         printf("\"%s\"\t%d\t%d\t%d\t%d\t\"%s\"\t%d\t%d\t%d\t%d\t\"%s\""
##                "\t%d\t%d\t%d\t%d\t%d",
##                princstr, dprinc.princ_expire_time, dprinc.last_pwd_change,
##                dprinc.pw_expiration, dprinc.max_life, modprincstr,
##                dprinc.mod_date, dprinc.attributes, dprinc.kvno,
##                dprinc.mkvno, dprinc.policy ? dprinc.policy : "[none]",
##                dprinc.max_renewable_life, dprinc.last_success,
##                dprinc.last_failed, dprinc.fail_auth_count,
##     Principal (in quotes)
##     principal expire time (unix timestamp)
##     principal last password change (unix timestamp)
##     principal password expiration (unix timestamp)
##     principal max life
##     who changed principal last
##     when last changed
##     attributes (see below)
##     kvno
##     mkvno
##     policy (or [none])
##     max renewable life
##     last successful auth (unix timestamp)
##     last failed auth (unix timestamp)
##     fail_auth_count

## выделение полей можно сделать как здесь: https://docs.sqlalchemy.org/en/21/orm/mapped_sql_expr.html

## Поля
## ## static const struct flag_table_row ftbl[] = {
## ##     {"allow_postdated",         KRB5_KDB_DISALLOW_POSTDATED,    1},
## ##     {"postdateable",            KRB5_KDB_DISALLOW_POSTDATED,    1},
## ##     {"disallow_postdated",      KRB5_KDB_DISALLOW_POSTDATED,    0},
## ##     {"allow_forwardable",       KRB5_KDB_DISALLOW_FORWARDABLE,  1},
## ##     {"forwardable",             KRB5_KDB_DISALLOW_FORWARDABLE,  1},
## ##     {"disallow_forwardable",    KRB5_KDB_DISALLOW_FORWARDABLE,  0},
## ##     {"allow_tgs_req",           KRB5_KDB_DISALLOW_TGT_BASED,    1},
## ##     {"tgt_based",               KRB5_KDB_DISALLOW_TGT_BASED,    1},
## ##     {"disallow_tgt_based",      KRB5_KDB_DISALLOW_TGT_BASED,    0},
## ##     {"allow_renewable",         KRB5_KDB_DISALLOW_RENEWABLE,    1},
## ##     {"renewable",               KRB5_KDB_DISALLOW_RENEWABLE,    1},
## ##     {"disallow_renewable",      KRB5_KDB_DISALLOW_RENEWABLE,    0},
## ##     {"allow_proxiable",         KRB5_KDB_DISALLOW_PROXIABLE,    1},
## ##     {"proxiable",               KRB5_KDB_DISALLOW_PROXIABLE,    1},
## ##     {"disallow_proxiable",      KRB5_KDB_DISALLOW_PROXIABLE,    0},
## ##     {"allow_dup_skey",          KRB5_KDB_DISALLOW_DUP_SKEY,     1},
## ##     {"dup_skey",                KRB5_KDB_DISALLOW_DUP_SKEY,     1},
## ##     {"disallow_dup_skey",       KRB5_KDB_DISALLOW_DUP_SKEY,     0},
## ##     {"allow_tickets",           KRB5_KDB_DISALLOW_ALL_TIX,      1},
## ##     {"allow_tix",               KRB5_KDB_DISALLOW_ALL_TIX,      1},
## ##     {"disallow_all_tix",        KRB5_KDB_DISALLOW_ALL_TIX,      0},
## ##     {"preauth",                 KRB5_KDB_REQUIRES_PRE_AUTH,     0},
## ##     {"requires_pre_auth",       KRB5_KDB_REQUIRES_PRE_AUTH,     0},
## ##     {"requires_preauth",        KRB5_KDB_REQUIRES_PRE_AUTH,     0},
## ##     {"hwauth",                  KRB5_KDB_REQUIRES_HW_AUTH,      0},
## ##     {"requires_hw_auth",        KRB5_KDB_REQUIRES_HW_AUTH,      0},
## ##     {"requires_hwauth",         KRB5_KDB_REQUIRES_HW_AUTH,      0},
## ##     {"needchange",              KRB5_KDB_REQUIRES_PWCHANGE,     0},
## ##     {"pwchange",                KRB5_KDB_REQUIRES_PWCHANGE,     0},
## ##     {"requires_pwchange",       KRB5_KDB_REQUIRES_PWCHANGE,     0},
## ##     {"allow_svr",               KRB5_KDB_DISALLOW_SVR,          1},
## ##     {"service",                 KRB5_KDB_DISALLOW_SVR,          1},
## ##     {"disallow_svr",            KRB5_KDB_DISALLOW_SVR,          0},
## ##     {"password_changing_service", KRB5_KDB_PWCHANGE_SERVICE,    0},
## ##     {"pwchange_service",        KRB5_KDB_PWCHANGE_SERVICE,      0},
## ##     {"pwservice",               KRB5_KDB_PWCHANGE_SERVICE,      0},
## ##     {"md5",                     KRB5_KDB_SUPPORT_DESMD5,        0},
## ##     {"support_desmd5",          KRB5_KDB_SUPPORT_DESMD5,        0},
## ##     {"new_princ",               KRB5_KDB_NEW_PRINC,             0},
## ##     {"ok_as_delegate",          KRB5_KDB_OK_AS_DELEGATE,        0},
## ##     {"ok_to_auth_as_delegate",  KRB5_KDB_OK_TO_AUTH_AS_DELEGATE, 0},
## ##     {"no_auth_data_required",   KRB5_KDB_NO_AUTH_DATA_REQUIRED, 0},
## ##     {"lockdown_keys",           KRB5_KDB_LOCKDOWN_KEYS,         0},
## ## };
## ## #define NFTBL (sizeof(ftbl) / sizeof(ftbl[0]))
## ## 
## ## static const char *outflags[] = {
## ##     "DISALLOW_POSTDATED",       /* 0x00000001 */
## ##     "DISALLOW_FORWARDABLE",     /* 0x00000002 */
## ##     "DISALLOW_TGT_BASED",       /* 0x00000004 */
## ##     "DISALLOW_RENEWABLE",       /* 0x00000008 */
## ##     "DISALLOW_PROXIABLE",       /* 0x00000010 */
## ##     "DISALLOW_DUP_SKEY",        /* 0x00000020 */
## ##     "DISALLOW_ALL_TIX",         /* 0x00000040 */
## ##     "REQUIRES_PRE_AUTH",        /* 0x00000080 */
## ##     "REQUIRES_HW_AUTH",         /* 0x00000100 */
## ##     "REQUIRES_PWCHANGE",        /* 0x00000200 */
## ##     NULL,                       /* 0x00000400 */
## ##     NULL,                       /* 0x00000800 */
## ##     "DISALLOW_SVR",             /* 0x00001000 */
## ##     "PWCHANGE_SERVICE",         /* 0x00002000 */
## ##     "SUPPORT_DESMD5",           /* 0x00004000 */
## ##     "NEW_PRINC",                /* 0x00008000 */
## ##     NULL,                       /* 0x00010000 */
## ##     NULL,                       /* 0x00020000 */
## ##     NULL,                       /* 0x00040000 */
## ##     NULL,                       /* 0x00080000 */
## ##     "OK_AS_DELEGATE",           /* 0x00100000 */
## ##     "OK_TO_AUTH_AS_DELEGATE",   /* 0x00200000 */
## ##     "NO_AUTH_DATA_REQUIRED",    /* 0x00400000 */
## ##     "LOCKDOWN_KEYS",            /* 0x00800000 */
## ## };
## ## #define NOUTFLAGS (sizeof(outflags) / sizeof(outflags[0]))

Base.metadata.create_all(engine)
