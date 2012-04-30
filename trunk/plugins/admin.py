# -*- coding: utf-8 -*-

from twisted.internet.reactor import callFromThread

def hnd_restart(type, source, parameters):
    reply(type, source, u'ok')
    p = domish.Element(('jabber:client', 'presence'))
    p['type'] = 'unavailable'
    p.addElement('status').addContent(u'Рестарт: Admin')
    reactor.callFromThread(dd, p)
    reactor.stop()
    time.sleep(2)
    os.execl(sys.executable, sys.executable, sys.argv[0])

def hnd_login(type, source, parameters):
    jid = get_true_jid(source)
    if parameters.strip() == ADMIN_PASSWORD:
        GLOBACCESS[jid]=100
	reply('chat', source, u'пароль принят, глобальный полный доступ выдан')
    else:
        reply('chat', source, u'неверный пароль')
	
def hnd_logout(type, source, parameters):
	jid = get_true_jid(source)
	if jid in GLOBACCESS:
            del GLOBACCESS[jid]
            reply(type, source, u'доступ снят')

def hnd_off(type, source, parameters):
    reply(type, source, u'Выключаюсь!')
    reactor.stop()
    os.abort()

def hnd_wherei(type, source, parameters):
    rep=''
    n=0
    list=[]
    if len(GROUPCHATS)>0:
        for x in GROUPCHATS:
            n=0
            if len(GROUPCHATS[x])==0:
                list.append(x)
            for c in GROUPCHATS[x]:
                if GROUPCHATS[x][c]['ishere']:
                    n+=1
            rep+=x+' ('+str(n)+')\n'
        if list:
            rep+=u'Бот не смог войти в следующие конференции '+', '.join(list)+u' чтобы удалить их используйте proper'
    reply(type, source, u'Я сижу в '+str(len(GROUPCHATS))+u' комнатах.\n'+rep)

def hnd_proper(t, s, p):
    import shutil
    i=[x for x in GROUPCHATS.keys() if len(GROUPCHATS[x])==0]
    if i:
        txt=eval(read_file('dynamic/chatroom.list'))
        for x in i:
            del GROUPCHATS[x]
            if x in txt:
                del txt[x]
            try:
                shutil.rmtree('dynamic/'+x)
            except:
                pass
        write_file('dynamic/chatroom.list', str(txt))
        reply(t, s, u'Были удалены: '+', '.join(i))
            
def hnd_join(type, source, parameters):
    file = 'dynamic/chatroom.list'
    if not parameters:
        return
    jid=get_true_jid(source[1]+'/'+source[2])
    parameters=parameters.lower()
    if not parameters.count('.'):
        parameters=parameters+'@conference.jabber.ru'
    try: os.path.exists(parameters)
    except:
        reply(type, source, u'На сервере скорее всего не настроен юникод, русские символы недопустимы!')
        return
    db=eval(read_file(file))
    db[parameters]={'nick':DEFAULT_NICK, 'status':'', 'show':''}
    write_file(file, str(db))
    callback=source[1]+'/'+source[2]
    if type in ['groupchat','public'] and source[1] in GROUPCHATS:
        callback=source[1]
    JOIN_CALLBACK[parameters]=callback
    join(parameters, DEFAULT_NICK)

def hnd_j2j(type, source, parameters):
    if not J2J:
        reply(type, source, u'j2j транспорт не указан в конфигураторе!')
        return
    parameters=parameters.replace('@','%')
    parameters=parameters+'@'+J2J
    hnd_join(type, source, parameters)

def hnd_leave(type, source, parameters):
    if not parameters and not source[1] in GROUPCHATS:
        return
    level = int(user_level(source[1]+'/'+source[2], source[1]))
    file = 'dynamic/chatroom.list'
    if not parameters:
        db=eval(read_file(file))
        if source[1] in db:
            del db[source[1]]
            write_file(file, str(db))
        if source[1] in GROUPCHATS:
            del GROUPCHATS[source[1]]
        leave(source[1],u'Меня увидит '+source[2])
    else:
        parameters=parameters.lower()
        if level<40:
            reply(type, source, u'Для вывода бота из другой конференции нужен доступ!')
            return
        if not parameters.count('@con'):
            parameters=parameters+'@conference.jabber.ru'
        db=eval(read_file(file))
        if not parameters in db and not parameters in GROUPCHATS:
            reply(type, source, u'Меня там нет!')
            return
        if parameters in db:
            del db[parameters]
            write_file(file, str(db))
        if parameters in GROUPCHATS:
            del GROUPCHATS[parameters]
        leave(parameters)

def hnd_botstatus(type, source, parameters):
    if not source[1] in GROUPCHATS:
        return
    db=eval(read_file(file))
    

