%include header title = "Обновление пользовательских данных"
%import settings

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
	</table>
	<input type=submit value="Обновить">
	</form>
	

%include footer	

