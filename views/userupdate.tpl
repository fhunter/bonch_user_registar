%include header title = "Обновление пользовательских данных"

<table><tr><td>
<form method=post id="form" name="form">
	Пользователь {{username}}<br>
	ФИО: <input name=fio value="{{fio}}"></input><br>
	Номер студ. билета: <input name=studnum value="{{studnum}}"></input><br>
	Фото: <input name=photo id=photo type=hidden value="{{photo}}"></input><br><div id='results'><img src="data:image/png;base64,{{photo}}"></div>
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

%include footer	