def hnd_botup(type, source, parameters):
    rep=u'Я работаю без падений '+timeElapsed(time.time()-INFO['start'])+'\n'
    rep+=u'Получено сообщений ICQ '+str(INFO['imsg'])+'\n'
    rep+=u'Сообщений XMPP '+str(INFO['jmsg'])+'\n'
    rep+=u'Отправлено сообщений всего '+str(INFO['out'])+'\n'
    #rep+=u'Запросов на авторизацию '+str(INFO['auth'])+'\n'
    rep+=u'Входящий траффик '+str(INFO['tin']/1024)+' kb\n'
    rep+=u'Исходящий '+str(INFO['tout']/1024)+' kb\n'
    rep+=u'Ошибок '+str(INFO['err'])+'\n'
    rep+=u'Всего было запущено потоков '+str(INFO['thr'])+'\n'
    rep+=u'Активно на данный момент '+str(len(threading.enumerate()))
    reply(type, source, rep)

def moderate_set(t, s, p, jn, jid_nick, ra, set_to, reason):
    d = moderate(s, jn, jid_nick, ra, set_to, reason)
    d.addCallback(moderate_result_handler, t, s, p)

def moderate_result_handler(x, t, s, p):
    if x['type'] == 'result': reply(t, s, u'Сделано!')
    else: reply(t, s, u'Выполнение невозможно!')

def moderate(s, jn, jid_nick, ra, set_to, reason=None):
    if not reason:
        try: reason = get_bot_nick(s[1])
        except: reason = ''
    packet = IQ(JAB, 'set')
    query = packet.addElement('query', 'http://jabber.org/protocol/muc#admin')
    i = query.addElement('item')
    i[jn] = jid_nick
    i[ra] = set_to
    i.addElement('reason').addContent(reason)
    d = Deferred()
    packet.addCallback(d.callback)
    callFromThread(packet.send, s[1])
    return d

def ban(groupchat, jid):
    room_access(groupchat, 'affiliation', 'outcast', 'jid', jid)

def unban(groupchat, jid):
    room_access(groupchat, 'affiliation', 'none', 'jid', jid)

def room_access(groupchat, aff_role, par_one, jid_nick, par_two):
    q = domish.Element(('jabber:client', 'iq'))
    q['type'] = 'set'
    q['id'] = str(random.randrange(1,999))
    q['to'] = groupchat
    query = q.addElement('query', 'http://jabber.org/protocol/muc#admin')
    i = query.addElement('item')
    i[aff_role] = par_one
    i[jid_nick] = par_two
    JAB.send(q)

def hnd_unban(t, s, p):
    if not s[1] in GROUPCHATS or not p: return
    jid = p
    if p in GROUPCHATS[s[1]]:
        jid = GROUPCHATS[s[1]]['jid']
    moderate_set(t, s, jid, 'affiliation', 'none', 'jid', jid, s[2])
    

def hnd_ban(type, source, parameters):
    if not source[1] in GROUPCHATS:
        return
    if parameters:
        if parameters.count(' '):
            parameters=parameters.split()[0]
        nicks=GROUPCHATS[source[1]]
        if parameters in nicks:
            moderate_set(type, source, parameters, 'affiliation', 'outcast', 'nick', parameters, source[2])
    else:
        reply(type, source, u'Кого?')

def hnd_member(type, source, parameters):
    if not source[1] in GROUPCHATS:
        return
    if parameters:
        if parameters.count('@') and parameters.count('.'):
            jid = parameters
        else:
            jid = get_true_jid(source[1]+'/'+parameters)
            if not jid:
                reply(type, source, u'А есть такой?')
                return
        moderate_set(type, source, parameters, 'affiliation', 'member', 'jid', jid, source[2])
    
def hnd_participant(type, source, parameters):	
	if parameters:
            moderate_set(type, source, parameters, 'role', 'participant', 'nick', parameters, source[2])

def hnd_owner(type, source, parameters):
        jid = None
        if source[1] in GROUPCHATS:
            if parameters:
                if parameters.count('@') and parameters.count('.'):
                    jid = parameters
                else:
                    jid=get_true_jid(source[1] + '/' + parameters)
                if not jid:
                    reply(type, source, u'А есть такой?')
                    return    
                moderate_set(type, source, parameters, 'affiliation', 'owner', 'jid', jid, source[2])

def hnd_kick(type, source, parameters):
    if not source[1] in GROUPCHATS:
        return
    if parameters:
        if not parameters in GROUPCHATS[source[1]]:
            reply(type, source, u'А есть такой?')
            return
        moderate_set(type, source, parameters, 'role', 'none', 'nick', parameters, source[2])

def hnd_visitor(type, source, parameters):
    if not source[1] in GROUPCHATS:
        return
    if parameters:
        if not parameters in GROUPCHATS[source[1]]:
            reply(type, source, u'А есть такой?')
            return
        moderate_set(type, source, parameters, 'role', 'visitor', 'nick', parameters, source[2])

