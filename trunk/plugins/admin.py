# -*- coding: utf-8 -*-

from twisted.internet.reactor import callFromThread
import datetime

TRAF_FROM_MUC = {}

bot_start = str(datetime.datetime.today())[:-7]

DEFAUL_STATUS = u'Справка по команде ´помощь´'

def change_nick_check(muc, newnick, cl):
    chk = 0
    if muc in GROUPCHATS:
        for x in GROUPCHATS[muc]:
            if x == get_bot_nick(muc):
                break
        else:
            real_nick = [x for x in GROUPCHATS[muc].keys() if GROUPCHATS[muc][x]['jid'].split('/')[0] in CLIENTS.keys() and GROUPCHATS[muc][x]['ishere']]
            if not real_nick:
                time.sleep(5)
                if muc in GROUPCHATS:
                    change_nick_check(muc, newnick, cl)
                return
            if real_nick: real_nick = real_nick[0]
            sl = ''
            try:
                n = 0
                for c in real_nick:
                    try:
                        if c!=newnick[n]:
                            sl+=newnick[n]+' - '+c+'\n'
                        n+=1
                    except:
                        sl+='+ '+c+'\n'
            except: pass
            BOT_NICK[muc] = real_nick
            msg(cl, muc, u'/me Некоторые символы в нике изменены сервером!\n'+sl)
            file = 'dynamic/chatroom.list'
            db = eval(read_file(file))
            if not cl in db.keys(): return
            if muc in db[cl].keys():
                db[cl][muc]['nick'] = real_nick
                write_file(file, str(db))
            

def turn_byte(b):
    if b<1024:
        return str(b)+u'b'
    if b>=1024:
        b=b/1024
        if b<1024:
            return str(b)+u'Кb'
        return str(b/1024)+u'Мb'

def traf_iq_muc(iq, cl):
    try: fromjid = iq['from']
    except: return
    if not fromjid.split('/')[0] in GROUPCHATS: return
    if not fromjid.split('/')[0] in TRAF_FROM_MUC:
        TRAF_FROM_MUC[fromjid.split('/')[0]]=0
    #print 'IQ'

    TRAF_FROM_MUC[fromjid.split('/')[0]]+=sys.getsizeof(iq)

register_iq_handler(traf_iq_muc)

def traf_msg_muc(r, t, s, p):
    if not s[1] in GROUPCHATS: return
    
    if not s[1] in TRAF_FROM_MUC.keys():
        TRAF_FROM_MUC[s[1]]=0
        
    TRAF_FROM_MUC[s[1]]+=sys.getsizeof(r)

register_message_handler(traf_msg_muc)

def traf_prs_muc(prs, cl):
    try: fromjid = prs['from']
    except: return
    if not fromjid.split('/')[0] in GROUPCHATS: return
    if not fromjid.split('/')[0] in TRAF_FROM_MUC:
        TRAF_FROM_MUC[fromjid.split('/')[0]]=0

    TRAF_FROM_MUC[fromjid.split('/')[0]]+=sys.getsizeof(prs)

register_presence_handler(traf_prs_muc)

def search_in_plugincode(t, s, p):
    if not p: return
    n, rep = 0, str()
    list = [x for x in os.listdir('plugins') if x[-3:]=='.py']
    for x in list:
        try:
            f=read_file(os.path.join('plugins',x)).splitlines()
        except: continue
        for c in f:
            try:
                if c.decode('utf8','ignore').count(p):
                    n+=1
                    rep+=str(n)+') '+c+' ['+x+'] '+str(f.index(c))+'\n'
            except: pass
    if not rep:
        reply(t, s, u'Увы, ничего не нашел!')
        return
    reply(t, s, rep)

register_command_handler(search_in_plugincode, 'плагкод', ['все'], 100, 'Поиск совпадений в исходниках плагинов бота.', 'плагкод <текст>', ['плагкод print'])	


