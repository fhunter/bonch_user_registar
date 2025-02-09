%include header
%import settings
<h1>Git репозитории</h1>
<h2>Репозитории без владельцев</h2>
<table><tr><td class=field_name>Пользователь</td><td class=field_name>Репозиторий</td></tr>
%for i in repos:
<tr>
    <td class=field_value><a href={{ settings.PREFIX }}/uinfo/{{i["username"]}}>{{i["username"]}}</a></td>
    <td class=field_value>{{i["repo_name"]}}</td>
</tr>
%end
</table>

%include menu
%include footer