def hnd_clear(type, source, parameters):
    if not source[1] in GROUPCHATS:
        return
    for x in range(1, 21):
        time.sleep(1.3)
        msg(source[1], '')
    time.sleep(1)
    reply('chat', source, u'Очищено!')

def hnd_globmsg(type, source, parameters):
    if not GROUPCHATS or not parameters:
        return
    for x in GROUPCHATS:
        msg(x, u'Новости от Admin:\n'+parameters)
    reply(type, source, u'Отправлено в '+str(len(GROUPCHATS))+u' конференций!')

def hnd_botnick(type, source, parameters):
    if not source[1] in GROUPCHATS or not parameters:
        return
    if len(parameters)>21:
        reply(type, source, u'Напиши ник по короче!')
        return
    file = 'dynamic/chatroom.list'
    db=eval(read_file(file))
    if source[1] in db.keys():
        db[source[1]]['nick']=parameters
        write_file(file, str(db))
    join(source[1],parameters)

def hnd_botstatus(type, source, parameters):
    if not source[1] in GROUPCHATS:
        return
    if not parameters or len(parameters)>250:
        return
    show='chat'
    status=parameters
    if parameters.count(' ') and parameters.split()[0] in [u'chat',u'dnd',u'away',u'xa']:
        show=parameters.split()[0]
        status=' '.join(parameters.split()[1:])
    db=eval(read_file('dynamic/chatroom.list'))
    if source[1] in db.keys():
        db[source[1]]['show']=show
        db[source[1]]['status']=status
        write_file(file, str(db))
    join(source[1], get_bot_nick(source[1]))

if not 'inspect' in globals():
        import inspect