def hnd_restart(type, source, parameters):
    if parameters:
        if parameters.lower() in [u'timer',u'таймер']:
            reply(type, source, u'Рестарт через три минуты')
            p = domish.Element(('jabber:client', 'presence'))
            #p['type'] = 'unavailable'
            p.addElement('show').addContent('dnd')
            p.addElement('status').addContent(u'Плановый рестарт через: 3 минуты')
            for x in CLIENTS.keys():
                reactor.callFromThread(dd, p, CLIENTS[x])
            time.sleep(180)
            hnd_restart(type, source, str())
            return
        if parameters.lower() in [u'icq',u'ася',u'асю']:
            if 'icq_restart' in globals().keys() and UIN and ENABLE_ICQ=='1' and ICQ_PASS:
                icq_restart()
                reply(type, source, u'Перезапустил uin '+UIN)
                return
            else:
                reply(type, source, u'Проверьте конфигурацию ICQ в файле настройки!')
                return
        list = [x for x in range(10) if GENERAL_CONFIG("JABBER_ID"+str(x)).count(parameters.lower())]
        if not list:
            if GENERAL_CONFIG("JABBER_ID").count(parameters.lower()):
                a, b = GENERAL_CONFIG("JABBER_ID"), GENERAL_CONFIG("JABBER_PASS")
                reply(type, source, u'Перазапускаю '+a)
                reactor.callFromThread(JabberBot, a, b)
                return
            reply(type, source, u'Учтеная запись содержащая '+parameters.lower()+u' не найдена!')
            return
        if len(list)>1:
            reply(type, source, u'Укажите конкретнее, по совпадениям найдено несколько учтеных записей!')
            return
        istr = str(list[0])
        a, b = GENERAL_CONFIG("JABBER_ID"+istr), GENERAL_CONFIG("JABBER_PASS"+istr)
        if not b:
            reply(type, source, u'Отсутствует пароль учтеной записи!')
            return
        reply(type, source, u'Перазапускаю '+a)
        reactor.callFromThread(JabberBot, a, b)
        return
    reply(type, source, u'ok')
    p = domish.Element(('jabber:client', 'presence'))
    p['type'] = 'unavailable'
    p.addElement('status').addContent(u'Рестарт: Admin')
    for x in CLIENTS.keys():
        reactor.callFromThread(dd, p, CLIENTS[x])
    reactor.stop()
    time.sleep(2)
    os.execl(sys.executable, sys.executable, sys.argv[0])

def hnd_login(type, source, parameters):
    global GLOBACCESS
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
    p = domish.Element(('jabber:client', 'presence'))
    p['type'] = 'unavailable'
    p.addElement('status').addContent(u'System Shut Down: Admin')
    for x in CLIENTS.keys():
        reactor.callFromThread(dd, p, CLIENTS[x])
    reactor.stop()
    os._exit(1)

def hnd_wherei(type, source, parameters):
    rep=''
    n=0
    inmuc = 0
    list=[]
    txt=eval(read_file('dynamic/chatroom.list'))
    for x in txt.keys():
        if x.count('@con') or not x in CLIENTS.keys():
            continue
        ii = txt.keys().index(x)+1
        rep+='JID ['+str(ii)+'] - '+x+'\n'
        for c in txt[x].keys():
            if c in GROUPCHATS.keys():
                inmuc = len([x for x in GROUPCHATS[c].keys() if GROUPCHATS[c][x]['ishere']])
                if not inmuc:
                    list.append(c)
                rep+=c+' ('+str(inmuc)+')['+turn_byte(TRAF_FROM_MUC.get(c,0))+']\n'
    if list:
        rep+=u'Бот не смог войти в следующие конференции '+', '.join(list)+u' чтобы удалить их используйте <proper>'
    reply(type, source, u'Я сижу в '+str(len(GROUPCHATS))+u' комнатах.\n'+rep)

def hnd_proper(t, s, p):
    import shutil
    n, rem = 0, []
    list = [x for x in GROUPCHATS.keys() if len(GROUPCHATS[x])==0]
    if list:
        txt = eval(read_file('dynamic/chatroom.list'))
        for x in list:
            if not x or x.isspace():
                continue

            try: del GROUPCHATS[x]
            except: pass

            try:
                if os.path.isdir(os.path.join('dynamic',x)) and os.path.exists(os.path.join('dynamic',x)):
                    shutil.rmtree(os.path.join('dynamic',x))
                    n+=1
                    rem.append(x)
                    if "JOIN_TIMER" in globals().keys():
                        if x in JOIN_TIMER.keys():
                            del JOIN_TIMER[x]
            except: pass
            hnd_proper_cfg(list)
        reply(t, s, u'Были удалены ('+str(n)+'): \n'+', '.join(rem))
    else: reply(t, s, u'Все в порядке!')

