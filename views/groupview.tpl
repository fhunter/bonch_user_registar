%include header
%import settings
<h1>Просмотр группы {{groupname}}</h1>

<form method='post'>
%for i in [('fio','ФИО'), ('number','Номер'), ('quota', 'Квота'), ('password','Пароль')]:
<input type='hidden' value='0' name="{{i[0]}}">
%if param[i[0]]:
<input type='checkbox' checked value='1' name="{{i[0]}}" onChange="this.form.submit()">
%else:
<input type='checkbox' value='1' name="{{i[0]}}" onChange="this.form.submit()">
%end
<label for="{{i[0]}}">{{i[1]}}</label>
<br/>
%end
<!--<input type='submit' value='Обновить'>--!>
</form>

<h2>{{groupname}}</h2>
<table>
<tr>
<th class=field_name>Пользователь</th>
%if param['fio']:
<th class=field_name>ФИО</th>
%end
%if param['number']:
<th class=field_name>Номер<br/>студенческого</th>
%end
%if param['quota']:
<th class=field_name>Квота</th>
%end
%if param['password']:
<th class=field_name>Пароль</th>
<th class=field_name>Применён</th>
%end 
</tr>
%for i in users:
<tr>
<td class=field_value><a href={{ settings.PREFIX }}/uinfo/{{i['username']}}>{{i['username']}}</a></td>
%if param['fio']:
<td class=field_value>{{i['fio']}}</td>
%end
%if param['number']:
<td class=field_value>{{i['studnumber']}}</td>
%end
%if param['quota']:
<td class=field_value>
%include quotatable used=i['useddiskspace'], quota=i['quota']
</td>
%end
%if param['password']:
<td class=field_value>{{i['password']}}</td>
<td class=field_value align=center valign=center>
%if i['applied']:
✅
%else:
❎
%end
</td>
%end
</tr>
%end
</table>
%include menu
%include footer
