#!/usr/bin/python3
# coding=utf-8
import pwd
import os
import grp
import base64
import io
import bottle
from bottle import route, view, request, template, static_file, response, abort, redirect
from PIL import Image
from sqlalchemy import or_
import qrcode
import gpw
import settings
from my_db import User, Queue, Quota, Session

def findusers(key):
    #DONE
    userlist = []
    key = '%' + key + '%'
    session = Session()
    result = session.query(User).filter(or_(User.username.like(key), User.fio.like(key), User.studnum.like(key))).all()
    return result

def resetpassword(username):
    #DONE
    user={}
    password=""
    students_gid=grp.getgrnam("students")[2]
    try:
        passwd = pwd.getpwnam(username)
    except:
        return ""
    #check that user is a student and generate password and qrcode from it
    if passwd[3]==students_gid:
        password=gpw.GPW(6).password
        currentuser = os.environ["REMOTE_USER"]
        session = Session()
        session.add( Queue(username=username, password=password,resetedby=currentuser))
        session.commit()
    else:
        password = ""
    return password

def getuser(username):
    user = {}
    try:
        passwd = pwd.getpwnam(username)
    except:
        return user
    t = ( username, )
    result=db_exec_sql("select fio,studnum from users where username = %s", t)[0]
    quotaresult=db_exec_sql("select usedspace,softlimit from quota where username = %s",t)[0]
    queue = db_exec_sql("select password, done, date from queue where username=%s order by date desc limit 1", (username,) )
    user["password"]=""
    user["applied"]=False
    if queue:
        user["password"]=queue[0][0]
        user["applied"]=queue[0][1]
    user["fio"] = result[0]
    user["studnumber"] = result[1]
    user["quota"] = int(quotaresult[1])
    user["useddiskspace"] = int(quotaresult[0])
    user["username"] = passwd[0]
    user["groups"] = []
    user["groups"].append(grp.getgrgid(passwd[3])[0])
    for i in grp.getgrall():
        if user["username"] in i[3]:
            user["groups"].append(i[0])
    return user

@route(settings.PREFIX + '/')
@view('mainpage')
def main():
    return dict()

@route(settings.PREFIX + '/', method = 'POST')
@view('mainpage')
def main_search():
    searchkey = request.forms.get('searchkey')
    userlist=findusers(searchkey)
    return dict(query = userlist)

#- TODO: make it so, after debug . Should be available only from 127.0.0.1
@route(settings.PREFIX + '/process/quota', method = 'POST') 
def receive_quota_update():
    """ Method takes in lines of 'username used_blocks quota' """
    data = request.json
    if isinstance(data, list):
        for i in data:
            username = i['username']
            quota = int(i['quota'])
            used  = int(i['used'])
            db_exec_sql("insert into quota (username,usedspace,softlimit) values ( %s, '%s', '%s' ) on duplicate key update usedspace='%s', softlimit='%s';", (username, used, quota, used, quota) )
    else:
        username = data['username']
        quota = int(data['quota'])
        used  = int(data['used'])
        db_exec_sql("insert into quota (username,usedspace,softlimit) values ( %s, '%s', '%s' ) on duplicate key update usedspace='%s', softlimit='%s';", (username, used, quota, used, quota) )
    currentuser = os.environ["REMOTE_USER"]
    return dict(currentuser=currentuser)

#- TODO: make it so, after debug . Should be available only from 127.0.0.1
@route(settings.PREFIX + '/process/newuser', method = 'POST')
def receive_users_update():
    """ Method takes in json array of dictionaries: username/password """
    data = request.json
    password = resetpassword(data['username'])
    currentuser = os.environ["REMOTE_USER"]
    return dict(username=data['username'],password=password,currentuser=currentuser)

@route(settings.PREFIX + '/listoverquota')
@view('overquota')
def overquota():
    result = db_exec_sql("select username from quota where usedspace > softlimit and softlimit > 0")
    quotas = []
    for i in result:
        userinfo = getuser(i[0])
        dictionary = dict(username = i[0], quota = userinfo["quota"], useddisk = userinfo["useddiskspace"])
        quotas.append(dictionary)
    return dict(quotas = quotas)

