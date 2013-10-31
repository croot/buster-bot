# -*- coding: utf-8 -*-

DR_JABBER = {'captcha':{'jabber.ru':None,'qip.ru':None,'xmpp.ru':None},'open':{},'close':{}}
DR_JABBER_FILE = 'dynamic/drjabber.txt'

db_file(DR_JABBER_FILE, dict)

WHITE_SERV = ['jabber.ru','xmpp.ru','qip.ru']


def drjab_getmuc_servlist():
    d = 'dynamic/'
    f = 'backup_roomf.txt'
    l = [x for x in os.listdir(d) if os.path.isdir(os.path.join(d,x)) and (x.count('@con') or x.count('@muc') or x.count('@chat'))]
    l = [x for x in l if os.path.exists(os.path.join(d,x,f))]
    dict = {}
    for x in l:
        try:
            db = eval(read_file(os.path.join(d,x,f)))
            db = db[x]
            for c in ['admin','member','owner','outcast']:
                for b in db[c]:
                    try: serv = b.split('@')[1]
                    except: serv = b
                    if not serv in dict.keys():
                        dict[serv]={}
        except:
            continue
    return dict.keys()

def grab_servlist_uptime():
    req = urllib2.Request('http://jabberworld.info/'+u'Список_работающих_публичных_серверов_Jabber'.encode('utf8'))
    req.add_header = ('User-agent', 'Mozilla/5.0')
    res = urllib2.urlopen(req).read()
    serv = re.findall('<td align="left">(.*?\d{1,2} месяца \d{1,2} дней \d{1,2}:\d{1,2}:\d{1,2})s', res, re.DOTALL|re.IGNORECASE)
    serv = [re.compile(r'<[^<>]*>').sub('', x) for x in serv]
    return serv


def drjab_grab2():
    global WHITE_SERV
    req = urllib2.Request('http://jabberworld.info/RAW:'+u'_Список_Jabber-серверов'.encode('utf8'))
    req.add_header = ('User-agent', 'Mozilla/5.0')
    res = urllib2.urlopen(req).read()
    serv = re.findall('<p>(.*)\n',res)
    return [x for x in serv if x not in WHITE_SERV]

def drjabber_grab():
    global WHITE_SERV
    req = urllib2.Request('http://jabberworld.info/'+u'Список_работающих_публичных_серверов_Jabber'.encode('utf8'))
    req.add_header = ('User-agent', 'Mozilla/5.0')
    res = urllib2.urlopen(req).read()
    serv = re.findall('<td align="left">(.*)\n',res)
    return [x for x in serv if x not in WHITE_SERV]

TOPUPSERV_FILE = 'dynamic/topupserv.txt'
db_file(TOPUPSERV_FILE, dict)

def hnd_uptime_top(t, s, p):
    global TOPUPSERV_FILE
    d={}
    db = eval(read_file(TOPUPSERV_FILE))
    list = []
    def stod(s):
        if isinstance(s, basestring):
            s=float(s)
        d= s/86400
        return str(d)
    def supsnd(cljid,serv):
        packet = IQ(CLIENTS[cljid], 'get')
        packet.addElement('query', 'jabber:iq:last')
        packet.addCallback(supsnd_result_handler, serv)
        reactor.callFromThread(packet.send, serv)
    def supsnd_result_handler(serv, x):
        if x['type']=='result':
            tt=x.children[0].getAttribute('seconds')
            d[serv]=int(tt)
            try: print serv,tt
            except: pass
    n=0
    if time.time()-os.path.getmtime(TOPUPSERV_FILE)>86400*3:
        list = drjabber_grab()
        list.extend(drjab_grab2())
        list.extend([x for x in drjab_getmuc_servlist() if not x in list])
        reply(t, s, u'Выбор лучшего сервера на основе аптайма.\nПроверка займет ~'+timeElapsed(len(list)/4)+u', скорость 4 серв./с.')
        
    
        for x in list:
            supsnd(s[3], x)
            n+=1
            if n>=50:
                time.sleep(3)
                n=0
            time.sleep(0.25)
        time.sleep(5)
        write_file(TOPUPSERV_FILE, str(d))
        
    else:
        d = db.copy()
    d=sorted(d.items(), key=itemgetter(1))
    d.reverse()
    rep=str()
    last,st,n=str(),str(),0
    for x in d:
        st=stod(x[1])
        if last==st and p.lower()!='-f':
            continue
        last=st
        n+=1
        rep+=str(n)+')'+x[0]+' - '+stod(x[1])+'\n'
        if n>=30:
            break
    reply(t, s, u'№ - Name - Uptime days\n'+rep)
    


register_command_handler(hnd_uptime_top, 'выбрать сервер', ['админ','все'], 0, 'Топ-30 jabber-серверов на основе времени работы. По умолчанию работает фильтр серверов с одинаковым аптаймом(серверы яндекса и т.д.) ключ -f выведет результат без фильтров.', 'выбрать сервер', ['выбрать сервер'])


def register_try(cl, srv):
    iq = IQ(CLIENTS[cl], 'get')
    iq['type'] = 'get'
    iq['id'] = str(random.randrange(1, 999))
    iq['to'] = srv
    query = iq.addElement('query', 'jabber:iq:register')
    iq.addCallback(fld_chc_srv, srv)
    reactor.callFromThread(iq.send, srv)

def register_try1(cl, srv):
    iq = IQ(CLIENTS[cl], 'get')
    iq['type'] = 'get'
    iq['id'] = str(random.randrange(1, 999))
    iq['to'] = srv
    query = iq.addElement('query', 'jabber:iq:register')
    iq.addCallback(ts, srv)
    reactor.callFromThread(iq.send, srv)

