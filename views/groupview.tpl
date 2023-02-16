%include header
%import settings
<h1>Просмотр группы</h1>
<h2>{{groupname}}</h2>
<table>
<tr>
<td class=field_name>Пользователь</td>
<td class=field_name>Квота</td>
<td class=field_name>Пароль</td>
<td class=field_name>Применён</td>
</tr>
%for i in users:
<tr>
<td class=field_value><a href={{ settings.PREFIX }}/uinfo/{{i['username']}}>{{i['username']}}</a></td>
<td class=field_value>
%include quotatable used=i['useddiskspace'], quota=i['quota']
</td>
<td class=field_value>{{i['password']}}</td>
<td class=field_value align=center valign=center>
%if i['applied']:
✅
%else:
❎
%end
</td>
</tr>
%end
</table>
%include menu
%include footer
