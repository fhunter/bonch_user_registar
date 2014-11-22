#!/usr/bin/python
# coding=utf-8
import bottle
from bottle import route
import pwd
import os
import grp
import base64
from PIL import Image
import qrcode
import StringIO
import gpw
from my_db import db_exec_sql

returnbutton=u"<a href=./><button>На главную</button></a>"
queuebutton=u"<a href=./listreset><button>Очередь сброса</button></a>"
overquotabutton=u"<a href=./listoverquota><button>С превышением квоты</button></a>"
statisticsbutton=u"<a href=./resetstats><button>Статистика</button></a>"
passwordresetbutton=u"<a href=./reset/%s><button>Сбросить пароль</button></a>"

overquotapage=u"""
<h1>Превысившие квоту</h1>
%s
""" + returnbutton + queuebutton + overquotabutton + statisticsbutton

mainpage=u"""
<h1>Информация о пользователях и сброс паролей</h1>
<form method="post" action="./?page=searchkey" name="usersearch">
Ключ поиска:<input type="text" name="searchkey">
<input type="submit" value="Submit">
</form>
%s
<br>
""" + returnbutton + queuebutton + overquotabutton + statisticsbutton

@route('/')
def main():
	return mainpage

@route('/listoverquota')
def overquota():
	return overquotapage

@route('/listreset')
def listreset():
	return mainpage

@route('/resetstats')
def resetstats():
	return mainpage

bottle.run(server=bottle.CGIServer)


