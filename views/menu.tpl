%import settings
%from bottle import request
<a href={{ settings.PREFIX }}/><button>На главную</button></a>
<a href={{ settings.PREFIX }}/listreset><button>Очередь сброса</button></a>
<a href={{ settings.PREFIX }}/listoverquota><button>С превышением квоты</button></a>
<a href={{ settings.PREFIX }}/resetstats><button>Статистика</button></a>
<a href={{ settings.PREFIX }}/groups><button>Группы</button></a>
% if defined ('username'):
	<a href={{ settings.PREFIX }}/reset/{{username}}><button>Сбросить пароль</button></a>
% end
<div style="float: right; padding: 1px;margin: 1px; border-radius: 6px">{{ request.environ.get("REMOTE_USER") }}</div>
