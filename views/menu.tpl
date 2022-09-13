<a href=./><button>На главную</button></a>
<a href=./listreset><button>Очередь сброса</button></a>
<a href=./listoverquota><button>С превышением квоты</button></a>
<a href=./resetstats><button>Статистика</button></a>
<a href=./groups><button>Группы</button></a>
% if defined ('username'):
	<a href=./reset/{{username}}><button>Сбросить пароль</button></a>
% end
%import os
<div style="float: right; padding: 1px;margin: 1px; border-radius: 6px">{{ os.environ["REMOTE_USER"] }}</div>