def hnd_find_plugin(type, source, parameters):
    if not parameters: return
    if not parameters.lower() in COMMANDS:
        reply(type, source, u'Такой команды не существует!')
        return
    cmd=COMMAND_HANDLERS[parameters.lower()]
    file=inspect.getfile(cmd)
    size=str(os.path.getsize(file)//1024)+'Kb.'
    last=timeElapsed(time.time()-os.path.getmtime(file))
    name=cmd.func_name
    reply(type, source, u'Информация о команде \"'+parameters.lower()+u'\":\n Файл:'+file+u'\nИмя функции:'+name+u'\nВремя последнего изменения:\n'+last+u'\nРазмер всего плагина:'+size)

def hnd_remote_cmd(t, s, p):
    par=''
    if not p.count(' ')>1:
        reply(t, s, u'Синтаксис: чат команда параметры')
        return
    ss=p.split()
    #0-chat,1-command,2-par
    chat=ss[0].lower()
    if not chat in GROUPCHATS:
        reply(t, s, u'Меня там нет!')
        return
    if chat==s[1]:
        reply(t, s, u'И зачем?')
        return
    cmd=ss[1].lower()
    if not cmd in COMMANDS:
        reply(t, s, u'Нет такой команды!')
        return
    par=' '.join(ss[2:])
    ajid=random.choice(ADMINS)
    ba=u'botadmin'
    GROUPCHATS[chat][ba]={'stmsg':'','status':'','ishere':1,'jid':ajid,'joined':time.time(),'idle':time.time()}
    call_command_handlers(cmd, 'private', [chat+'/'+ba, chat, ba], par)
    del GROUPCHATS[chat][ba]
    reply(t, s, u'Выполнено!')

def hnd_say(t, s, p):
    if not p or not s[1] in GROUPCHATS: return
    msg(s[1], p)

def hnd_wtf(t, s, p):
    rep=INFO['tlasterr']['err']
    i=timeElapsed(time.time()-INFO['tlasterr']['t'])
    if not rep:
        reply(t, s, u'Нет исключений!')
        return
    try:
        if not isinstance(rep, unicode):
            rep=rep.decode('utf-8','replace')
        reply(t, s, i+':\n'+rep)
    except:
        reply(t, s, i+':\n'+re.compile(r'[A-Za-z]+',re.DOTALL).search(rep).group(0))

def handler_getrealjid(type, source, parameters):
	groupchat=source[1]
	if GROUPCHATS.has_key(groupchat):
		nicks = GROUPCHATS[groupchat].keys()
		nick = parameters.strip()
		if not nick in nicks:
			reply(type,source,u'ты уверен, что <'+nick+u'> был тут?')
			return
		else:
			jidsource=groupchat+'/'+nick
			if get_true_jid(jidsource) == 'None':
				reply(type, source, u'я ж не модер')
				return
			truejid=get_true_jid(jidsource)
			if type == 'public':
				reply(type, source, u'ушёл')
		reply('private', source, u'реальный жид <'+nick+u'> --> '+truejid)

register_command_handler(hnd_unban, 'унбан', ['админ','мук','все'], 20, 'Достает из бани ник/жид', 'унбан <jid>', ['унбан d@jab.ua'])
register_command_handler(hnd_unban, 'никто', ['админ','мук','все'], 20, 'Устанавливает на jid affiliation <none>', 'никто <jid>', ['никто d@jab.ua'])
register_command_handler(handler_getrealjid, 'тружид', ['инфо','админ','мук','все'], 20, 'Показывает реальный жид указанного ника. Работает только если бот модер ессно', 'тружид <ник>', ['тружид guy'])
register_command_handler(hnd_proper, 'proper', ['все'], 40, 'Удаляет конференции в которые не смог войти бот.', 'proper', ['proper'])        
register_command_handler(hnd_wtf, 'wtf', ['все'], 10, 'Выводит последнюю ошибку бота.', 'wtf', ['wtf'])        
register_command_handler(hnd_say, 'сказать', ['все'], 20, 'Сказать что-то от имени бота.', 'сказать <текст>', ['сказать пук'])        
register_command_handler(hnd_remote_cmd, 'ремоут', ['все'], 100, 'Дистанционное выполнение команды в любой из конференций где находится бот.', 'ремоут <чат> <команда> <параметры>', ['ремоут cool@conference.talkonaut.com сказать посоны привет'])        
register_command_handler(hnd_find_plugin, '!плагин', ['все'], 20, 'Информация об определенной команде, о плагине в котором содержиться ее код.', '!плагин <команда>', ['!плагин пинг'])        
register_command_handler(hnd_botstatus, 'ботстатус', ['все'], 20, 'Устанавливает статус бота в конференции.', 'ботстатус <презенс статус> <текст>', ['ботстатус away скоро вернусь'])        
register_command_handler(hnd_botnick, 'ботник', ['все'], 20, 'Меняет ник бота в конференции.', 'ботник <ник>', ['ботник вася'])    
register_command_handler(hnd_globmsg, 'globmsg', ['админ','все'], 100, 'Сообщение во все комнаты где бот.', 'globmsg <body>', ['globmsg test'])    
register_command_handler(hnd_restart, 'рестарт', ['админ','все'], 100, 'Рестарт', 'рестарт', ['рестарт'])    
register_command_handler(hnd_wherei, 'хдея', ['админ','все'], 0, 'Показывает комнаты в которых сидит бот', 'хдея', ['хдея'])    
register_command_handler(hnd_off, 'пшёл', ['админ','все'], 100, 'Выключение бота', 'пшёл', ['пшёл'])    
register_command_handler(hnd_owner, 'овнер', ['админ','все'], 30, 'Дает овнера определенному нику или JID-у', 'овнер <nick>', ['овнер Guy'])
register_command_handler(hnd_botup, 'ботап', ['админ','все'], 0, 'Статистика работы бота', 'ботап', ['ботап'])
register_command_handler(hnd_ban, 'бан', ['админ','все'], 20, 'Бан юзера/сервера', 'бан <nick>', ['бан Guy'])
register_command_handler(hnd_participant, 'войс', ['админ','все'], 15, 'Даёт посетителю право голоса', 'войс <nick>', ['войс Guy'])		
register_command_handler(hnd_kick, 'кик', ['админ','все'], 15, 'Выгнать посетителя из комнаты', 'кик <nick>', ['кик Guy'])
register_command_handler(hnd_visitor, 'девойс', ['админ','все'], 15, 'Лишает посетителя голоса', 'девоис <nick>', ['девоис Guy'])
register_command_handler(hnd_member, 'мембер', ['админ','все'], 20, 'Делает юзера постоянным участником по jid-y или нику', 'мембер <nick>', ['мембер Guy'])			
register_command_handler(hnd_join, 'зайти', ['админ','все'], 40, 'Зайти в конфу', 'зайти чат', ['зайти cool@conference.talkonaut.com'])			
register_command_handler(hnd_j2j, 'j2j', ['админ','все'], 40, 'Зайти в конфу через транспорт j2j', 'j2j чат', ['j2j cool@conference.talkonaut.com'])			
register_command_handler(hnd_leave, 'свал', ['админ','все'], 20, 'Выйти с конференции', 'свал чат', ['свал cool@conference.talkonaut.com','свал'])			
register_command_handler(hnd_clear, 'чисть', ['админ','все'], 0, 'Чистит конфу', 'чисть', ['чисть'])			
register_command_handler(hnd_login, 'логин', ['доступ','админ','все'], 0, 'Авторизоваться как админиcтратор бота. Использовать только в привате!', 'логин <пароль>', ['логин мой_пароль'])
register_command_handler(hnd_logout, 'логаут', ['доступ','админ','все'], 0, 'Снять авторизацию.', 'логаут', ['логаут'])

