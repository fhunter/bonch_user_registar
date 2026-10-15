%from utils import get_used_percent, get_available_percent, get_availablehard_percent
<table id="quotatable_u" width=514px height=17px>
<tr>
<td bgcolor="red" width={{get_used_percent(quota,hardquota,used)}}%></td>
<td bgcolor="white" width=*></td>
</tr>
</table>
<table id="quotatable_d" width=514px height=17px>
<tr>
<td bgcolor="lime" width={{get_available_percent(quota,hardquota,used)}}%></td>
<td bgcolor="orange" width={{get_availablehard_percent(quota,hardquota,used)}}%></td>
<td bgcolor="white" width=*></td>
</tr>
</table>

