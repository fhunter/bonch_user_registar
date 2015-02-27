<a href=./><button>На главную</button></a>
<a href=./listreset><button>Очередь сброса</button></a>
<a href=./listoverquota><button>С превышением квоты</button></a>
<a href=./resetstats><button>Статистика</button></a>
% if defined ('username'):
	<a href=./reset/{{username}}><button>Сбросить пароль</button></a>
% end