def hnd_proper_cfg(list):
    if list:
        file = 'dynamic/chatroom.list'
        db = eval(read_file(file))
        for x in db.keys():
            try:
                for c in db[x].keys():
                    if c in list:
                        del db[x][c]
            except: continue
        write_file(file, str(db))
        

LAST_AR_DT = {}

import unicodedata

try:
    db_file('dynamic/arabic_old.txt',dict)
    arabic_old = eval(read_file('dynamic/arabic_old.txt'))
except:
    arabic_old = {}

def hnd_arabic_detect(r, t, s, p):
    if not s[1] in GROUPCHATS: return
    if not s[2] or s[2].isspace(): return
    if s[2] == get_bot_nick(s[1]): return
    global LAST_AR_DT
    global arabic_old
    
    if s[1] in arabic_old.keys():
        return
    if s[1] in LAST_AR_DT.keys(): return
    if len(p)>1 and p.split()[0].lower() in COMMANDS.keys(): return
    try:
        z=random.choice(p)
        #print unicodedata.category(z)
        if unicodedata.category(z) in ['Lo']:
            id = random.randrange(99, 9999)
            LAST_AR_DT[s[1]]={}
            LAST_AR_DT[s[1]]=str(id)
            arabic_old[s[1]]={}
            write_file('dynamic/arabic_old.txt', str(arabic_old))
            for x in [c for c in GLOBACCESS.keys() if GLOBACCESS[c]==100]:
                msg(s[3], x, u'В конференции '+s[1]+u' зафиксировано использование арабского языка. \nЕсли желаете закрыть вход бота в эту конференцию отправьте ораб '+str(id))
    except: pass

register_message_handler(hnd_arabic_detect)

def hnd_orab(t, s, p):
    global LAST_AR_DT
    if not p in LAST_AR_DT.values(): return
    for x in LAST_AR_DT.keys():
        if LAST_AR_DT[x]==p:
            hnd_leave(t, s, x)
            f = 'dynamic/ban_room.list'
            db_file(f, dict)
            if check_file(file='ban_room.list'):
                db=eval(read_file(f))
                db[x]={}
                write_file(f, str(db))
                reply(t, s, u'ok')

register_command_handler(hnd_orab, 'ораб', ['все'], 100, 'При обнаружении использования орабского языга бот присвает определенной конференции уникальный ИД который можно использовать в даной команде для запрета входа бота в конференцию.', 'ораб <room id>', ['ораб 11'])	

            
def hnd_join(t, s, p):
    if not p:
        reply(t, s, u'Куда?')
        return
    try:
        global DEFAULT_NICK
        nick = DEFAULT_NICK
    except: nick = s[2]
    if p[:1]=='#' and not p.count('@con'):
        if not hasattr(IRC, 'join'):
            reply(t, s, u'IRC подключение неактивно!')
            return
        IRC.join(p.encode('utf-8'))
        file = 'dynamic/irc_channel.txt'
        db = eval(read_file(file))
        db[p]={}
        write_file(file, str(db))
        reply(t, s, u'Зашел на канал '+p)
        return
    if p.count(' '):
        ss = p.split()
        try:
            nick = re.findall('nick\s{0,2}=\s{0,2}(.*?)([ ,]|$)',p)[0][0]
            if not nick or len(nick)<2 or nick.isspace():
                nick = DEFAULT_NICK
        except: pass
        p = ss[0]
    if not p.count('.'):
        p = p+'@conference.jabber.ru'
    #unicodedata.category
    try:
        f = 'dynamic/ban_room.list'
        db_file(f, dict)
        if check_file(file='ban_room.list'):
            db=eval(read_file(f))
            if p.lower() in db.keys():
                reply(t, s, u'Вход бота в данную конференцию запрещен админом бота!')
                return
    except: pass
    packet = IQ(CLIENTS[s[3]], 'get')
    packet.addElement('query', 'jabber:iq:version')
    packet.addCallback(hnd_join_result, nick, t, s, p)
    reactor.callFromThread(packet.send, p)

