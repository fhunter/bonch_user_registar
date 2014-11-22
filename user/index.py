#!/usr/bin/env python
# coding=utf-8
import os
import cgi
import cgitb
from my_db import db_exec_sql                                                                                                                                               
cgitb.enable()

def is_post():                                                                                                                                                              
	if os.environ['REQUEST_METHOD'] == 'POST':                                                                                                                          
		return True                                                                                                                                                 
	return False


user = os.environ["REMOTE_USER"].split('@')[0]

if is_post():
	form = cgi.FieldStorage()
	if "fio" in form:
		fio = form.getfirst("fio")
		result = db_exec_sql("update users set fio= ? where username=?",(fio.decode('utf-8'), user,))
	if "studnum" in form:
		studnum = form.getfirst("studnum")
		result = db_exec_sql("update users set studnum= ? where username=?",(studnum.decode('utf-8'), user,))
	if "photo" in form:
		photo = form.getfirst("photo").replace("data:image/png;base64,","")
		result = db_exec_sql("update users set photo = ? where username=?",(photo.decode('utf-8'), user,))

result = db_exec_sql("select fio, studnum, photo from users where username=?",(user,))
fio = ""
studnum = ""
photo = ""

if result:
	(fio,studnum, photo ) = result[0]
	if fio == None:
		fio = u""
	if studnum == None:
		studnum = u""
	if photo == None:
		photo = u""

print "Content: text/html"
print ""

print """<!doctype html><html lang="ru"><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><title>Обновление пользовательских данных</title></head>"""

print """
<body>
<table><tr><td>
<form method=post id="form" name="form">
	Пользователь %s<br>
	ФИО: <input name=fio value="%s"></input><br>
	Номер студ. билета: <input name=studnum value="%s"></input><br>
	Фото: <input name=photo id=photo type=hidden value="%s"></input><br><div id='results'><img src="data:image/png;base64,%s"></div>
	<input type=submit value="Обновить">
	</form>
	</td><td>
	
	<h1>WebcamJS Test Page</h1>
	<h3>Demonstrates simple capture &amp; display</h3>
	
	<div id="my_camera" style="width:320px; height:240px;"></div>
	
	<!-- First, include the Webcam.js JavaScript Library -->
	<script type="text/javascript" src="webcam.js"></script>
	
	<!-- Configure a few settings and attach camera -->
	<script language="JavaScript">
		Webcam.set({
			image_format: 'png',
			dest_width: 100,
			dest_height: 75,
			force_flash: true
		});
		Webcam.attach( '#my_camera' );
	</script>
	
	<!-- A button for taking snaps -->
	<form>
		<input type=button value="Фото" onClick="take_snapshot()">
	</form>
	</td></tr></table>
	
	<!-- Code to handle taking the snapshot and displaying it locally -->
	<script language="JavaScript">
		function take_snapshot() {
			// take snapshot and get image data
			var data_uri = Webcam.snap();

			// display results in page
			document.getElementById('photo').value = data_uri;
			document.getElementById('results').innerHTML = 	'<img src="'+data_uri+'"/>';
		}
	</script>
	
</body>
</html>
""" % (user.encode('utf-8'), fio.encode('utf-8'), studnum.encode('utf-8'), photo.encode('utf-8'), photo.encode('utf-8') )
