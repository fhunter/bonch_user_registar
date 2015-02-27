#!/usr/bin/python
# coding=utf-8
import bottle
from bottle import route, view, request, template, static_file, response
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
	#FIXME - this does not work for now
	return dict(username = os.environ["REMOTE_USER"], fio = "blah", studnum = "123", photo = "")

@route('/user', method = 'POST')
@route('/user/', method = 'POST')
@view('userupdate')
def update_user():
	#FIXME - this does not work for now
	return dict(username = os.environ["REMOTE_USER"], fio = "blah", studnum = "123", photo = "")

@route('/uinfo/<username:re:[a-zA-Z0-9_]+>')
@view('userinfo')
def show_userinfo(username):
	userinfo = getuser(username)
	quota = int(userinfo["quota"])
	useddisk = int(userinfo["useddiskspace"])
	return dict(username = username, fio = userinfo["fio"], studnumber = userinfo["studnumber"], quotaused= useddisk, quotaavail = quota, groups = userinfo["groups"] )

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
    return static_file(filename, root='./', mimetype='text/css')

bottle.run(server=bottle.CGIServer)


#
#passwordupdatedpage=u"""
#<h1>Смена пароля</h1>
#<table>
#	<tr><td class=field_name>Пароль:</td><td class=field_value><center><b>%s</b></center></td></tr>
#	<tr><td class=field_name>Считать телефоном:</td><td class=field_value><img src="data:image/png;base64,%s"/></td></tr>
#</table>""" + returnbutton + queuebutton + overquotabutton + statisticsbutton
#

#statisticspage=u"""
#<h1>Статистика сброса пароля</h1>
#%s
#""" + returnbutton + queuebutton + overquotabutton + statisticsbutton
#
#errorpage=u"""
#<h1>Error</h1>
#%s
#""" + returnbutton + queuebutton + overquotabutton + statisticsbutton
#
#def resetpassword(username):
#	user={}
#	password=""
#	students_gid=grp.getgrnam("students")[2]
#	try:
#		passwd = pwd.getpwnam(username)
#	except:
#		return ""
#	#check that user is a student and generate password and qrcode from it
#	if passwd[3]==students_gid:
#		password=gpw.GPW(15).password
#		currentuser = os.environ["REMOTE_USER"]
#		t = ( username, password, currentuser )
#		db_exec_sql('insert into queue (username, password, resetedby) values (?, ?, ?)', t)
#	else:
#		password = ""
#	return password
#
#def passwordupdatedpage_ui(form):
#	header_html()
#	newpassword=resetpassword(form["reset"].value)
#	if newpassword=="":
#		print_ui(errorpage % u"Пользователь должен быть в группе students" )
#	else:
#		qr = qrcode.QRCode(version=6, error_correction=qrcode.ERROR_CORRECT_L)
#		qr.add_data(newpassword)
#		qr.make()
#		image = qr.make_image()
#		image_file = StringIO.StringIO()
#		image.save(image_file,"PNG")
#		ui = passwordupdatedpage % (newpassword, base64.b64encode(image_file.getvalue()),)
#		print_ui(ui)
#
#def overquotapage_ui(form):
#	header_html()
#	result = db_exec_sql("select username from quota where usedspace > softlimit and softlimit > 0")
#	table=u"<table><tr><td class=field_name>Пользователь</td><td class=field_name>Квота</td><td class=field_name>Использовано</td><td class=field_name>Доступно</td></tr>"
#	for i in result:
#		userinfo = getuser(i[0])
#		quota = int(userinfo["quota"])
#		useddisk = int(userinfo["useddiskspace"])
#		image_file = makequota_image(useddisk,quota,True)
#		table+= u"""<tr>
#			<td class=field_value><a href=./?page=getuser&getuser=%s>%s</a></td>
#			<td class=field_value>%s</td>
#			<td class=field_value>%s</td>
#			<td class=field_value>%s</td>
#		</tr>""" % (i[0],i[0],image_file,useddisk,quota)
#	table += u"</table>"
#	print_ui(overquotapage % table)
