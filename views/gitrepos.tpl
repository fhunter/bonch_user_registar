%include header
%import settings
<h1>Git репозитории</h1>
<h2>Удалённые пользователи<h2>

<table>
    <tr><td class=field_name>Пользователь</td></tr>
%for i in users:
    <tr><td class=field_value><a href="https://gitea.pivt.spbgut.ru/{{i}}/">{{i}}</a></td></tr>
%end
</table>

<h2>Репозитории без владельцев</h2>
<table>
    <tr><td class=field_name>Пользователь</td><td class=field_name>Репозиторий</td></tr>
%for i in repos:
    <tr>
        <td class=field_value><a href="https://gitea.pivt.spbgut.ru/{{i["username"]}}/">{{i["username"]}}</a></td>
        <td class=field_value><a href="https://gitea.pivt.spbgut.ru/-/admin/repos?q={{i["repo_name"]}}&sort=recentupdate">{{i["repo_name"]}}</a></td>
    </tr>
%end
</table>

%include menu
%include footer
