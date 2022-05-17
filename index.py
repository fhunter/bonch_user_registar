#!/usr/bin/python
# coding=utf-8
import bottle
from bottle import route, view, request, template, static_file, response, abort, redirect
import pwd
import os
import grp
import base64
from PIL import Image
import qrcode
import StringIO
import gpw
from my_db import db_exec_sql

def findusers(key):
	userlist = []
	key = key.decode('utf-8')
	key = '%' + key + '%'
	t = ( key, key, key )
	result=db_exec_sql("select username,fio,studnum from users where (username like %s) or (fio like %s) or (studnum like %s)", t)
	return result 

def resetpassword(username):
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
		t = ( username, password, currentuser )
		db_exec_sql('insert into queue (username, password, resetedby) values (%s, %s, %s)', t)
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
	queue = db_exec_sql("select password, done, date from queue where username=%s order by date desc limit 1", (username,))
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

@route('/')
@view('mainpage')
def main():
	return dict()

@route('/', method = 'POST')
@view('mainpage')
def main_search():
	searchkey = request.forms.get('searchkey')
	userlist=findusers(searchkey)
	return dict(query = userlist)

@route('/process/quota')  #, method = 'POST') - TODO: make it so, after debug . Should be available only from 127.0.0.1
def receive_quota_update():
	""" Method takes in lines of 'username used_blocks quota' """
	return ""

@route('/process/newuser', method = 'POST') #- TODO: make it so, after debug . Should be available only from 127.0.0.1
def receive_users_update():
	""" Method takes in json array of dictionaries: username/password """
	return ""

@route('/listoverquota')
@view('overquota')
def overquota():
	result = db_exec_sql("select username from quota where usedspace > softlimit and softlimit > 0")
	quotas = []
	for i in result:
		userinfo = getuser(i[0])
		dictionary = dict(username = i[0], quota = userinfo["quota"], useddisk = userinfo["useddiskspace"])
		quotas.append(dictionary)
	return dict(quotas = quotas)

@route('/listreset')
@view('listreset')
def listreset():
	data = db_exec_sql('select * from queue where done=False order by date desc')
	return dict(data = data)

@route('/resetstats')
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

@route('/quota/<username:re:[a-zA-Z0-9_][a-zA-Z0-9_.]+>')
def show_userquota(username):
	response.set_header('Content-type', 'image/png')
	userinfo = getuser(username)
	quota = int(userinfo["quota"])
	useddisk = int(userinfo["useddiskspace"])
	image_file = StringIO.StringIO()
	image = Image.new("RGB",(514,34), "white")
	image.im.paste((0,0,0),(0,0,514,34))
	image.im.paste((255,255,255),(1,1,513,33))
	image.im.paste((0,255,0),(1,17,int(1+(512.0/max(quota,useddisk))*quota),17+16))
	image.im.paste((255,0,0),(1,1,int(1+(512.0/max(quota,useddisk))*useddisk),1+16))
#		image = Image.new("RGB",(514,18), "white")
#		image.im.paste((0,0,0),(0,0,514,18))
#		image.im.paste((255,255,255),(1,1,513,17))
#		image.im.paste((0,255,0),(1,9,int(1+(512.0/max(quota,used))*quota),9+8))
#		image.im.paste((255,0,0),(1,1,int(1+(512.0/max(quota,used))*used),1+8))
	image.save(image_file, "PNG")
	return image_file.getvalue()

@route('/photo/<username:re:[a-zA-Z0-9_][a-zA-Z0-9_.]+>')
def show_userphoto(username):
	response.set_header('Content-type', 'image/png')
	empty="""
		iVBORw0KGgoAAAANSUhEUgAAAGQAAABkAQAAAABYmaj5AAAAAmJLR0QAAd2KE6QAAAAZSURBVDjLY/
		iPBD4wjPJGeaO8Ud4oj8Y8AL7rCVzcsTKLAAAAAElFTkSuQmCC
	"""
	t = ( username, )
	photo=db_exec_sql('select photo from users where username = %s', t)[0]
	if photo == None:
		photo=empty
	else:
		photo=photo[0]
	if photo==None:
		photo=empty
	image = photo.decode('base64')
	return image

