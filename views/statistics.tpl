%include header
<h1>Статистика сброса пароля</h1>
<table><tr><td class=field_name>Всего пароли сброшены:</td><td class=field_value> {{count}} раз</td></tr>
<tr><td class=field_name>В очереди на сброс паролей</td><td class=field_value> {{requests}} запросов</td></tr>
% if defined('date'):
<tr><td class=field_name>Последний выполненный запрос пришёл</td><td class=field_value> {{date}}
% else:
<tr><td class=field_name>Выполненных запросов</td><td class=field_value> не найдено
% end
</td></tr></table>
%if defined('frequency'):
<h2>Наиболее часто сбрасываемые пароли</h2><br>
<table><tr><td class=field_name>Пользователь</td><td class=field_name>сброшен</td></tr>
%for i in frequency:
<tr><td class=field_value>{{i[0]}}</td><td class=field_value>{{i[1]}} раз</td></tr>
%end
</table>
%end
%if defined('topresets'):
<h2>Top 10 лаборантов чаще всего сбрасывавших пароли</h2><br>
<table><tr><td class=field_name>Пользователь</td><td class=field_name>сбросил</td></tr>
%for i in topresets:
<tr><td class=field_value>{{i[0]}}</td><td class=field_value>{{i[1]}} раз</td></tr>
%end
</table>
%end

%include menu
%include footer
