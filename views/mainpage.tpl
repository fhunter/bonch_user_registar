%include header
%import settings
%from utils import getcurrentuser, is_in_groups
<h1>Информация о пользователях и сброс паролей</h1>
% if is_in_groups(getcurrentuser(), settings.ADMINGROUPS):
<form method="post" action="{{ settings.PREFIX }}/" name="usersearch">
Ключ поиска:<input type="text" name="searchkey">
<input type="submit" value="Submit">
</form>
% if defined('query'):
<table><tr><td class=field_name>Имя пользователя</td><td class=field_name>ФИО</td><td class=field_name>Номер студ билета</td></tr>
	%for i in query:
		<tr><td class=field_value><a href="{{ settings.PREFIX }}/uinfo/{{i.username}}">{{i.username}}</a></td><td class=field_value>{{i.fio}}</td><td class=field_value>{{i.studnum}}</td></tr>
	%end
</table>
% end
% end
<br>
%include menu
%include footer
