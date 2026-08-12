%include('header')
%import settings
<h1>Git репозитории</h1>
<h2>Удалённые пользователи<h2>

<table>
    <tr><td class=field_name>Пользователь</td><td class=field_name>Репозитории</td><td class=field_name>Организации</td></tr>
%for i in users:
    <tr>
    <td class=field_value><a href="https://gitea.pivt.spbgut.ru/{{i}}/">{{i}}</a></td>
    <td class=field_value>
%for j in users[i]["repos"]:
        <a href="https://gitea.pivt.spbgut.ru/{{i}}/{{j}}/">{{j}}</a> <a href="https://gitea.pivt.spbgut.ru/-/admin/repos?q={{i["repo_name"]}}&sort=recentupdate">{{j}}</a>
%end
    </td>
    <td class=field_value>
%for j in users[i]["orgs"]:
        <a href="https://gitea.pivt.spbgut.ru/{{j}}/">{{j}}</a><br/>
%end
    </td>
    </tr>
%end
</table>

%include('menu')
%include('footer')
