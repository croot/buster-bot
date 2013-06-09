# -*- coding: utf-8 -*-

WHO_JOIN = {}

def hnd_day_of_week(t, s, p):
    R = [u'Кабуча',u'Понедельник',u'Вторник',u'Среда',u'Четверг',u'Пятницо',u'Суббота',u'Воскресенье']
    from datetime import date
    if not p:
        c = time.localtime()
        reply(t, s, u'Сегодня '+R[datetime.date(c[0], c[1], c[2]).isoweekday()])
    else:
        if len(p.split())!=3:
            reply(t, s, u'Укажите год месяц день в числовом формате через пробел!')
        else:
            ss = p.split()
            try: reply(t, s, ss[0]+'-'+ss[1]+'-'+ss[2]+u' '+R[datetime.date(int(ss[0]), int(ss[1]), int(ss[2])).isoweekday()])
            except: reply(t, s, u'Хрень какаято..')

register_command_handler(hnd_day_of_week, 'dayweek', ['инфо','все'], 0, 'Показывает день недели по дате', 'dayweek <год> <месяц> <число>', ['dayweek 1980 11 12'])

def hnd_port_tel(t, s, p):
    if not p or not p.count(' '):
        reply(t, s, u'adres port1 port2 ...')
        return
    list = p.split()
    ports = p.split()[1:]
    rep = list[0]+':\n'
    for x in ports:
        if not x.isdigit():
            reply(t, s, 'wrong port parameters '+x)
            break
        rep+= x
        if check_server(list[0], int(x)):
            rep+=' on\n'
        else:
            rep+=' off\n'
    reply(t, s, rep)

register_command_handler(hnd_port_tel, 'port', ['все'], 0, 'Проверяет порт на подключение', 'port adres port', ['port qip.ru 5222'])
    

def check_server(address, port):
	# Create a TCP socket
	s = socket.socket()
	s.settimeout(2)
	#print "Attempting to connect to %s on port %s" % (address, port)
	try:
		s.connect((address, port))
		#print "Connected to %s on port %s" % (address, port)
		s.close()
		return True
	except socket.error, e:
		#print "Connection to %s on port %s failed: %s" % (address, port, e)
		return False


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
    list = sorted(WHO_JOIN[day][source[1]].iteritems(), key=operator.itemgetter(1))
    list.reverse()
    list = [x for x in list if x[0] in GROUPCHATS[source[1]] and not GROUPCHATS[source[1]][x[0]]['ishere']]
    rep=[]
    for x in list:
        y=unicode(x[0][:20])+' ('+x[1]+')'
        rep.append(y)
    if not rep:
        reply(type, source, u'Нет статистики!')
        return
    if len(rep)>3000:
        rep=rep[:3000]+'>>>'
    if type not in ['chat','private']:
        reply(type, source, u'Смотри в привате!')
    now = len([x for x in GROUPCHATS[source[1]] if x!=get_bot_nick(source[1]) and GROUPCHATS[source[1]][x]['ishere']])
    reply('chat', source, str(time.localtime()[0])+'-'+str(time.localtime()[1])+'-'+str(time.localtime()[2])+u' тут было '+str(len(rep))+u' юзеров:\n'+'\n'.join(rep)+'\n'+(str(now)+u' еще здесь.' if now else u''))
        

def hnd_stat_l(g, n, a, b, cljid):
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
    if not p:
        p=s[3].split('@')[1]
    packet = IQ(CLIENTS[s[3]], 'get')
    query = packet.addElement('query', 'http://jabber.org/protocol/stats')
    query.addElement('stat').__setitem__('name', 'users/total')
    query.addElement('stat').__setitem__('name', 'users/online')
    packet.addCallback(stats_result_handler, t, s, p)
    reactor.callFromThread(packet.send, p)

gog=None

def stats_result_handler(t, s, p, x):
    global gog
    gog=x
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

        
    
