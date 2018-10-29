# vim: set fileencoding=utf-8 :
#import sqlite3
import MySQLdb
import secret

def db_open():
	#conn = sqlite3.connect("database.sqlite3")
	#conn.execute('pragma foreign_keys = on')
        conn = MySQLdb.connect(host=secret.dbhost,
                               user=secret.dbuser,
                               passwd=secret.dbpassword,
                               db=secret.database)

	return conn

def db_exec_sql(*request):
	if len(request)<1:
		return None
	conn = db_open()
	cursor = conn.cursor()
	if len(request)==1:
		cursor.execute(request[0])
	else:
		cursor.execute(request[0],request[1])
	result=cursor.fetchall()
	conn.commit()
	conn.close()
	return result
	