def hnd_join_result(nick, type, source, parameters, x):
    global DEFAUL_STATUS
    file = 'dynamic/chatroom.list'
    level = int(user_level(source[1]+'/'+source[2], source[1]))
    if x['type'] == 'error':
        try: code = [c['code'] for c in x.children if (c.name=='error')]
        except: code = []
        if code:
            if code[0] in ['404']:
                reply(type, source, u'Дык нет такова чата! Смотри внимательней! (code 404)')
                return
            if code[0] in ['403']:
                reply(type, source, u'Я там или в бане, или сервер закрыт! (code 403)')
                return
    jid=get_true_jid(source[1]+'/'+source[2])
    parameters=parameters.lower()
    try: os.path.exists(parameters)
    except:
        reply(type, source, u'На сервере скорее всего не настроен юникод, русские символы недопустимы!')
        return
    db=eval(read_file(file))
    if not source[3] in db:
        db[source[3]]={}
    for x in db.keys():
        for c in db[x].keys():
            if x!= source[3] and c == parameters:
                if level<40 and x in CLIENTS.keys():
                    reply(type, source, u'Бот уже сидит в '+parameters+u' с другой учтеной записи! Для смены жида/вывода бота нужен доступ 40!')
                    return
                else:
                    reply(type, source, u'Ок, перезахожу с другой учтеной записи! ('+x+' / '+source[3]+')')
                    hnd_leave(type, source, parameters)
                    try:
                        for x in db.keys():
                            for c in db[x].keys():
                                if c==parameters:
                                    del db[x][c]
                                    if c in GROUPCHATS.keys():
                                        del GROUPCHATS[c]
                    except Exception as err:
                        try: print err.message,'admin.py hnd_join_result'
                        except: pass
                    #time.sleep(2)
    frm = source[1]+'/'+source[2]
    db[source[3]][parameters]={'from':frm, 'nick':nick, 'status':DEFAUL_STATUS, 'show':'chat'}
    write_file(file, str(db))
    callback=source[1]+'/'+source[2]
    if type in ['groupchat','public'] and source[1] in GROUPCHATS:
        callback=source[1]
    JOIN_CALLBACK[parameters]=callback
    join(parameters, nick, source[3])

def hnd_j2j(type, source, parameters):
    if not J2J:
        reply(type, source, u'j2j транспорт не указан в конфигураторе!')
        return
    parameters=parameters.replace('@','%')
    parameters=parameters+'@'+J2J
    hnd_join(type, source, parameters)

def hnd_leave(type, source, parameters):
    if parameters and parameters[:1]=='#' and not parameters.count('@con'):
        if not hasattr(IRC, 'left'):
            reply(type, source, u'IRC подключение неактивно!')
            return
        IRC.left(parameters.encode('utf-8'))
        file = 'dynamic/irc_channel.txt'
        db = eval(read_file(file))
        if parameters in db.keys():
            del db[parameters]
            write_file(file, str(db))
        reply(type, source, u'Ушел с '+parameters)
        return
    if not parameters and not source[1] in GROUPCHATS:
        return
    level = int(user_level(source[1]+'/'+source[2], source[1]))
    file = 'dynamic/chatroom.list'
    if not parameters:
        db=eval(read_file(file))
        if source[3] in db and source[1] in db[source[3]]:
            del db[source[3]][source[1]]
            write_file(file, str(db))
        if source[1] in GROUPCHATS:
            del GROUPCHATS[source[1]]
        leave(source[1],u'Меня уводит '+source[2], source[3])
        try: log_write(u'Меня уводит '+source[2], '', 'public', source[1])
        except: pass
    else:
        parameters = parameters.lower()
        if level<40:
            reply(type, source, u'Для вывода бота из другой конференции нужен доступ >= 40!')
            return
        if not parameters.count('@con'):
            parameters = parameters+'@conference.jabber.ru'
        db = eval(read_file(file))
        
        botjid = [x for x in db.keys() if hasattr(db[x], 'keys') and parameters in db[x].keys()]

        rep = ''

        if "JOIN_TIMER" in globals().keys() and parameters in JOIN_TIMER.keys():
                del JOIN_TIMER[parameters]
                rep+= u'Удалена из джойн таймера!\n'
        if parameters in GROUPCHATS.keys():
            del GROUPCHATS[parameters]
            rep+= u'Удалена из GROUPCHATS!\n'
        if botjid:
            botjid = botjid[0]
            if parameters in db[botjid].keys():
                del db[botjid][parameters]
                write_file(file, str(db))
                rep+= u'Удалена из \"dynamic/chatroom.list\"!\n'
        else:
            if not rep or rep.isspace():
                reply(type, source, u'Меня там нет!')
                return
            else:
                reply(type, source, rep)
                return
        leave(parameters, '', botjid)
        try: log_write(u'Меня уводит '+source[2], '', 'public', parameters)
        except: pass
        if source[1] in GROUPCHATS.keys():
            reply(type, source, u'Конференция <'+parameters+'> (bot JID '+botjid+')\n'+rep)
    

