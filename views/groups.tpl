%include header
%import settings
<h1>Управление группами</h1>
<table border=1>
<tr><th>Группа</th><th>Пользователи</th></tr>
%for i in data:
	<tr>
		<td><a href={{ settings.PREFIX }}/groups/{{i[0]}}>{{i[0]}}</a></td>
		<td>
                %ctr = 0
		%for j in i[1]:
			<a href={{ settings.PREFIX }}/uinfo/{{j}}>{{j}}</a>
                %ctr = ctr + 1
                %if (ctr % 10) == 0:
                        <br/>
                %end
		%end 
		</td>
	</tr>
%end
</table>
<br>
Quota table = {{counts['quota']}} </br>
Users table = {{counts['users']}} </br>
Passwd file = {{counts['passwd']}} </br>
%include menu
%include footer
