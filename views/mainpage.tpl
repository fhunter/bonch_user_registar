%include header
<h1>Информация о пользователях и сброс паролей</h1>
<form method="post" action="./" name="usersearch">
Ключ поиска:<input type="text" name="searchkey">
<input type="submit" value="Submit">
</form>
% if defined('query'):
<table><tr><td class=field_name>Имя пользователя</td><td class=field_name>ФИО</td><td class=field_name>Номер студ билета</td></tr>
	%for i in query:
		<tr><td class=field_value><a href="./uinfo/{{unicode(i[0])}}">{{unicode(i[0])}}</a></td><td class=field_value>{{unicode(i[1])}}</td><td class=field_value>{{unicode(i[2])}}</td></tr>
	%end
</table>
% end
<br>
%include menu
%include footer
