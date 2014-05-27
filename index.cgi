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
Имя пользователя: %s

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
	print page
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


form = cgi.FieldStorage()

if "searchkey" in form:
	header_html()
	print_ui(mainpage % "search results go here")
	exit(0)
if "getuser" in form:
	header_html()
	t= getuser(form["getuser"].value)

	print_ui(userinfopage % t)
	exit(0)
if "reset" in form:
	header_html()


header_html()
print_ui(mainpage % "")
exit(0)
#
#	if form["query"].value == "reset":
#		if "username" not in form:
#		  	header_html()
#			print json.dumps({"error": 1 });
#		else:
#		  	user={}
#			students_gid=grp.getgrnam("students")[2]
#			try:
#				passwd = pwd.getpwnam(form["username"].value)
#			except:
#				header_html()
#				print json.dumps({"error": 1 })
#				exit(0)
#			header_html()
#			#check that user is a student and generate password and qrcode from it
#			if passwd[3]==students_gid:
#				password="SoMeWeIrDpAsSwOrD"
#				conn = sqlite3.connect("database.sqlite3")
#				cursor = conn.cursor()
#				t = ( form["username"].value, password )
#				cursor.execute('insert into queue (username, password) values (?, ?)', t)
#				conn.commit()
#				conn.close()
#				print "<pre>New password will be set to:"
#				print password
#				print "</pre>"
#				qr = qrcode.QRCode(version=10, error_correction=qrcode.ERROR_CORRECT_L)
#				qr.add_data(password)
#				qr.make()
#				image = qr.make_image()
#				image_file = StringIO.StringIO()
#				image.save(image_file,"PNG")
#				print "<img src=\"data:image/png;base64,"
#				print base64.b64encode(image_file.getvalue())
#				print "\"/>"
#			else:
#				print "<pre>Must be a student!</pre>"
#		exit(0)
#	print header_html()
#	print "<pre>Blah!</pre>"
