#!/usr/bin/python
# coding=utf-8
import cgi
import cgitb
import sqlite3
import pwd
import grp
import base64
import json
import qrcode
import StringIO
cgitb.enable()

mainpage="""
<h1>Информация о пользователях и сброс паролей</h1>
<form method="get" action="./" name="usersearch">
Ключ поиска:<input type="text" name="searchkey">
<input type="submit" value="Submit">
</form>
%s
"""

userinfopage="""
<h1>Информация о пользователе</h1>
Имя пользователя: %s<br>
ФИО: %s<br>
Номер студенческого билета: %s</br>
Список групп: %s<br>
Фотография: %s<br>

<a href="./?reset=%s">Сбросить пароль</a>
"""

passwordupdatedpage="""
<h1>Смена пароля</h1>
Пароль заменён на: %s<br>
Считать пароль телефоном:<br>
<img src="data:image/png;base64,%s"/>
<a href="./">Вернуться на основную страницу</a>
"""

errorpage="""
<h1>Error</h1>
%s
"""

def header_html():
	print "Content-type: text/html"
	print ""

def print_ui(page):
	print """
	<html><meta http-equiv="Content-Type" content="text/html;charset=utf8"><head></head><body>
	"""
	print page.encode('utf-8')
	print """
	</body></html>
	"""

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
	conn.close()
	
	user["fio"] = result[0]
	user["studnumber"] = result[1]
	user["quota"] = 0
	user["useddiskspace"] = 0
	user["username"] = passwd[0]
	user["groups"] = []
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
		password="SoMeWeIrDpAsSwOrD"
		conn = sqlite3.connect("database.sqlite3")
		cursor = conn.cursor()
		t = ( username, password )
		cursor.execute('insert into queue (username, password) values (?, ?)', t)
		conn.commit()
		conn.close()
	else:
		password = ""
	return password

form = cgi.FieldStorage()

if "searchkey" in form:
	header_html()
	print_ui(mainpage.decode('utf-8') % "search results go here")
	exit(0)
if "getuser" in form:
	header_html()
	userinfo = getuser(form["getuser"].value)
	photo = getphoto(form["getuser"].value)
	t= (userinfo["username"], userinfo["fio"], userinfo["studnumber"], userinfo["groups"],photo, userinfo["username"])
	ui = userinfopage.decode('utf-8') % t
	print_ui(ui)
	exit(0)
if "reset" in form:
	header_html()
	newpassword=resetpassword(form["reset"].value)
	if newpassword=="":
		print_ui(errorpage % (form["reset"].value) )
	else:
		qr = qrcode.QRCode(version=10, error_correction=qrcode.ERROR_CORRECT_L)
		qr.add_data(newpassword)
		qr.make()
		image = qr.make_image()
		image_file = StringIO.StringIO()
		image.save(image_file,"PNG")
		ui = passwordupdatedpage.decode('utf-8') % (newpassword, base64.b64encode(image_file.getvalue()),)
		print_ui(ui)
	exit(0)


header_html()
print_ui(mainpage.decode('utf-8') % "")
exit(0)