#cgitb.enable()
#
#
#
#userinfopage=u"""
#<h1>Информация о пользователе</h1>
#<table>
#<tr>
#	<td class=field_name>Имя пользователя:</td>
#	<td class=field_value>%s</td>
#</tr>
#<tr>
#	<td class=field_name>ФИО:</td>
#	<td class=field_value>%s</td>
#</tr>
#<tr>
#	<td class=field_name>Номер студенческого билета:</td>
#	<td class=field_value>%s</td></tr>
#<tr>
#	<td class=field_name>Дисковая квота:</td>
#	<td class=field_value>
#		<table>
#		<tr><td class=field_name>использовано:</td><td class=field_value>%d</td><td class=field_value>Кб</td></tr>
#		<tr><td class=field_name>доступно:</td><td class=field_value>%d</td><td class=field_value>Кб</td></tr>
#		</table><br>%s
#	</td>
#</tr>
#<tr>
#	<td class=field_name>Группы:</td>
#	<td class=field_value>%s</td></tr>
#<tr>
#	<td class=field_name>Фотография:</td>
#	<td class=field_value><center>%s</center></td>
#</tr>
#</table>
#
#""" + passwordresetbutton + returnbutton + queuebutton + overquotabutton + statisticsbutton
#
#passwordupdatedpage=u"""
#<h1>Смена пароля</h1>
#<table>
#	<tr><td class=field_name>Пароль:</td><td class=field_value><center><b>%s</b></center></td></tr>
#	<tr><td class=field_name>Считать телефоном:</td><td class=field_value><img src="data:image/png;base64,%s"/></td></tr>
#</table>""" + returnbutton + queuebutton + overquotabutton + statisticsbutton
#
#resetlistpage=u"""
#<h1>Очередь на сброс паролей</h1>
#%s """ + returnbutton + queuebutton + overquotabutton + statisticsbutton
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
#def header_html():
#	print "Content-type: text/html"
#	print ""
#
#def print_ui(page):
#	print """
#	<html><head><meta http-equiv="Content-Type" content="text/html;charset=utf8">
#        <link rel="stylesheet" type="text/css" href="style.css" />
#	<title>Управление пользователями</title>
#	</head><body>
#	"""
#	print page.encode('utf-8')
#	print """
#	</body></html>
#	"""
#
#def findusers(key):
#	userlist = []
#	key = key.decode('utf-8')
#	key = '%' + key + '%'
#	t = ( key, key, key )
#	result=db_exec_sql("select username,fio,studnum from users where (username like ?) or (fio like ?) or (studnum like ?)", t)
#	return result 
#
#def getuser(username):
#	user = {}
#	try:
#		passwd = pwd.getpwnam(username)
#	except:
#		return user
#	t = ( username, )
#	result=db_exec_sql('select fio,studnum from users where username = ?', t)[0]
#	quotaresult=db_exec_sql('select usedspace,softlimit from quota where username = ?',t)[0]
#	
#	user["fio"] = result[0]
#	user["studnumber"] = result[1]
#	user["quota"] = int(quotaresult[1])
#	user["useddiskspace"] = int(quotaresult[0])
#	user["username"] = passwd[0]
#	user["groups"] = []
#	user["groups"].append(grp.getgrgid(passwd[3])[0])
#	for i in grp.getgrall():
#		if user["username"] in i[3]:
#			user["groups"].append(i[0])
#	return user
#
#def getphoto(username):
#	begin="<img src=\"data:image/png;base64,"
#	end="\">"
#	empty="""
#		iVBORw0KGgoAAAANSUhEUgAAAGQAAABkAQAAAABYmaj5AAAAAmJLR0QAAd2KE6QAAAAZSURBVDjLY/
#		iPBD4wjPJGeaO8Ud4oj8Y8AL7rCVzcsTKLAAAAAElFTkSuQmCC
#	"""
#	t = ( username, )
#	photo=db_exec_sql('select photo from users where username = ?', t)[0]
#	if photo == None:
#		photo=empty
#	else:
#		photo=photo[0]
#	if photo==None:
#		photo=empty
#	return begin + photo + end
#
#def makequota_image(used,quota,small=False):
#	image_file = StringIO.StringIO()
#	if small:
#		image = Image.new("RGB",(514,18), "white")
#		image.im.paste((0,0,0),(0,0,514,18))
#		image.im.paste((255,255,255),(1,1,513,17))
#		image.im.paste((0,255,0),(1,9,int(1+(512.0/max(quota,used))*quota),9+8))
#		image.im.paste((255,0,0),(1,1,int(1+(512.0/max(quota,used))*used),1+8))
#	else:
#		image = Image.new("RGB",(514,34), "white")
#		image.im.paste((0,0,0),(0,0,514,34))
#		image.im.paste((255,255,255),(1,1,513,33))
#		image.im.paste((0,255,0),(1,17,int(1+(512.0/max(quota,used))*quota),17+16))
#		image.im.paste((255,0,0),(1,1,int(1+(512.0/max(quota,used))*used),1+16))
#	image.save(image_file, "PNG")
#	image_file = base64.b64encode(image_file.getvalue())
#	image_file = "<img src=\"data:image/png;base64,"+image_file+"\"/>"
#	return image_file
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
#def mainpage_ui(form):
#	header_html()
#	userlist=findusers(form["searchkey"].value)
#	table = u"<table><tr><td class=field_name>Имя пользователя</td><td class=field_name>ФИО</td><td class=field_name>Номер студ билета</td></tr>"
#	for i in userlist:
#		table+=u"<tr><td class=field_value><a href=\"./?page=getuser&getuser="+unicode(i[0])+"\">"+unicode(i[0]) +"</a></td><td class=field_value>"+unicode(i[1])+"</td><td class=field_value>"+unicode(i[2])+"</td></tr>"
#	table+="</table>"
#	print_ui(mainpage % (table,))
#
#def userinfopage_ui(form):
#	header_html()
#	userinfo = getuser(form["getuser"].value)
#	photo = getphoto(form["getuser"].value)
#	grouptable = u"<table><tr>"
#	k=0
#	for i in userinfo["groups"]:
#		grouptable += "<td class=field_value width=20%>" + unicode(i) + "</td>"
#		k = k + 1
#		if k % 5 == 0:
#			grouptable += "</tr><tr>"
#	grouptable += "</tr></table>"
#
#	quota = int(userinfo["quota"])
#	useddisk = int(userinfo["useddiskspace"])
#
#	image_file = makequota_image(useddisk,quota)
#	t= (userinfo["username"], userinfo["fio"], userinfo["studnumber"],useddisk,quota,image_file, grouptable,photo, userinfo["username"])
#	ui = userinfopage % t
#	print_ui(ui)
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
#def resetlistpage_ui(form):
#	header_html()
#	results=""
#	data = db_exec_sql('select * from queue where done="false" order by date desc')
#	results = u"""<table><tr><td class=field_name>Имя пользователя</td><td class=field_name>Время и дата</td><td class=field_name>Новый пароль</td><td class=field_name>Сброшено пользователем</td></tr>"""
#	for i in data:
#		results += "<tr><td class=field_value>" + i[1] + "</td><td class=field_value>" + i[3] + "</td><td class=field_value>" + i[2] + "</td><td class=field_value>" + i[5] +"</td></tr>" 
#	results += "</table>"
#	print_ui(resetlistpage % results )
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
#
#def statisticspage_ui(form):
#	header_html()
#	result = db_exec_sql("select count() from queue")
#	count = result[0][0]
#	t = u"<table><tr><td class=field_name>Всего пароли сброшены:</td><td class=field_value> %s раз</td></tr>" % count
#	result = db_exec_sql("select count() from queue where done= ?", ( 'false',))
#	count = result[0][0]
#	t+= u"<tr><td class=field_name>В очереди на сброс паролей</td><td class=field_value> %s запросов</td></tr>" % count
#	result = db_exec_sql("select date from queue where done = ? order by date desc limit 1", ( 'true', ))
#	try:
#		date=result[0][0]
#		t+= u"<tr><td class=field_name>Последний выполненный запрос пришёл</td><td class=field_value> %s" % date
#	except:
#		t+= u"<tr><td class=field_name>Выполненных запросов</td><td class=field_value> не найдено"
#	t+= u"</td></tr></table>"
#	result = db_exec_sql("select username,count(username) from queue group by username order by count(username) desc limit 10")
#	t+=u"<h1>Наиболее часто сбрасываемые пароли</h2><br>"
#	table = u"<table><tr><td class=field_name>Пользователь</td><td class=field_name>сброшен</td></tr>"
#	for i in result:
#		table += u"<tr><td class=field_value>%s</td><td class=field_value>%s раз</td></tr>" % (i[0],i[1])
#	table += u"</table>"
#	t+=table
#	result=db_exec_sql("select resetedby,count(resetedby) from queue group by resetedby order by count(resetedby) desc limit 10")
#	t+=u"<h1>Top 10 лаборантов чаще всего сбрасывавших пароли</h2><br>"
#	table = u"<table><tr><td class=field_name>Пользователь</td><td class=field_name>сбросил</td></tr>"
#	for i in result:
#		table += u"<tr><td class=field_value>%s</td><td class=field_value>%s раз</td></tr>" % (i[0],i[1])
#	table += u"</table>"
#	t+=table
#	print_ui(statisticspage % t)
#
#form = cgi.FieldStorage()
#
#pages = { "searchkey": mainpage, "getuser": userinfopage, "reset": passwordupdatedpage, "listreset": resetlistpage, "listoverquota": overquotapage, "resetstats": statisticspage}
#functions = { "searchkey": mainpage_ui, "getuser": userinfopage_ui, "reset": passwordupdatedpage_ui, "listreset": resetlistpage_ui, "listoverquota": overquotapage_ui, "resetstats": statisticspage_ui }
#
#if "page" in form:
#	functions[form["page"].value](form)
#	exit(0)
#
#header_html()
#print_ui(mainpage % "")
#exit(0)