@route('/user')
@route('/user/')
@view('userupdate')
def update_user():
	user = os.environ["REMOTE_USER"].split('@')[0]
	result = db_exec_sql("select fio, studnum, photo from users where username=%s",(user,))
	fio = ""
	studnum = ""
	photo = ""
	if result:
		(fio,studnum, photo ) = result[0]
		if fio == None:
			fio = u""
		if studnum == None:
			studnum = u""
		if photo == None:
			photo = u""
	return dict(username = user, fio = fio, studnum = studnum, photo = photo)

@route('/user', method = 'POST')
@route('/user/', method = 'POST')
@view('userupdate')
def update_user():
	user = os.environ["REMOTE_USER"].split('@')[0]
	fio = request.forms.get('fio',None)
	studnum = request.forms.get('studnum',None)
	photo = request.forms.get('photo',None)
	if fio:
		result = db_exec_sql("update users set fio= %s where username=%s",(fio.decode('utf-8'), user,))
	if studnum:
		result = db_exec_sql("update users set studnum= %s where username=%s",(studnum.decode('utf-8'), user,))
	if photo:
		dphoto = photo.replace("data:image/png;base64,","")
		result = db_exec_sql("update users set photo = %s where username=%s",(photo.decode('utf-8'), user,))
	return dict(username = user, fio = fio, studnum = studnum, photo = dphoto)

@route('/uinfo/<username:re:[a-zA-Z0-9_][a-zA-Z0-9_.]+>')
@view('userinfo')
def show_userinfo(username):
	userinfo = getuser(username)
	quota = int(userinfo["quota"])
	useddisk = int(userinfo["useddiskspace"])
	return dict(username = username, fio = userinfo["fio"], studnumber = userinfo["studnumber"], quotaused= useddisk, quotaavail = quota, groups = userinfo["groups"], issued=False, logged_in=False, password = userinfo["password"], applied = userinfo["applied"] )

@route('/reset/<username:re:[a-zA-Z0-9_][a-zA-Z0-9_.]+>')
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
		image_file = StringIO.StringIO()
		image.save(image_file,"PNG")
	return dict(username = username, password = newpassword, qrcode = base64.b64encode(image_file.getvalue()) )

@route('/groups')
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
	result = db_exec_sql('select count(username) from quota')[0][0]
	counts['quota'] = result
	result = db_exec_sql('select count(username) from users')[0][0]
	counts['users'] = result
	#cleanup begin
	#remove absent from passwd
	for i in db_exec_sql('select username from quota'):
		if i[0] not in userlist:
			#extra, remove it
			#print i[0]
			db_exec_sql('delete from quota where username = %s', (i[0],))
	for i in db_exec_sql('select username from users'):
		if i[0] not in userlist:
			#extra, remove it
			#print i[0]
			db_exec_sql('delete from users where username = %s', (i[0],))
	#insert missing
	for i in userlist:
		result = db_exec_sql('select username from quota where username = %s', (i,))
		if len(result) == 0:
			db_exec_sql('insert into quota (username, usedspace, softlimit) values ( %s, %s, %s)', (i, 0,0))
	for i in userlist:
		result = db_exec_sql('select username from users where username = %s', (i,))
		if len(result) == 0:
			db_exec_sql('insert into users (username, fio, studnum) values ( %s, %s, %s)', (i, '',''))
	#cleanup end
	for i in grp.getgrall():
	  	if (i[2] > 1000) and (i[2] <=64000):
			grouplist.append((i[0],i[3],"",))
	return dict(data = grouplist, counts = counts)

#TODO
@route('/groups/<groupname>')
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
@route('/groups/add/<groupname>')
def add_group(groupname):
	redirect('../../groups')

#TODO
@route('/groupstats')
@view('groupstats')
def show_group_queues():
	return dict()

@route('/<filename:re:.*\.css>')
def send_image(filename):
	return static_file(filename, root='./files/', mimetype='text/css')

@route('/<filename:re:.*\.js>')
def send_image(filename):
	return static_file(filename, root='./files/', mimetype='text/javascript')

@route('/<filename:re:.*\.swf>')
def send_image(filename):
	#FIXME: flash content type
	return static_file(filename, root='./files/', mimetype='application/x-shockwave-flash')

bottle.run(server=bottle.CGIServer)

