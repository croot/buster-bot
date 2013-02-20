# -*- coding: utf-8 -*-

DR_JABBER = {'captcha':{'jabber.ru':None,'qip.ru':None,'xmpp.ru':None},'open':{},'close':{}}
DR_JABBER_FILE = 'dynamic/drjabber.txt'

db_file(DR_JABBER_FILE, dict)

WHITE_SERV = ['jabber.ru','xmpp.ru','qip.ru']

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
    serv = re.findall('<td style=\"text-align: left;\">(.*)\n',res)
    return [x for x in serv if x not in WHITE_SERV]


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

def hnd_drjabber(t, s, p):
    global DR_JABBER_FILE
    global DR_JABBER
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
    list, w = drjabber_grab(), 0
    list.extend(drjab_grab2())
    if not list:
        reply(t, s, u'Граббер сломался или сайт лежит!')
    reply(t, s, u'В списке найдено '+str(len(list))+u' серверов.')
    if p.lower()==u'update' or time.time()-os.path.getmtime(DR_JABBER_FILE)>86400*3 or not eval(read_file(DR_JABBER_FILE)):
        w = 1
        reply(t, s, u'Проверка займет '+str(len(list)/4)+u' секунд, скорость 4 серв./с.')
        for x in list:
            register_try(s[3], x)
            time.sleep(0.25)
    else:
        DR_JABBER = eval(read_file(DR_JABBER_FILE))
    rep = u'Проверка завершена. Отчет:\nServers on CAPTCHA: '+str(len(DR_JABBER['captcha']))+u', new '+str(len(DR_JABBER['captcha'])-lenc)+'\n'
    rep +=u'Open registation (outcast server): '+str(len(DR_JABBER['open']))+u', new '+str(len(DR_JABBER['open'])-leno)+'\n'
    rep +=u'Servers send error: '+str(len(DR_JABBER['close']))+u', new '+str(len(DR_JABBER['close'])-lene)
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
