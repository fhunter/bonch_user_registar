#!/usr/bin/env python
import os
import sqlite3
import subprocess
import sys

if "REMOTE_ADDR" in os.environ:
	print "Content/type: text/html"
	print ""
	print "Wrong page"
	exit(0)

#This is not a CGI
conn = sqlite3.connect("/var/www/selfreg/database.sqlite3")
cursor = conn.cursor()
#cursor.execute('insert into queue (username, password) values (?, ?)', t)
cursor.execute('select * from queue where done=\'false\'')
queue = cursor.fetchall()
conn.commit()
conn.close()
if queue != None:
	conn = sqlite3.connect("/var/www/selfreg/database.sqlite3")
	cursor = conn.cursor()
	for i in queue:
		print i
		commandline=u"""kadmin -p automator/admin -k -t /etc/krb5.keytab -q "change_password -pw %s %s" """ % (i[2], i[1], )
		print commandline
		try:
			retcode = subprocess.call(commandline, shell=True)
			if retcode < 0:
				print >>sys.stderr, "Child was terminated by signal", -retcode
			else:
				print >>sys.stderr, "Child returned", retcode
				if retcode == 0:
					cursor.execute('update queue set done= ? where username = ? and password = ?',(True,i[1],i[2]))
		except OSError as e:
			print >>sys.stderr, "Execution failed:", e
	conn.commit()
	conn.close()

