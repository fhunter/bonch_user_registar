%import settings
%from bottle import request
%from utils import getcurrentuser, is_in_groups
<a href={{ settings.PREFIX }}/><button>На главную</button></a>
% if is_in_groups(getcurrentuser(), settings.ADMINGROUPS):
<a href={{ settings.PREFIX }}/listreset><button>Очередь сброса</button></a>
<a href={{ settings.PREFIX }}/listoverquota><button>С превышением квоты</button></a>
<a href={{ settings.PREFIX }}/resetstats><button>Статистика</button></a>
<a href={{ settings.PREFIX }}/groups><button>Группы</button></a>
% if defined ('username'):
	<a href={{ settings.PREFIX }}/reset/{{username}}><button>Сбросить пароль</button></a>
% end
% end
<a href={{ settings.PREFIX }}/user/><button>Текущий пользователь</button></a>
<div class="userid">{{ getcurrentuser() }}</div>