def hnd_botup(type, source, parameters):
    global bot_start
    icq, mem, cpu, st = 0, str(), str(), str()
    if hasattr(ICQ, 'sendMessage'):
        icq = 1
    
    rep = u'Старт бота '+bot_start+' ('+timeElapsed(time.time()-INFO['start'])+');\n'
    try:
        if 'RESTART_TIMER' in globals().keys() and RESTART_TIMER:
            rep+=u'Авторестарт каждых '+str(RESTART_TIMER/3600)+u'ч.\n'
    except: pass
    
    if "CLIENTS_UPTIME" in globals().keys():
        rep+=u'- Список подключений:\n'
        for x in CLIENTS_UPTIME.keys():
            try:
                st = BPING_STAT[x]['last']
            except:
                pass
            rep+='  JID: '+x+u' - '+(timeElapsed(time.time()-CLIENTS_UPTIME[x]) if hasattr(CLIENTS.get(x),'send') else u'(Отключен)')+' ping '+st+'\n'
        if icq:
            rep+='  UIN: '+UIN+'\n'
        try:
            if int(ENABLE_IRC):
                rep+='  IRC: '+IRC_NICK+'/'+IRC_SERV+'\n'
        except: pass
        try:
            if int(ENABLE_MRIM):
                rep+='  MailAgent: '+EMAIL+'\n'
        except: pass
    rep+=u'- Ошибок '+str(INFO['err'])+'\n'
    rep+=u'- Всего было запущено '+str(INFO['thr'])+u' потоков, активно '+str(len(threading.enumerate()))+'\n'

    def popen_read(cmd):
        pr = os.popen(cmd)
        data = pr.read()
        pr.close()
        return data
    
    if os.name=='posix':
        try:
            #pr = os.popen('ps -o rss -p %s' % os.getpid())
	    ls = popen_read('ps -o rss -p %s' % os.getpid()).splitlines()#pr.readlines()
	    if len(ls) >= 2:
			mem = ls[1].strip()
	    #pr.close()
	except: pass
	if mem: rep += u'- Использую %s мб. оперативной памяти\n' % (round(int(mem),1) / 1024)
	try:
            ls = popen_read('ps -p '+str(os.getpid())+' -o %cpu' ).splitlines()
	    if len(ls) >= 2:
			cpu = ls[1].strip()
	except: pass
	if cpu: rep += u'- Использую '+cpu+u' % процессора\n'

    rep+=u'- Получено сообщений '+str(INFO['imsg']+INFO['jmsg'])+':\n'
    rep+=u'   ICQ сообщения '+(str(INFO['imsg']) if hasattr(ICQ, 'sendMessage') else u'(Подключение не активно)')+'\n'
    rep+=u'   XMPP сообщения '+str(INFO['jmsg'])+'\n'
    rep+=u'- Траффик In '+str(INFO['tin']/1024)+u'кб. Out '+str(INFO['tout']/1024)+u'кб.\n'
    rep+=u'- Отправлено сообщений всего '+str(INFO['out'])+'\n'
    rep+=u'- Запросов на авторизацию '+str(INFO['auth'])+'\n'
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
    packet = IQ(CLIENTS[s[3]], 'set')
    query = packet.addElement('query', 'http://jabber.org/protocol/muc#admin')
    i = query.addElement('item')
    i[jn] = jid_nick
    i[ra] = set_to
    i.addElement('reason').addContent(reason)
    d = Deferred()
    packet.addCallback(d.callback)
    reactor.callFromThread(packet.send, s[1])
    return d

