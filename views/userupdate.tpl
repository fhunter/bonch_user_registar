%include header title = "Обновление пользовательских данных"
%import settings

<h1>Обновление регистрационных данных</h1>
<p>
Пожалуйста обновите данные, чтобы преподаватели могли воспользоваться системой сброса пароля для вас
</p>
<p>
Для обновления - заполните форму и нажмите кнопку "обновить"
</p>
<h2>Текущие данные</h2>
	<table>
		<tr>
			<td>Пользователь</td>
			<td>{{username}}</td>
		</tr>
		<tr>
			<td>ФИО:</td>
			<td>{{fio}}</td>
		</tr>
		<tr>
			<td>Номер студ. билета:</td>
			<td>{{studnum}}</td>
		</tr>
	</table>

<form method=post id="form" name="form">
<h2>Новые данные</h2>
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
%if defined('updated'):
<br/><h3>Данные обновлены</h3>
%end
	<input type=submit value="Обновить">
	</form>
	

%include footer	

