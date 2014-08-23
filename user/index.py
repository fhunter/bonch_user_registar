#!/usr/bin/env python
import os
import cgi
import cgitb
cgitb.enable()

print "Content: text/html"
print ""
print """
<!doctype html>

<html lang="en">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<title>WebcamJS Test Page</title>
	<style type="text/css">
		body { font-family: Helvetica, sans-serif; }
		h2, h3 { margin-top:0; }
		form { margin-top: 15px; }
		form > input { margin-right: 15px; }
		#results { float:right; margin:20px; padding:20px; border:1px solid; background:#ccc; }
	</style>
</head>
<body>
	<div id="results">Your captured image will appear here...</div>
	
	<h1>WebcamJS Test Page</h1>
	<h3>Demonstrates simple capture &amp; display</h3>
	
	<div id="my_camera" style="width:320px; height:240px;"></div>
	
	<!-- First, include the Webcam.js JavaScript Library -->
	<script type="text/javascript" src="webcam.js"></script>
	
	<!-- Configure a few settings and attach camera -->
	<script language="JavaScript">
		Webcam.set({
			image_format: 'png',
			dest_width: 133,
			dest_height: 100,
			force_flash: true
		});
		Webcam.attach( '#my_camera' );
	</script>
	
	<!-- A button for taking snaps -->
	<form>
		<input type=button value="Take Snapshot" onClick="take_snapshot()">
	</form>
	
	<!-- Code to handle taking the snapshot and displaying it locally -->
	<script language="JavaScript">
		function take_snapshot() {
			// take snapshot and get image data
			var data_uri = Webcam.snap();
			
			// display results in page
			document.getElementById('results').innerHTML = 
				'<h2>Here is your image:</h2>' + 
				'<img src="'+data_uri+'"/>';
		}
	</script>
	
</body>
</html>
"""