def ban(cljid, groupchat, jid):
    room_access(cljid, groupchat, 'affiliation', 'outcast', 'jid', jid)

def unban(cljid, groupchat, jid):
    room_access(cljid, groupchat, 'affiliation', 'none', 'jid', jid)

def room_access(cljid, groupchat, aff_role, par_one, jid_nick, par_two):
    q = domish.Element(('jabber:client', 'iq'))
    q['type'] = 'set'
    q['id'] = str(random.randrange(1,999))
    q['to'] = groupchat
    query = q.addElement('query', 'http://jabber.org/protocol/muc#admin')
    i = query.addElement('item')
    i[aff_role] = par_one
    i[jid_nick] = par_two
    reactor.callFromThread(dd, q, CLIENTS[cljid])

def hnd_unban(t, s, p):
    if not s[1] in GROUPCHATS or not p: return
    jid = p
    if p in GROUPCHATS[s[1]]:
        jid = GROUPCHATS[s[1]][p]['jid']
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
        jid = parameters
        if parameters in GROUPCHATS[source[1]]:
            jid = get_true_jid(source[1]+'/'+parameters)
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
        time.sleep(2)
        msg(source[3], source[1], '')
    time.sleep(2)
    reply('chat', source, u'Очищено!')

def hnd_globmsg(type, source, parameters):
    file = 'dynamic/chatroom.list'
    db = eval(read_file(file))
    if not GROUPCHATS or not parameters:
        return
    if not db:
        return
    for x in db.keys():
        for c in db[x].keys():
            if c in GROUPCHATS:
                msg(x, c, u'Новости от Admin:\n'+parameters)
    reply(type, source, u'Отправлено в '+str(len(GROUPCHATS))+u' конференций!')

def hnd_botnick(type, source, parameters):
    if not source[1] in GROUPCHATS or not parameters:
        return
    if len(parameters)>21:
        reply(type, source, u'Напиши ник по короче!')
        return
    file = 'dynamic/chatroom.list'
    db=eval(read_file(file))
    if not source[3] in db.keys(): return
    if source[1] in db[source[3]].keys():
        db[source[3]][source[1]]['nick']=parameters
        write_file(file, str(db))
    try: BOT_NICK[source[1]]=parameters
    except: pass
    join(source[1],parameters,source[3])
    time.sleep(2)
    change_nick_check(source[1], parameters, source[3])

def hnd_botstatus(type, source, parameters):
    file='dynamic/chatroom.list'
    if not source[1] in GROUPCHATS:
        return
    if not parameters or len(parameters)>250:
        return
    show='chat'
    status=parameters
    if parameters.count(' ') and parameters.split()[0] in [u'chat',u'dnd',u'away',u'xa']:
        show=parameters.split()[0]
        status=' '.join(parameters.split()[1:])
    db=eval(read_file(file))
    if not source[3] in db.keys():
        db[source[3]] = {}
    if source[1] in db[source[3]].keys():
        db[source[3]][source[1]]['show']=show
        db[source[3]][source[1]]['status']=status
        write_file(file, str(db))
    join(source[1], get_bot_nick(source[1]), source[3])

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

REMOTE_REPORT = {}

def hnd_remote_report(jid, body, any):
    global REMOTE_REPORT
    if jid in REMOTE_REPORT.keys():
        reply(REMOTE_REPORT[jid][0],REMOTE_REPORT[jid][1],body)
    #print jid, body

register_outgoing_message_handler(hnd_remote_report)

