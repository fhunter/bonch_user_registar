%include header
<h1>Информация о пользователе</h1>
<table>
<tr>
	<td class=field_name>Имя пользователя:</td>
	<td class=field_value>{{username}}</td>
</tr>
<tr>
	<td class=field_name>ФИО:</td>
	<td class=field_value>{{fio}}</td>
</tr>
<tr>
	<td class=field_name>Номер студенческого билета:</td>
	<td class=field_value>{{studnumber}}</td></tr>
<tr>
	<td class=field_name>Дисковая квота:</td>
	<td class=field_value>
		<table>
		<tr><td class=field_name>использовано:</td><td class=field_value>{{quotaused}}</td><td class=field_value>Кб</td></tr>
		<tr><td class=field_name>доступно:</td><td class=field_value>{{quotaavail}}</td><td class=field_value>Кб</td></tr>
		</table><br><img src=./quota/{{username}} />
	</td>
</tr>
<tr>
	<td class=field_name>Группы:</td>
	<td class=field_value>
		<table><tr>
		%k=0
		%for i in groups:
			<td class=field_value width=20%>{{unicode(i)}}</td>
		%k = k + 1
		%if k % 5 == 0:
			</tr><tr>
		%end
		%end 
	</tr></table>
	</td></tr>
<tr>
	<td class=field_name>Фотография:</td>
	<td class=field_value><center><img src=./photo/{{username}} /></center></td>
</tr>
</table>

%include menu username =username
%include footer
