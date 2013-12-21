#!/usr/bin/python
import cgi
import cgitb
import sqlite3
import pwd
import json
cgitb.enable()

print "Content-type: text/javascript"
print ""

form = cgi.FieldStorage()
if "query" not in form:
	print json.dumps({"error": 1 });
else:
	if form["query"].value == "group":
		conn = sqlite3.connect("database.sqlite3")
		cursor = conn.cursor()
		cursor.execute("select groupname, info from groups")
		js=json.dumps({"error": 0, "groups": cursor.fetchall()})
		conn.close()
		print js
	if form["query"].value == "userfree":
		if "username" not in form:
			js=json.dumps({"error": 1})
		else:
			userfree=0
			try:
				pwd.getpwnam(form["username"].value)
			except KeyError:
				userfree=1
			if userfree == 0:
				js=json.dumps({"error": 0, "username": form["username"].value, "userfree": userfree})
			else:
				conn = sqlite3.connect("database.sqlite3")
				cursor = conn.cursor()
				t = ( form["username"].value, )
				cursor.execute('select username from users where username=?',t)
				if cursor.fetchone() == None :
					userfree  = 1
				else:
					userfree  = 0
				conn.close()
				js=json.dumps({"error": 0, "username": form["username"].value, "userfree": userfree})
		print js
