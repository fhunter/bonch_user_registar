#!/usr/bin/python3
# coding=utf-8

""" Main web app module """

import pwd
import grp
import base64
import io
import bottle
from bottle import view, request, static_file, abort, redirect
from sqlalchemy import or_, func
import qrcode
import gpw
import settings
from my_db import User, Queue, Quota, Session
from utils import getcurrentuser, normaliseuser
from utils import require_groups, require_users

app = application = bottle.Bottle()


def findusers(key):
    #DONE
    key = '%' + key + '%'
    session = Session()
    result = session.query(User).filter(
        or_(
            User.username.like(key),
            User.fio.like(key),
            User.studnum.like(key)
            )).all()
    return result

def resetpassword(username):
    #DONE
    password=""
    students_gid=grp.getgrnam("students")[2]
    try:
        passwd = pwd.getpwnam(username)
    except KeyError:
        return ""
    #check that user is a student and generate password and qrcode from it
    if passwd[3]==students_gid:
        password=gpw.GPW(6).password
        currentuser = getcurrentuser()
        session = Session()
        user = session.query(User).filter_by(username=username).first()
        session.add( Queue(user_id=user.id, password=password,resetedby=currentuser))
        session.commit()
    else:
        password = ""
    return password

def getuser(username):
    #DONE
    user = {}
    try:
        passwd = pwd.getpwnam(username)
    except KeyError:
        return user
    session = Session()
    result = session.query(User).filter(User.username==username).first()
    queue = session.query(
        User.username,
        Queue.password,
        Queue.done,
        Queue.date).\
        join(Queue).\
        filter(User.username==username).\
        order_by(Queue.date.desc()).limit(1).all()
    user["password"]=""
    user["applied"]=False
    if queue:
        user["password"]=queue[0].password
        user["applied"]=queue[0].done
    user["fio"] = result.fio
    user["studnumber"] = result.studnum
    user["quota"] = result.quota.softlimit
    user["useddiskspace"] = result.quota.usedspace
    user["username"] = passwd[0]
    user["groups"] = []
    user["groups"].append(grp.getgrgid(passwd[3])[0])
    for i in grp.getgrall():
        if user["username"] in i[3]:
            user["groups"].append(i[0])
    return user

@app.error(403)
def error403(error_m):
    e_message = "<html><head>"
    e_message += f"<meta http-equiv=\"refresh\" content=\"5; url='{settings.PREFIX}/'\" />"
    e_message += "</head><body><h1>Unauthorised, sorry</h1></body></html>"
    return e_message

@app.route(settings.PREFIX + '/')
@view('mainpage')
def main():
    return dict()

@app.route(settings.PREFIX + '/', method = 'POST')
@require_groups(settings.ADMINGROUPS)
@view('mainpage')
def main_search():
    searchkey = request.forms.getunicode('searchkey')
    userlist=findusers(searchkey)
    return dict(query = userlist)

#- TODO: make it so, after debug . Should be available only from 127.0.0.1
@app.route(settings.PREFIX + '/process/quota', method = 'POST')
@require_users(settings.QUOTAPROCESS)
def receive_quota_update():
    """ Method takes in lines of 'username used_blocks quota' """
    data = request.json
    session = Session()
    if isinstance(data, list):
        for i in data:
            username = i['username']
            quota = int(i['quota'])
            used  = int(i['used'])
            result = session.query(User).filter(User.username==username).first()
            if result:
                if result.quota:
                    result.quota.usedspace = used
                    result.quota.softlimit = quota
                else:
                    session.add(Quota(user_id=result.id, usedspace = used, softlimit = quota))
    else:
        username = data['username']
        quota = int(data['quota'])
        used  = int(data['used'])
        result = session.query(User).filter(User.username==username).first()
        if result:
            if result.quota:
                result.quota.usedspace = used
                result.quota.softlimit = quota
            else:
                session.add(Quota(user_id=result.id, usedspace = used, softlimit = quota))
    session.commit()
    currentuser = getcurrentuser()
    return dict(currentuser=currentuser)