@route(settings.PREFIX + '/listreset')
@view('listreset')
def listreset():
    data = db_exec_sql('select * from queue where done=False order by date desc')
    return dict(data = data)

@route(settings.PREFIX + '/resetstats')
@view('statistics')
def resetstats():
    result = db_exec_sql("select count(*) from queue")
    count = result[0][0]
    result = db_exec_sql("select count(*) from queue where done= False")
    requests = result[0][0]
    result = db_exec_sql("select date from queue where done = True order by date desc limit 1")
    try:
        date=result[0][0]
    except:
        date=None
    frequency = db_exec_sql("select username,count(username) from queue group by username order by count(username) desc limit 10")
    topresets = db_exec_sql("select resetedby,count(resetedby) from queue group by resetedby order by count(resetedby) desc limit 10")
    return dict(count = count, requests = requests, date = date, frequency = frequency, topresets = topresets)

@route(settings.PREFIX + '/quota/<username:re:[a-zA-Z0-9_][a-zA-Z0-9_.]+>')
def show_userquota(username):
    response.set_header('Content-type', 'image/png')
    userinfo = getuser(username)
    quota = int(userinfo["quota"])
    useddisk = int(userinfo["useddiskspace"])
    image_file = io.StringIO()
    image = Image.new("RGB",(514,34), "white")
    image.im.paste((0,0,0),(0,0,514,34))
    image.im.paste((255,255,255),(1,1,513,33))
    image.im.paste((0,255,0),(1,17,int(1+(512.0/max(quota,useddisk))*quota),17+16))
    image.im.paste((255,0,0),(1,1,int(1+(512.0/max(quota,useddisk))*useddisk),1+16))
#        image = Image.new("RGB",(514,18), "white")
#        image.im.paste((0,0,0),(0,0,514,18))
#        image.im.paste((255,255,255),(1,1,513,17))
#        image.im.paste((0,255,0),(1,9,int(1+(512.0/max(quota,used))*quota),9+8))
#        image.im.paste((255,0,0),(1,1,int(1+(512.0/max(quota,used))*used),1+8))
    image.save(image_file, "PNG")
    return image_file.getvalue()

@route(settings.PREFIX + '/photo/<username:re:[a-zA-Z0-9_][a-zA-Z0-9_.]+>')
def show_userphoto(username):
    response.set_header('Content-type', 'image/png')
    empty="""
        iVBORw0KGgoAAAANSUhEUgAAAGQAAABkAQAAAABYmaj5AAAAAmJLR0QAAd2KE6QAAAAZSURBVDjLY/
        iPBD4wjPJGeaO8Ud4oj8Y8AL7rCVzcsTKLAAAAAElFTkSuQmCC
    """
    t = ( username, )
    photo=db_exec_sql('select photo from users where username = %s', t)[0]
    if photo is None:
        photo=empty
    else:
        photo=photo[0]
    if photo is None:
        photo=empty
    image = photo.decode('base64')
    return image

@route(settings.PREFIX + '/user')
@route(settings.PREFIX + '/user/')
@view('userupdate')
def update_user():
    user = os.environ["REMOTE_USER"].split('@')[0]
    result = db_exec_sql("select fio, studnum, photo from users where username=%s",(user,))
    fio = ""
    studnum = ""
    photo = ""
    if result:
        (fio,studnum, photo ) = result[0]
        if fio is None:
            fio = ""
        if studnum is None:
            studnum = ""
        if photo is None:
            photo = ""
    return dict(username = user, fio = fio, studnum = studnum, photo = photo)

@route(settings.PREFIX + '/user', method = 'POST')
@route(settings.PREFIX + '/user/', method = 'POST')
@view('userupdate')
def update_user2():
    user = os.environ["REMOTE_USER"].split('@')[0]
    fio = request.forms.get('fio',None)
    studnum = request.forms.get('studnum',None)
    photo = request.forms.get('photo',None)
    if fio:
        db_exec_sql("update users set fio= %s where username=%s",(fio.decode('utf-8'), user,))
    if studnum:
        db_exec_sql("update users set studnum= %s where username=%s",(studnum.decode('utf-8'), user,))
    if photo:
        dphoto = photo.replace("data:image/png;base64,","")
        db_exec_sql("update users set photo = %s where username=%s",(photo.decode('utf-8'), user,))
    return dict(username = user, fio = fio, studnum = studnum, photo = dphoto)

