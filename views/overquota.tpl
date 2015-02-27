%include header
<h1>Превысившие квоту</h1>
<table><tr><td class=field_name>Пользователь</td><td class=field_name>Квота</td><td class=field_name>Использовано</td><td class=field_name>Доступно</td></tr>
% for i in quotas:
#		userinfo = getuser(i[0])
#		quota = int(userinfo["quota"])
#		useddisk = int(userinfo["useddiskspace"])
#		image_file = makequota_image(useddisk,quota,True)
<tr>
	<td class=field_value><a href=./?page=getuser&getuser=%s>%s</a></td>
	<td class=field_value>%s</td>
	<td class=field_value>%s</td>
	<td class=field_value>%s</td>
</tr>""" % (i[0],i[0],image_file,useddisk,quota)
%end
</table>

%include menu
%include footer