#- TODO: make it so, after debug . Should be available only from 127.0.0.1
@app.route(settings.PREFIX + '/process/newuser', method = 'POST')
@require_users(settings.QUOTAPROCESS)
def receive_users_update():
    """ Method takes in json array of dictionaries: username/password """
    data = request.json
    password = resetpassword(data['username'])
    currentuser = getcurrentuser()
    return dict(username=data['username'],password=password,currentuser=currentuser)


@app.route(settings.PREFIX + '/listoverquota')
@require_groups(settings.ADMINGROUPS)
@view('overquota')
def overquota():
#    result = db_exec_sql("select username from quota where usedspace >
#    softlimit and softlimit > 0")
    session = Session()
    result = session.query(
        Quota.user_id,
        User.username, Quota.usedspace, Quota.softlimit).join(User).\
        filter(Quota.usedspace>Quota.softlimit).\
        filter(Quota.softlimit>0).all()
    quotas = []
    for i in result:
        dictionary = dict(
            username = i.username,
            quota = i.softlimit,
            useddisk = i.usedspace)
        quotas.append(dictionary)
    return dict(quotas = quotas)

@app.route(settings.PREFIX + '/listreset')
@require_groups(settings.ADMINGROUPS)
@view('listreset')
def listreset():
    session = Session()
    data = session.query(
        User.username,
        Queue.date,
        Queue.resetedby,
        Queue.password).\
        join(Queue).\
        filter(Queue.done.is_(False)).\
        order_by(Queue.date.desc()).all()
    return dict(data = data)

@app.route(settings.PREFIX + '/resetstats')
@require_groups(settings.ADMINGROUPS)
@view('statistics')
def resetstats():
    #DONE
    session = Session()
    count = session.query(Queue).count()
    requests = session.query(Queue).filter_by(done=False).count()
    result = session.query(Queue).filter_by(done=True).order_by(Queue.date.desc()).all()
    try:
        date=result[0].date
    except:
        date=None
    frequency = session.query(
        Queue.user_id,
        User.username,
        func.count(Queue.user_id).label('count')).\
        join(User).group_by(Queue.user_id).\
        order_by(func.count(Queue.user_id).desc()).limit(10)
    topresets = session.query(
        Queue.resetedby,
        func.count(Queue.resetedby).label('count')).\
        group_by(Queue.resetedby).\
        order_by(func.count(Queue.resetedby).desc()).limit(10)
    return dict(
        count = count,
        requests = requests,
        date = date,
        frequency = frequency,
        topresets = topresets)

@app.route(settings.PREFIX + '/user')
@app.route(settings.PREFIX + '/user/')
@view('userupdate')
def update_user():
    user = normaliseuser(getcurrentuser())
    session = Session()
    result = session.query(User).filter(User.username==user).first()
    fio = ""
    studnum = ""
    if result:
        fio = result.fio
        studnum =result.studnum
        if fio is None:
            fio = ""
        if studnum is None:
            studnum = ""
    return dict(username = user, fio = fio, studnum = studnum)

@app.route(settings.PREFIX + '/user', method = 'POST')
@app.route(settings.PREFIX + '/user/', method = 'POST')
@view('userupdate')
def update_user2():
    user = normaliseuser(getcurrentuser())
    fio = request.forms.getunicode('fio',None)
    studnum = request.forms.getunicode('studnum',None)
    session = Session()
    userdata = session.query(User).filter_by(username=user).first()
    if fio:
        userdata.fio = fio
    if studnum:
        userdata.studnum = studnum
    session.commit()
    return dict(username = user, fio = fio, studnum = studnum)

@app.route(settings.PREFIX + '/uinfo/<username:re:[a-zA-Z0-9_][a-zA-Z0-9_.]+>')
@require_groups(settings.ADMINGROUPS)
@view('userinfo')
def show_userinfo(username):
    userinfo = getuser(username)
    quota = int(userinfo["quota"])
    useddisk = int(userinfo["useddiskspace"])
    return dict(
        username = username,
        fio = userinfo["fio"],
        studnumber = userinfo["studnumber"],
        quotaused= useddisk,
        quotaavail = quota,
        groups = userinfo["groups"],
        issued=False,
        logged_in=False,
        password = userinfo["password"],
        applied = userinfo["applied"] )