@route(settings.PREFIX + '/uinfo/<username:re:[a-zA-Z0-9_][a-zA-Z0-9_.]+>')
@view('userinfo')
def show_userinfo(username):
    userinfo = getuser(username)
    quota = int(userinfo["quota"])
    useddisk = int(userinfo["useddiskspace"])
    return dict(username = username, fio = userinfo["fio"], studnumber = userinfo["studnumber"], quotaused= useddisk, quotaavail = quota, groups = userinfo["groups"], issued=False, logged_in=False, password = userinfo["password"], applied = userinfo["applied"] )

@route(settings.PREFIX + '/reset/<username:re:[a-zA-Z0-9_][a-zA-Z0-9_.]+>')
@view('passwordreset')
def reset_password(username):
    newpassword=resetpassword(username)
    if newpassword=="":
        abort(401, "Sorry, access denied.")
    else:
        qr = qrcode.QRCode(version=6, error_correction=qrcode.ERROR_CORRECT_L)
        qr.add_data(newpassword)
        qr.make()
        image = qr.make_image()
        image_file = io.StringIO()
        image.save(image_file,"PNG")
    return dict(username = username, password = newpassword, qrcode = base64.b64encode(image_file.getvalue()) )

@route(settings.PREFIX + '/groups')
@view('groups')
def show_groups():
    grouplist = []
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
    result = session.query(Quota).count()
#    result = db_exec_sql('select count(username) from quota')[0][0]
    counts['quota'] = result
    result = session.query(User).count()
#    result = db_exec_sql('select count(username) from users')[0][0]
    counts['users'] = result
    #cleanup begin
    #remove absent from passwd
###    for i in db_exec_sql('select username from quota'):
###        if i[0] not in userlist:
###            #extra, remove it
###            #print i[0]
###            db_exec_sql('delete from quota where username = %s', (i[0],))
###    for i in db_exec_sql('select username from users'):
###        if i[0] not in userlist:
###            #extra, remove it
###            #print i[0]
###            db_exec_sql('delete from users where username = %s', (i[0],))
    #insert missing
    for i in userlist:
#        result = db_exec_sql('select username from quota where username = %s', (i,))
        result = session.query(Quota).filter(Quota.username==i).all()
        if len(result) == 0:
            session.add(Quota(username=i,usedspace=0,softlimit=0))
            #db_exec_sql('insert into quota (username, usedspace, softlimit) values ( %s, %s, %s)', (i, 0,0))
    for i in userlist:
        #result = db_exec_sql('select username from users where username = %s', (i,))
        result = session.query(User).filter(User.username == i).all()
        if len(result) == 0:
            session.add(User(username=i))
            #db_exec_sql('insert into users (username, fio, studnum) values ( %s, %s, %s)', (i, '',''))
    session.commit()
    #cleanup end
    for i in grp.getgrall():
        if (i[2] > 1000) and (i[2] <=64000):
            grouplist.append((i[0],i[3],"",))
    return dict(data = grouplist, counts = counts)

#TODO
@route(settings.PREFIX + '/groups/<groupname>')
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
    return dict(groupname=groupname,users=data_list, )

#TODO
@route(settings.PREFIX + '/groups/add/<groupname>')
def add_group(groupname):
    redirect('../../groups')

#TODO
@route(settings.PREFIX + '/groupstats')
@view('groupstats')
def show_group_queues():
    return dict()

@route(settings.PREFIX + r'/<filename:re:.*\.css>')
def send_css(filename):
    return static_file(filename, root='./files/', mimetype='text/css')

@route(settings.PREFIX + r'/<filename:re:.*\.js>')
def send_js(filename):
    return static_file(filename, root='./files/', mimetype='text/javascript')

@route(settings.PREFIX + r'/<filename:re:.*\.swf>')
def send_swf(filename):
    #FIXME: flash content type
    return static_file(filename, root='./files/', mimetype='application/x-shockwave-flash')

#bottle.run(server=bottle.CGIServer)
bottle.run(host="127.0.0.1", port=8888, debug=True, reloader=True)
