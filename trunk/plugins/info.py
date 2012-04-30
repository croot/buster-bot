# -*- coding: utf-8 -*-

WHO_JOIN = {}

def hnd_who_join(type, source, parameters):
    global WHO_JOIN
    if not source[1] in GROUPCHATS:
        return
    day=time.localtime()[2]
    if not day in WHO_JOIN:
        reply(type, source, u'Нет статистики')
        return
    if not source[1] in WHO_JOIN[day]:
        reply(type, source, u'Нет статистики')
        return
    rep=[]
    for x in WHO_JOIN[day][source[1]]:
        y=unicode(x[:20])+' ('+str(WHO_JOIN[day][source[1]][x])+')'
        rep.append(y)
    if not rep:
        reply(type, source, u'Нет статистики!')
        return
    if len(rep)>3000:
        rep=rep[:3000]+'>>>'
    if type not in ['chat','private']:
        reply(type, source, u'Смотри в привате!')
    reply('chat', source, str(len(rep))+':\n'+', '.join(rep))
        

def hnd_stat_l(g, n, a, b):
    global WHO_JOIN
    if not g in GROUPCHATS:
        return
    day=time.localtime()[2]
    if not day in WHO_JOIN:
        WHO_JOIN[day]={}
    if not g in WHO_JOIN[day]:
        WHO_JOIN[day][g]={}
    WHO_JOIN[day][g][n]=time.ctime().split()[3]

def get_thr_list():
	thr_list = []
	enu_list = threading.enumerate()
	for thread in enu_list:
		thr_name = thread.getName()
		splthr = thr_name.split('.')
		
		if len(splthr) == 1:
			thr_list.append(u'%d) "%s".' % (enu_list.index(thread)+1,thr_name))
		elif len(splthr) == 5:
			thr_list.append(u'%d) "%s" из "%s" в %s:%s:%s.' % (enu_list.index(thread)+1,splthr[0],splthr[1],splthr[2],splthr[3],splthr[4]))
		else:
                    thr_list.append(str(enu_list.index(thread)+1)+') "'+thr_name+'".')
				
	return (len(enu_list),thr_list)

def handler_thr_show(type, source, parameters):
	thr_list_get = get_thr_list()
	count = thr_list_get[0]
	thr_list = thr_list_get[1]	
	rep = u'Список активных потоков (всего: %d):\n\n%s' % (count,'\n'.join(thr_list))
	reply(type, source, rep)

def stats_handler(t, s, p):
    if p:
        pass
    else:
        p=JABBER_ID.split('@')[1]
    packet = IQ(JAB, 'get')
    query = packet.addElement('query', 'http://jabber.org/protocol/stats')
    query.addElement('stat').__setitem__('name', 'users/total')
    query.addElement('stat').__setitem__('name', 'users/online')
    packet.addCallback(stats_result_handler, t, s, p)
    reactor.callFromThread(packet.send, p)


def stats_result_handler(t, s, p, x):
 if x['type'] == 'result':
  query = element2dict(x)['query']
  r = {}
  if not query.children:
      reply(t, s, u'Невозможно получить информацию!')
      return
  for i in query.children:
   r[i['name']] = i['value']
  reply(t, s, p+':\nusers/total: '+r.get('users/total', '?')+'\nusers/online: '+r.get('users/online', '?'))
 elif x['type'] == 'error':
  reply(t, s, u'Невозможно получить информацию!')


register_command_handler(handler_thr_show, 'потоки', ['инфо','админ','все'], 20, 'Показывает активные потоки бота', 'потоки', ['потоки'])
register_command_handler(stats_handler, 'инфа', ['инфо','админ','все'], 0, 'Возвращает статистику о сервере юзая XEP-0039.', 'инфа сервер', ['инфа talkonaut.com'])
register_leave_handler(hnd_stat_l)
register_command_handler(hnd_who_join, 'хтобыл', ['все'], 0, 'Статистика конференции', 'хтобыл', ['хтобыл'])

        
    
