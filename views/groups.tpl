%include header
%import settings
<h1>Управление группами</h1>
<table border=1><tr><td>Группа</td><td>Пользователи</td><td>Комментарий к группе</td></tr>
%for i in data:
	<tr>
		<td><a href={{ settings.PREFIX }}/groups/{{i[0]}}>{{i[0]}}</a></td>
		<td>
		%for j in i[1]:
			<a href={{ settings.PREFIX }}/uinfo/{{j}}>{{j}}</a>
		%end 
		</td>
		<td>{{i[2]}}</td>
	</tr>
%end
</table>
<br>
Quota table = {{counts['quota']}} </br>
Users table = {{counts['users']}} </br>
Passwd file = {{counts['passwd']}} </br>
%include menu
%include footer
