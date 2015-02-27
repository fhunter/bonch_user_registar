%include header
<h1>Превысившие квоту</h1>
<table>
	<tr>
		<td class=field_name>Пользователь</td>
		<td class=field_name>Квота</td>
		<td class=field_name>Использовано</td>
		<td class=field_name>Доступно</td>
	</tr>
% for i in quotas:
<tr>
	<td class=field_value><a href=./uinfo/{{i["username"]}}>{{i["username"]}}</a></td>
	<td class=field_value>{{i["quota"]}}</td>
	<td class=field_value>{{i["useddisk"]}}</td>
	<td class=field_value><img src=./quota/{{i["username"]}} /></td>
</tr>
%end
</table>

%include menu
%include footer