def fld_chc_srv(srv, x):
    global DR_JABBER
    if x['type']=='result':
        try: ns = x.__dict__['children'][0].children[1].uri
        except: return
        if ns == 'jabber:x:data':
            DR_JABBER['captcha'][srv] = None
        if ns == 'jabber:iq:register':
            DR_JABBER['open'][srv] = None
    else: DR_JABBER['close'][srv] = None

DRJAB_TIMER = 0
DRJAB_CHAT = {}

def hnd_drjabber(t, s, p):
    global DR_JABBER_FILE
    global DR_JABBER
    global DRJAB_TIMER
    global DRJAB_CHAT
    txt = eval(read_file(DR_JABBER_FILE))
    if p.lower() in DR_JABBER.keys():
        try: reply(t, s, ', '.join(txt[p.lower()].keys()))
        except: pass
        return
    lenc, lene, leno = 0, 0, 0
    try:
        lenc=len(txt['captcha'])
        lene=len(txt['close'])
        leno=len(txt['open'])
    except: pass
    if len(p.split())>1 and p.split()[0].lower() == u'serv':
        c = p.split()[1].lower()
        if txt:
            if c in txt['captcha']:
                reply(t, s, u'Сервер '+c+u' на капче!')
                return
            
            if c in txt['open']:
                reply(t, s, u'Сервер '+c+u' с открытой регой!')
                return
            
            if c in txt['close']:
                reply(t, s, u'Сервер '+c+u' закрытый!')
                return
            reply(t, s, u'Статус сервера неизвестен!')
            return
    if not s[1] in GROUPCHATS:
        return
    if s[1] in DRJAB_CHAT.keys() and time.time()-DRJAB_CHAT[s[1]]<600:
        reply(t, s, u'Команду можно использовать не чаще раза в 10 минут!')
        return
    DRJAB_CHAT[s[1]]=time.time()
    list, w = drjabber_grab(), 0
    list.extend(drjab_grab2())
    zz=0
    ad=drjab_getmuc_servlist()
    for x in ad:
        if not x in list:
            zz+=1
            list.append(x)
    if not list:
        reply(t, s, u'Граббер сломался или сайт лежит!')
    reply(t, s, u'В списке найдено '+str(len(list))+u' серверов.\nСерверов с чатов '+str(zz))
    if p.lower()==u'update' or time.time()-os.path.getmtime(DR_JABBER_FILE)>86400*3 or not eval(read_file(DR_JABBER_FILE)):
        if DRJAB_TIMER!=0 and DRJAB_TIMER>time.time():
            reply(t, s, u'Сейчас идет обновление базы, примерное время до завершения '+timeElapsed(DRJAB_TIMER-time.time()))
            return
        w = 1
        reply(t, s, u'Проверка займет '+timeElapsed(len(list)/4)+u', скорость 4 серв./с.')
        DRJAB_TIMER = time.time()+len(list)/4
        for x in list:
            register_try(s[3], x)
            time.sleep(0.25)
    else:
        DR_JABBER = eval(read_file(DR_JABBER_FILE))
    rep = u'Проверка завершена. Отчет:\nServers on CAPTCHA: '+str(len(DR_JABBER['captcha']))+u', new '+str(len([x for x in DR_JABBER['captcha'].keys() if not x in txt.get('captcha',[])]))+'\n'
    rep +=u'Open registation (outcast server): '+str(len(DR_JABBER['open']))+u', new '+str(len([x for x in DR_JABBER['open'].keys() if not x in txt.get('open',[])]))+'\n'
    rep +=u'Servers send error: '+str(len(DR_JABBER['close']))+u', new '+str(len([x for x in DR_JABBER['close'].keys() if not x in txt.get('close',[])]))
    reply(t, s, rep)
    UNBAN = DR_JABBER['captcha']
    UNBAN.update(DR_JABBER['close'])
    drj_afl(s, 'none', UNBAN.keys())
    time.sleep(3)
    drj_afl(s, 'outcast', DR_JABBER['open'].keys())
    if w: write_file(DR_JABBER_FILE, str(DR_JABBER))
    for x in DR_JABBER.keys():
        DR_JABBER[x].clear()

def drj_afl(s, afl, jid):
    packet = IQ(CLIENTS[s[3]], 'set')
    query = packet.addElement('query', 'http://jabber.org/protocol/muc#admin')
    if len(jid)>51:
        a, b = 0, 50
        for x in range(len(jid)/50+1):
            print len(jid[a:b:])
            drj_afl(s, afl, jid[a:b:])
            a+= 50
            b+= 50
            time.sleep(3.5)
        return
    for x in jid:
        i = query.addElement('item')
        i['jid'] = x
        i['affiliation'] = afl
        if afl!='none':
            i.addElement('reason').addContent(u'dr.jabber: open registration')
        if sys.getsizeof(packet)>62000:
            break
    d = Deferred()
    packet.addCallback(d.callback)
    reactor.callFromThread(packet.send, s[1])
    return d


register_command_handler(hnd_drjabber, 'dr.jabber', ['админ','все'], 20, 'Команда оптимизирует защиту вашей конференции от спам ботом, баня серверы с открытой регистрацией и в то же время удаляя из бана безопасные серверы!Список обновляеться из сайта http://jabberworld.info с помощью ключа update либо раз в три дня автоматически.', 'dr.jabber', ['dr.jabber','dr.jabber open','dr.jabber captcha','dr.jabber update','dr.jabber serv jabber.ru'])