def hnd_remote_cmd(t, s, p):
    global REMOTE_REPORT
    par=''
    if not p.count(' ')>1:
        reply(t, s, u'Синтаксис: чат команда параметры')
        return
    ss=p.split()
    id = str(random.randrange(1000, 9999))
    #0-chat,1-command,2-par
    chat=ss[0].lower()
    if not chat in GROUPCHATS:
        list = [x for x in GROUPCHATS.keys() if x.count(chat)]
        if list:
            if len(list)>1:
                reply(t, s, u'Укажите чат более детально!(>1 совпадений)')
                return
            chat = list[0]
        else:
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
    

    try:
        bjid = GROUPCHATS[chat][get_bot_nick(chat)]['jid'].split('/')[0]
    except:
        reply(t, s, u'Ups! Error')
        return
    
    ba = u'botadmin'+id
    ajid = ba+'@uknown'+id+'.tld'
    REMOTE_REPORT[ajid] = (t, s)
    GLOBACCESS[ajid] = 100
    GROUPCHATS[chat][ba]={'stmsg':'','status':'','ishere':1,'jid':ajid,'joined':time.time(),'idle':time.time()}
    call_command_handlers(cmd, 'private', [chat+'/'+ba, chat, ba, bjid], par)
    time.sleep(0.5)
    del GROUPCHATS[chat][ba]
    del GLOBACCESS[ajid]
    time.sleep(1)
    reply(t, s, u'Выполнено!')

def hnd_say(t, s, p):
    if not p or not s[1] in GROUPCHATS: return
    msg(s[3], s[1], p)

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

def handler_searsh_conf(tt, s, p):
        if not p or p.isspace():
                reply(tt, s, u'Кого искать?')
                return
        aa, jid, confs, t = '', p, '', 0
	
	for i in range(0, len(GROUPCHATS.keys())):
		for j in range(0, len(GROUPCHATS[GROUPCHATS.keys()[i]].keys())):
			truejid = get_true_jid(GROUPCHATS.keys()[i]+'/'+GROUPCHATS[GROUPCHATS.keys()[i]].keys()[j])
			truejid = truejid.lower()
			nick = GROUPCHATS[GROUPCHATS.keys()[i]].keys()[j]
			jid = jid.lower()
			nick = nick.lower()
			try:
                                if (truejid.count(jid)>0) | (nick.count(jid)>0):
                                        if GROUPCHATS[GROUPCHATS.keys()[i]][GROUPCHATS[GROUPCHATS.keys()[i]].keys()[j]]['ishere']==1:
                                                t += 1
                                                if t<12 and len(confs)<600:
                                                        confs += str(t)+'. '+ GROUPCHATS.keys()[i] + ' ('+GROUPCHATS[GROUPCHATS.keys()[i]].keys()[j]+') '+truejid+'\n'
                        except:
                                pass
	if confs == '':
		aa = u'Ничего не найдено!'
	else:
		aa = u'Найдено :\n № [chat][nick][jid]\n'+ confs
	reply(tt, s, aa[:900])
	
