%include header
%import settings
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
%from utils import getcurrentuser, normaliseuser, is_in_groups
%if is_in_groups(normaliseuser(getcurrentuser()), settings.ADMINGROUPS):
<tr><td class=field_name></td><td class=field_value align=right><a href={{settings.PREFIX}}/user/{{username}}><button>Редактировать</button></a></td></tr>
%end
<tr>
	<td class=field_name>Дисковая квота:</td>
	<td class=field_value>
		<table>
		<tr><td class=field_name>использовано:</td><td class=field_value align=right>{{quotaused}}</td><td class=field_value>Кб</td></tr>
		<tr><td class=field_name>доступно:</td><td class=field_value align=right>{{quotaavail}}</td><td class=field_value>Кб</td></tr>
		</table><br>
        %include quotatable used=quotaused, quota=quotaavail
	</td>
</tr>
<tr>
	<td class=field_name>Группы:</td>
	<td class=field_value>
		<table><tr>
		%k=0
		%for i in groups:
			<td class=field_value width=20%>{{i}}</td>
		%k = k + 1
		%if k % 5 == 0:
			</tr><tr>
		%end
		%end 
	</tr></table>
	</td></tr>
<tr>
	<td class=field_name>Выдан:</td>
	<td class=field_value>N/A</td></tr>
<tr>
	<td class=field_name>Вход выполнен:</td>
	<td class=field_value>N/A</td>
</tr>
<tr>
    <td class=field_name>Последний пароль:</td>
    <td class=field_value>
        <table>
            <tr><td class=field_name>Пароль:</td><td class=field_value>{{password}}</td></tr>
            <tr><td class=field_name>Применён:</td><td class=field_value align=center>
            %if applied:
            ✅
            %else:
            ❎
            %end
            </td></tr>
        </table>
    </td>
</tr>
</table>

%include menu username =username
%include footer
