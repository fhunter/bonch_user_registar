%include header
<h1>Смена пароля</h1>
<table>
	<tr>
		<td class=field_name>Имя пользователя:</td>
		<td class=field_value><center>{{username}}</center></td>
	</tr>
	<tr>
		<td class=field_name>Пароль:</td>
		<td class=field_value><center><b>{{password}}</b></center></td>
	</tr>
	<tr>
		<td class=field_name>Считать телефоном:</td>
		<td class=field_value><img src="data:image/png;base64,{{qrcode}}"/></td>
	</tr>
</table>

%include menu
%include footer