register_command_handler(handler_searsh_conf, '!хде', ['все'], 20, 'поиск по всем комнатам где сидит бот,ищет по совпадению в jid-e или нике', 'хде <ник>', ['хде вася'])	
register_command_handler(hnd_unban, 'унбан', ['админ','мук','все'], 20, 'Достает из бани ник/жид', 'унбан <jid>', ['унбан d@jab.ua'])
register_command_handler(hnd_unban, 'никто', ['админ','мук','все'], 20, 'Устанавливает на jid affiliation <none>', 'никто <jid>', ['никто d@jab.ua'])
register_command_handler(handler_getrealjid, 'тружид', ['инфо','админ','мук','все'], 20, 'Показывает реальный жид указанного ника. Работает только если бот модер ессно', 'тружид <ник>', ['тружид guy'])
register_command_handler(hnd_proper, 'proper', ['все'], 40, 'Удаляет конференции в которые не смог войти бот.', 'proper', ['proper'])        
register_command_handler(hnd_wtf, 'wtf', ['все'], 10, 'Выводит последнюю ошибку бота.', 'wtf', ['wtf'])        
register_command_handler(hnd_say, 'сказать', ['все'], 20, 'Сказать что-то от имени бота.', 'сказать <текст>', ['сказать пук'])        
register_command_handler(hnd_remote_cmd, 'ремоут', ['все'], 100, 'Дистанционное выполнение команды в любой из конференций где находится бот.', 'ремоут <чат> <команда> <параметры>', ['ремоут cool@conference.talkonaut.com сказать посоны привет','ремоут cool избани gogi.net'])        
register_command_handler(hnd_find_plugin, '!плагин', ['все'], 20, 'Информация об определенной команде, о плагине в котором содержиться ее код.', '!плагин <команда>', ['!плагин пинг'])        
register_command_handler(hnd_botstatus, 'ботстатус', ['все'], 20, 'Устанавливает статус бота в конференции.', 'ботстатус <презенс статус> <текст>', ['ботстатус away скоро вернусь'])        
register_command_handler(hnd_botnick, 'ботник', ['все'], 20, 'Меняет ник бота в конференции.', 'ботник <ник>', ['ботник вася'])    
register_command_handler(hnd_globmsg, 'globmsg', ['админ','все'], 100, 'Сообщение во все комнаты где бот.', 'globmsg <body>', ['globmsg test'])    
register_command_handler(hnd_restart, 'рестарт', ['админ','все'], 100, 'Без параметров рестарт бота полностью, с указанием JID или его части - рестарт отдельного подключения.', 'рестарт', ['рестарт','рестарт gogi@jabber.ru','рестарт icq'])    
register_command_handler(hnd_wherei, 'хдея', ['админ','все'], 0, 'Показывает комнаты в которых сидит бот', 'хдея', ['хдея'])    
register_command_handler(hnd_off, 'пшёл', ['админ','все'], 100, 'Выключение бота', 'пшёл', ['пшёл'])    
register_command_handler(hnd_owner, 'овнер', ['админ','все'], 30, 'Дает овнера определенному нику или JID-у', 'овнер <nick>', ['овнер Guy'])
register_command_handler(hnd_botup, 'ботап', ['админ','все'], 0, 'Статистика работы бота', 'ботап', ['ботап'])
register_command_handler(hnd_ban, 'бан', ['админ','все'], 20, 'Бан юзера/сервера', 'бан <nick>', ['бан Guy'])
register_command_handler(hnd_participant, 'войс', ['админ','все'], 15, 'Даёт посетителю право голоса', 'войс <nick>', ['войс Guy'])		
register_command_handler(hnd_kick, 'кик', ['админ','все'], 15, 'Выгнать посетителя из комнаты', 'кик <nick>', ['кик Guy'])
register_command_handler(hnd_visitor, 'девойс', ['админ','все'], 15, 'Лишает посетителя голоса', 'девоис <nick>', ['девоис Guy'])
register_command_handler(hnd_member, 'мембер', ['админ','все'], 20, 'Делает юзера постоянным участником по jid-y или нику', 'мембер <nick>', ['мембер Guy'])			
register_command_handler(hnd_join, 'зайти', ['админ','все'], 40, 'Заводит бота в Jabber-конференцию, дополнительный ключ nick=ник заводит бота с указанным ником', 'зайти чат', ['зайти cool@conference.talkonaut.com nick=Gogi'])			
register_command_handler(hnd_j2j, 'j2j', ['админ','все'], 40, 'Зайти в конфу через транспорт j2j', 'j2j чат', ['j2j cool@conference.talkonaut.com'])			
register_command_handler(hnd_leave, 'свал', ['админ','все'], 20, 'Выйти с конференции', 'свал чат', ['свал cool@conference.talkonaut.com','свал'])			
register_command_handler(hnd_clear, 'чисть', ['админ','все'], 0, 'Чистит конфу', 'чисть', ['чисть'])			
register_command_handler(hnd_login, 'логин', ['доступ','админ','все'], 0, 'Авторизоваться как админиcтратор бота. Использовать только в привате!', 'логин <пароль>', ['логин мой_пароль'])
register_command_handler(hnd_logout, 'логаут', ['доступ','админ','все'], 0, 'Снять авторизацию.', 'логаут', ['логаут'])

