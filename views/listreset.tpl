%include header
<h1>Очередь на сброс паролей</h1>
<table>
	<tr>
		<td class=field_name>Имя пользователя</td>
		<td class=field_name>Время и дата</td>
		<td class=field_name>Новый пароль</td>
		<td class=field_name>Сброшено пользователем</td>
	</tr>
% for i in data:
	<tr>
		<td class=field_value>{{i[1]}}</td>
		<td class=field_value>{{i[3]}}</td>
		<td class=field_value>{{i[2]}}</td>
		<td class=field_value>{{i[5]}}</td>
	</tr>
% end
</table>

%include menu
%include footer
