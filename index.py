#!/usr/bin/python
# coding=utf-8
import cgi
import cgitb
import sqlite3
import pwd
import os
import grp
import base64
import json
from PIL import Image
import qrcode
import StringIO
import gpw
cgitb.enable()

mainpage=u"""
<h1>Информация о пользователях и сброс паролей</h1>
<form method="get" action="./" name="usersearch">
Ключ поиска:<input type="text" name="searchkey">
<input type="submit" value="Submit">
</form>
%s
<br>
<a href="./?listreset=html">Очередь сброса паролей</a><br>
<a href="./?listoverquota=html">Список пользователей с превышением квоты</a><br>
<a href="./?resetstats=html">Статистика по сбросу пароля</a><br>
"""

userinfopage=u"""
<h1>Информация о пользователе</h1>
Имя пользователя: %s<br>
ФИО: %s<br>
Номер студенческого билета: %s</br>
Дисковая квота:<br><font color=red>использовано %d Кб</font><br><font color=green>из доступных %d Кб</font><br>
%s<br>
Список групп: %s<br>
Фотография: %s<br>

<a href="./?reset=%s">Сбросить пароль</a>
"""

passwordupdatedpage=u"""
<h1>Смена пароля</h1>
Пароль заменён на: %s<br>
Считать пароль телефоном:<br>
<img src="data:image/png;base64,%s"/>
<a href="./">Вернуться на основную страницу</a>
"""

resetlistpage=u"""
<h1>Очередь на сброс паролей</h1>
%s
<a href="./">Вернуться на основную страницу</a>
"""

overquotapage=u"""
<h1>Превысившие квоту</h1>
%s
<a href="./">Вернуться на основную страницу</a>
"""

statisticspage=u"""
<h1>Статистика сброса пароля</h1>
%s
<a href="./">Вернуться на основную страницу</a>
"""

errorpage=u"""
<h1>Error</h1>
%s
"""

def header_html():
	print "Content-type: text/html"
	print ""

def header_txt():
	print "Content-type: text/plain"
	print ""

def print_ui(page):
	print """
	<html><head><meta http-equiv="Content-Type" content="text/html;charset=utf8"></head><body>
	"""
	print page.encode('utf-8')
	print """
	</body></html>
	"""

def findusers(key):
	userlist = []
	conn = sqlite3.connect("database.sqlite3")
	cursor = conn.cursor()
	key = '%' + key + '%'
	t = ( key, key, key )
	cursor.execute("select username,fio,studnum from users where (username like ?) or (fio like ?) or (studnum like ?)", t)
	result=cursor.fetchall()
	conn.close()
	return result 

def getuser(username):
	user = {}
	try:
		passwd = pwd.getpwnam(username)
	except:
		return user
	conn = sqlite3.connect("database.sqlite3")
	cursor = conn.cursor()
	t = ( username, )
	cursor.execute('select fio,studnum from users where username = ?', t)
	result=cursor.fetchone()
	cursor.execute('select usedspace,softlimit from quota where username = ?',t)
	quotaresult=cursor.fetchone()
	conn.close()
	
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

def getphoto(username):
	begin="<img src=\"data:image/png;base64,"
	end="\">"
	empty="""
		iVBORw0KGgoAAAANSUhEUgAAAGQAAABkAQAAAABYmaj5AAAAAmJLR0QAAd2KE6QAAAAZSURBVDjLY/
		iPBD4wjPJGeaO8Ud4oj8Y8AL7rCVzcsTKLAAAAAElFTkSuQmCC
	"""
	conn = sqlite3.connect("database.sqlite3")
	cursor = conn.cursor()
	t = ( username, )
	cursor.execute('select photo from users where username = ?', t)
	photo=cursor.fetchone()
	if photo == None:
		photo=empty
	else:
		photo=photo[0]
	conn.close()
	if photo==None:
		photo=empty
	return begin + photo + end

def makequota_image(used,quota,small=False):
	image_file = StringIO.StringIO()
	if small:
		image = Image.new("RGB",(514,18), "white")
		image.im.paste((0,0,0),(0,0,514,18))
		image.im.paste((255,255,255),(1,1,513,17))
		image.im.paste((0,255,0),(1,9,int(1+(512.0/max(quota,used))*quota),9+8))
		image.im.paste((255,0,0),(1,1,int(1+(512.0/max(quota,used))*used),1+8))
	else:
		image = Image.new("RGB",(514,34), "white")
		image.im.paste((0,0,0),(0,0,514,34))
		image.im.paste((255,255,255),(1,1,513,33))
		image.im.paste((0,255,0),(1,17,int(1+(512.0/max(quota,used))*quota),17+16))
		image.im.paste((255,0,0),(1,1,int(1+(512.0/max(quota,used))*used),1+16))
	image.save(image_file, "PNG")
	image_file = base64.b64encode(image_file.getvalue())
	image_file = "<img src=\"data:image/png;base64,"+image_file+"\"/>"
	return image_file

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
		conn = sqlite3.connect("database.sqlite3")
		cursor = conn.cursor()
		currentuser = os.environ["REMOTE_USER"]
		t = ( username, password, currentuser )
		cursor.execute('insert into queue (username, password, resetedby) values (?, ?, ?)', t)
		conn.commit()
		conn.close()
	else:
		password = ""
	return password

def mainpage_ui(form):
	pass

def userinfopage_ui(form):
	pass

def passwordupdatedpage_ui(form):
	pass

def resetlistpage_ui(form):
	pass

def overquotapage_ui(form):
	pass

def statisticspage_ui(form):
	pass

