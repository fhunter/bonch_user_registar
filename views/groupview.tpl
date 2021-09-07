%include header
<h1>Просмотр группы</h1>
<h2>{{groupname}}</h2>
%for i in users:
<a href=./uinfo/{{i}}>{{i}}</a></br>
%end
<br>
%include menu
%include footer
