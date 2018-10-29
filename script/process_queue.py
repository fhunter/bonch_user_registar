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

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from my_db import db_exec_sql

#This is not a CGI
queue = db_exec_sql('select * from queue where done=False order by date asc')
if queue != None:
	for i in queue:
		commandline=u"""kadmin -p automator/admin -k -t /etc/krb5.keytab -q "change_password -pw %s %s" """ % (i[2], i[1], )
		try:
			retcode = subprocess.call(commandline, shell=True)
			if retcode < 0:
				print >>sys.stderr, "Child was terminated by signal", -retcode
			else:
				if retcode == 0:
				    	db_exec_sql('update queue set done=True where username = %s and password = %s', (i[1],i[2]))
				else:
					print >>sys.stderr, "Child returned", retcode
		except OSError as e:
			print >>sys.stderr, "Execution failed:", e

		commandline=u"""kadmin -p automator/admin -k -t /etc/krb5.keytab -q "modprinc +needchange %s" """ % (i[1], )
		try:
			retcode = subprocess.call(commandline, shell=True)
		except OSError as e:
			print >>sys.stderr, "Execution failed:", e