form = cgi.FieldStorage()

pages = { "searchkey": mainpage, "getuser": userinfopage, "reset": passwordupdatedpage, "listreset": resetlistpage, "listoverquota": overquotapage, "resetstats": statisticspage}
functions = { "searchkey": mainpage_ui, "getuser": userinfopage_ui, "reset": passwordupdatedpage_ui, "listreset": resetlistpage_ui, "listoverquota": overquotapage_ui, "resetstats": statisticspage_ui }

if "searchkey" in form:
	header_html()
	userlist=findusers(form["searchkey"].value)
	table = u"<table><tr><td>Имя пользователя</td><td>ФИО</td><td>Номер студ билета</td></tr>"
	for i in userlist:
		table+=u"<tr><td><a href=\"./?getuser="+unicode(i[0])+"\">"+unicode(i[0]) +"</a></td><td>"+unicode(i[1])+"</td><td>"+unicode(i[2])+"</td></tr>"
	table+="</table>"
	print_ui(mainpage % (table,))
	exit(0)
if "getuser" in form:
	header_html()
	userinfo = getuser(form["getuser"].value)
	photo = getphoto(form["getuser"].value)
	grouptable = u"<table><tr><td>Группа</td></tr>"
	for i in userinfo["groups"]:
		grouptable += "<tr><td>" + unicode(i) + "</td></tr>"
	grouptable += "</table>"

	quota = int(userinfo["quota"])
	useddisk = int(userinfo["useddiskspace"])

	image_file = makequota_image(useddisk,quota)
	t= (userinfo["username"], userinfo["fio"], userinfo["studnumber"],useddisk,quota,image_file, grouptable,photo, userinfo["username"])
	ui = userinfopage % t
	print_ui(ui)
	exit(0)
if "reset" in form:
	header_html()
	newpassword=resetpassword(form["reset"].value)
	if newpassword=="":
		print_ui(errorpage % u"Пользователь должен быть в группе students" )
	else:
		qr = qrcode.QRCode(version=10, error_correction=qrcode.ERROR_CORRECT_L)
		qr.add_data(newpassword)
		qr.make()
		image = qr.make_image()
		image_file = StringIO.StringIO()
		image.save(image_file,"PNG")
		ui = passwordupdatedpage % (newpassword, base64.b64encode(image_file.getvalue()),)
		print_ui(ui)
	exit(0)
if "listreset" in form:
	header_html()
	results=""
	conn = sqlite3.connect("database.sqlite3")
	cursor = conn.cursor()
	cursor.execute('select * from queue where done="false" order by date desc')
	data = cursor.fetchall()
	conn.close()
	results = u"<table border=1><tr><td>Имя пользователя</td><td>Время и дата</td><td>Новый пароль</td><td>Сброшено пользователем</td></tr>"
	for i in data:
		results += "<tr><td>" + i[1] + "</td><td>" + i[3] + "</td><td>" + i[2] + "</td><td>" + i[5] +"</td></tr>" 
	results += "</table>"
	print_ui(resetlistpage % results )
	exit(0)
if "listoverquota" in form:
	header_html()
	conn = sqlite3.connect("database.sqlite3")
	cursor = conn.cursor()
	cursor.execute("select username from quota where usedspace > softlimit and softlimit > 0")
	result=cursor.fetchall()
	table=""
	for i in result:
		userinfo = getuser(i[0])
		quota = int(userinfo["quota"])
		useddisk = int(userinfo["useddiskspace"])
		image_file = makequota_image(useddisk,quota,True)
		table+= i[0] + image_file + u"Квота %s/%s" % (useddisk,quota) + "<br>"
	print_ui(overquotapage % table)
	exit(0)
if "resetstats" in form:
	header_html()
	conn = sqlite3.connect("database.sqlite3")
	cursor = conn.cursor()
	cursor.execute("select count() from queue")
	result=cursor.fetchall()
	count = result[0][0]
	t = u"Всего пароли сброшены: %s раз<br>" % count
	cursor.execute("select count() from queue where done= ?", ( 'false',))
	result=cursor.fetchall()
	count = result[0][0]
	t+= u"В очереди на сброс паролей %s запросов<br>" % count
	cursor.execute("select date from queue where done = ? order by date desc limit 1", ( 'true', ))
	result=cursor.fetchall()
	try:
		date=result[0][0]
		t+= u"Последний выполненный запрос пришёл %s <br>" % date
	except:
		t+= u"Выполненных запросов не найдено<br>"
	cursor.execute("select username,count(username) from queue group by username order by count(username) desc limit 10")
	t+=u"<h2>Наиболее часто сбрасываемые пароли</h2><br>"
	table = u"<table border=1><tr><td>Пользователь</td><td>сброшен</td></tr>"
	for i in cursor.fetchall():
		table += u"<tr><td>%s</td><td>%s раз</td></tr>" % (i[0],i[1])
	table += u"</table>"
	t+=table
	cursor.execute("select resetedby,count(resetedby) from queue group by resetedby order by count(resetedby) desc limit 10")
	t+=u"<h2>Top 10 лаборантов чаще всего сбрасывавших пароли</h2><br>"
	table = u"<table border=1><tr><td>Пользователь</td><td>сбросил</td></tr>"
	for i in cursor.fetchall():
		table += u"<tr><td>%s</td><td>%s раз</td></tr>" % (i[0],i[1])
	table += u"</table>"
	t+=table
	conn.close()
	print_ui(statisticspage % t)
	exit(0)


header_html()
print_ui(mainpage % "")
exit(0)
