#!/usr/bin/python
# coding=utf-8
import bottle
from bottle import route, view, request, template, static_file, response, abort
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
	result=db_exec_sql("select username,fio,studnum from users where (username like ?) or (fio like ?) or (studnum like ?)", t)
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
		password=gpw.GPW(15).password
		currentuser = os.environ["REMOTE_USER"]
		t = ( username, password, currentuser )
		db_exec_sql('insert into queue (username, password, resetedby) values (?, ?, ?)', t)
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
	result=db_exec_sql('select fio,studnum from users where username = ?', t)[0]
	quotaresult=db_exec_sql('select usedspace,softlimit from quota where username = ?',t)[0]
	
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
	data = db_exec_sql('select * from queue where done="false" order by date desc')
	return dict(data = data)

@route('/resetstats')
@view('statistics')
def resetstats():
	result = db_exec_sql("select count() from queue")
	count = result[0][0]
	result = db_exec_sql("select count() from queue where done= ?", ( 'false',))
	requests = result[0][0]
	result = db_exec_sql("select date from queue where done = ? order by date desc limit 1", ( 'true', ))
	try:
		date=result[0][0]
	except:
		date=None
	frequency = db_exec_sql("select username,count(username) from queue group by username order by count(username) desc limit 10")
	topresets = db_exec_sql("select resetedby,count(resetedby) from queue group by resetedby order by count(resetedby) desc limit 10")
	return dict(count = count, requests = requests, date = date, frequency = frequency, topresets = topresets)

@route('/quota/<username:re:[a-zA-Z0-9_]+>')
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

@route('/photo/<username:re:[a-zA-Z0-9_]+>')
def show_userphoto(username):
	response.set_header('Content-type', 'image/png')
	empty="""
		iVBORw0KGgoAAAANSUhEUgAAAGQAAABkAQAAAABYmaj5AAAAAmJLR0QAAd2KE6QAAAAZSURBVDjLY/
		iPBD4wjPJGeaO8Ud4oj8Y8AL7rCVzcsTKLAAAAAElFTkSuQmCC
	"""
	t = ( username, )
	photo=db_exec_sql('select photo from users where username = ?', t)[0]
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
	result = db_exec_sql("select fio, studnum, photo from users where username=?",(user,))
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
		result = db_exec_sql("update users set fio= ? where username=?",(fio.decode('utf-8'), user,))
	if studnum:
		result = db_exec_sql("update users set studnum= ? where username=?",(studnum.decode('utf-8'), user,))
	if photo:
		dphoto = photo.replace("data:image/png;base64,","")
		result = db_exec_sql("update users set photo = ? where username=?",(photo.decode('utf-8'), user,))
	return dict(username = user, fio = fio, studnum = studnum, photo = dphoto)

@route('/uinfo/<username:re:[a-zA-Z0-9_]+>')
@view('userinfo')
def show_userinfo(username):
	userinfo = getuser(username)
	quota = int(userinfo["quota"])
	useddisk = int(userinfo["useddiskspace"])
	return dict(username = username, fio = userinfo["fio"], studnumber = userinfo["studnumber"], quotaused= useddisk, quotaavail = quota, groups = userinfo["groups"] )

@route('/reset/<username:re:[a-zA-Z0-9_]+>')
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
def show_groups():
	table = u"<table border=1><tr><td>Группа</td><td>Пользователи</td><td>Комментарий к группе</td></tr>"
	for i in grp.getgrall():
	  	if (i[2] > 1000) and (i[2] <=64000):
			table += "<tr><td><a href=./?page=showgroup&group=" + unicode(i[0]) + ">" + unicode(i[0]) + "</a></td>"
			k=len(i[3])
			table += u"<td>%d</td>" % k
#			comment = db_exec_sql('select comment from comments where groupname = ?', (i[0],))
#			if comment == []:
#				comment = ""
#			else:
#				comment = comment[0][0]
			comment = ""
			table += "<td>%s</td></tr>" % (comment, )
	table+="</table>"
	return table

@route('/<filename:re:.*\.css>')
def send_image(filename):
    return static_file(filename, root='./files/', mimetype='text/css')

@route('/<filename:re:.*\.js>')
def send_image(filename):
    return static_file(filename, root='./files/', mimetype='text/javascript')

@route('/<filename:re:.*\.swf>')
def send_image(filename):
	#FIXME: flash content type
    return static_file(filename, root='./files/', mimetype='text/javascript')

bottle.run(server=bottle.CGIServer)

