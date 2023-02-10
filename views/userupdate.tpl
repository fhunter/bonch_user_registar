%include header title = "Обновление пользовательских данных"
%import settings

<table><tr><td>
<form method=post id="form" name="form">
	<table>
		<tr>
			<td>Пользователь</td>
			<td>{{username}}</td>
		</tr>
		<tr>
			<td>ФИО:</td>
			<td><input name=fio value="{{fio}}"></input></td>
		</tr>
		<tr>
			<td>Номер студ. билета:</td>
			<td><input name=studnum value="{{studnum}}"></input></td>
		</tr>
		<tr>
			<td>Фото:</td>
			<td>
				<input name=photo id=photo type=hidden value="{{photo}}"></input>
				<div id='results'><img src="data:image/png;base64,{{photo}}"></div>
			</td>
		</tr>
	</table>
	<input type=submit value="Обновить">
	</form>
	</td><td>
	
	<div id="my_camera" style="width:320px; height:240px;"></div>
	
	<!-- First, include the Webcam.js JavaScript Library -->
	<script type="text/javascript" src="{{ settings.PREFIX}}/webcam.js"></script>
	
	<!-- Configure a few settings and attach camera -->
	<script language="JavaScript">
		Webcam.set({
			image_format: 'png',
			dest_width: 100,
			dest_height: 75,
			force_flash: false
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

