%import settings
<a href={{ settings.PREFIX }}/><button>На главную</button></a>
<a href={{ settings.PREFIX }}/listreset><button>Очередь сброса</button></a>
<a href={{ settings.PREFIX }}/listoverquota><button>С превышением квоты</button></a>
<a href={{ settings.PREFIX }}/resetstats><button>Статистика</button></a>
<a href={{ settings.PREFIX }}/groups><button>Группы</button></a>
% if defined ('username'):
	<a href={{ settings.PREFIX }}/reset/{{username}}><button>Сбросить пароль</button></a>
% end
%import os
<div style="float: right; padding: 1px;margin: 1px; border-radius: 6px">{{ os.environ.get("REMOTE_USER") }}</div>
