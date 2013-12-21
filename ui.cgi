#!/usr/bin/python
import cgi
import cgitb
import sqlite3
import json
cgitb.enable()

form = cgi.FieldStorage()
if "query" not in form:
	print "Content-type: text/javascript"
	print ""
	print json.dumps({"error": 1 });
else:
	print "Content-type: text/javascript"
	print ""
	conn = sqlite3.connect("database.sqlite3")
	cursor = conn.cursor()
	cursor.execute("select groupname, info from groups")
	js=json.dumps({"error": 0, "groups": cursor.fetchall()})
	conn.close()
	print js