@app.route(settings.PREFIX + '/reset/<username:re:[a-zA-Z0-9_][a-zA-Z0-9_.]+>')
@require_users(settings.QUOTAPROCESS)
@view('passwordreset')
def reset_password(username):
    newpassword=resetpassword(username)
    if newpassword=="":
        abort(401, "Sorry, access denied.")
    else:
        qr_code = qrcode.QRCode(version=6, error_correction=qrcode.ERROR_CORRECT_L)
        qr_code.add_data(newpassword)
        qr_code.make()
        image = qr_code.make_image()
        image_file = io.BytesIO()
        image.save(image_file,"PNG")
    return dict(
        username = username,
        password = newpassword,
        qrcode = base64.b64encode(image_file.getvalue()) )

@app.route(settings.PREFIX + '/resync')
@require_groups(settings.ADMINGROUPS)
def resync_groups():
    counts = {}
    counts['passwd'] = 0
    counts['users'] = 0
    counts['quota'] = 0
    userlist = []
    for i in pwd.getpwall():
        if (i.pw_uid >=1000) and (i.pw_uid <=64000):
            userlist.append(i.pw_name)
    counts['passwd'] = len(userlist)
    session = Session()
    counts['quota'] = session.query(Quota).count()
    counts['users'] = session.query(User).count()
    #cleanup begin
    to_delete = session.query(User).filter(~User.username.in_(userlist))
    for i in to_delete:
        session.delete(i)
    session.commit()
    #insert missing
    result = {i.username for i in session.query(User.username).all()}
    for i in set(userlist) - result:
        session.add(User(username=i))
    session.commit()
    #cleanup end
    return dict(counts=counts, userlist = userlist)

@app.route(settings.PREFIX + '/groups')
@require_groups(settings.ADMINGROUPS)
@view('groups')
def show_groups():
    result = resync_groups()
    counts = result['counts']
    userlist = result['userlist']
    grouplist = []
    for i in grp.getgrall():
        if (i[2] > 1000) and (i[2] <=64000):
            if i[3] and all([j.startswith(i[0]+'n') for j in i[3]]):
                grouplist.append((i[0],i[3],))
    return dict(data = grouplist, counts = counts)

#TODO
@app.route(settings.PREFIX + '/groups/<groupname>', method= ['GET', 'POST'])
@require_groups(settings.ADMINGROUPS)
@view('groupview')
def show_group(groupname):
    group = grp.getgrnam(groupname)
    users = []
    if (group[2] > 1000) and (group[2] <=64000):
        users = group[3]
    data_list = []
    for i in users:
        userinfo=getuser(i)
        data_list.append(userinfo)

    params = {'fio': True, 'number': False, 'quota': True, 'password': False}
    query = dict(request.params.decode())
    for i in ['fio', 'number', 'quota', 'password']:
        if i in query:
            params[i]= (query[i] == '1')
    params = {i : 1 if params[i] else 0 for i in params}
    return dict(groupname=groupname,users=data_list, param=params )

#TODO
@app.route(settings.PREFIX + '/groups/add/<groupname>')
@require_groups(settings.ADMINGROUPS)
def add_group(groupname):
    redirect('../../groups')

#TODO
@app.route(settings.PREFIX + '/groupstats')
@require_groups(settings.ADMINGROUPS)
@view('groupstats')
def show_group_queues():
    return dict()

@app.route(settings.PREFIX + r'/<filename:re:.*\.css>')
def send_css(filename):
    #DONE
    return static_file(filename, root='./files/', mimetype='text/css')

@app.route(settings.PREFIX + r'/<filename:re:.*\.js>')
def send_js(filename):
    #DONE
    return static_file(filename, root='./files/', mimetype='text/javascript')

class StripPathMiddleware:
    '''
    Get that slash out of the request
    '''
    def __init__(self, attr):
        self.attr = attr
    def __call__(self, environ, h_data):
        environ['PATH_INFO'] = environ['PATH_INFO'].rstrip('/')
        return self.a(environ, h_data)

if __name__ == '__main__':
    bottle.run(app=app,
        debug=True, reloader=True,
        host='127.0.0.1',
        port=8888)
