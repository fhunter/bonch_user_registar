%include header
<h1>Управление группами</h1>
<table border=1><tr><td>Группа</td><td>Пользователи</td><td>Комментарий к группе</td></tr>
%for i in data:
	<tr>
		<td><a href=./groups/{{i[0]}}>{{i[0]}}</a></td>
		<td>
		%for j in i[1]:
			<a href=./uinfo/{{j}}>{{j}}</a>
		%end 
		</td>
		<td>{{i[2]}}</td>
	</tr>
%end
</table>
<br>
%include menu
%include footer
