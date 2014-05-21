#!/usr/bin/python
import cgi
import cgitb
import sqlite3
import pwd
import base64
import json
cgitb.enable()

def header():
	print "Content-type: text/javascript"
	print ""

form = cgi.FieldStorage()
if "query" not in form:
  	header()
	print json.dumps({"error": 1 });
else:
	if form["query"].value == "getuser":
		if "username" not in form:
		  	header()
			print json.dumps({"error": 1 });
		else:
		  	user={}
			user["quota"]=0
			user["useddiskspace"] = 0
			user["username"] = form["username"].value
			user["fio"] = ""
			user["studnumber"] = ""
			js=json.dumps({"error": 0, "username": user})
			header()
			print js
	if form["query"].value == "getphoto":
	  	print "Content-type: text/html"
		print ""
		print "<img src=\"data:image/png;base64,"
		if "username" not in form:
			s="""iVBORw0KGgoAAAANSUhEUgAAAGQAAABkAQAAAABYmaj5AAAAAmJLR0QAAd2KE6QAAAAZSURBVDjLY/
iPBD4wjPJGeaO8Ud4oj8Y8AL7rCVzcsTKLAAAAAElFTkSuQmCC"""
			print s
		else:
			#Fetch photo from table if it exists
		  	print ""
		print "\">"

			
