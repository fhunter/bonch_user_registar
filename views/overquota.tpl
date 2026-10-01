%include('header')
%import settings
%import datetime
<h1>Превысившие квоту</h1>
<table>
	<tr>
		<td class=field_name>Пользователь</td>
		<td class=field_name>Квота</td>
        <td class=field_name>Жёсткий лимит</td>
		<td class=field_name>Использовано</td>
		<td class=field_name>Доступно</td>
        <td class=field_name>Блокировка</td>
	</tr>
% for i in quotas:
<tr>
	<td class=field_value><a href={{ settings.PREFIX }}/uinfo/{{i["username"]}}>{{i["username"]}}</a></td>
	<td class=field_value>{{i["quota"]}}</td>
	<td class=field_value>{{i["useddisk"]}}</td>
    <td class=field_value>{{i["hardquota"]}}</td>
	<td class=field_value>
%include('quotatable', used=i["useddisk"], quota=i["quota"], hardquota=i["hardquota"],grace = i["grace"])
    </td>
    <td class=field_value>{{datetime.datetime.fromtimestamp(i["grace"])}}</td>
</tr>
%end
</table>

%include('menu')
%include('footer')
