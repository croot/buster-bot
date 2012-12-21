# -*- coding: utf-8 -*-

DR_JABBER = {'captcha':{},'open':{},'close':{}}
DR_JABBER_FILE = 'dynamic/drjabber.txt'

db_file(DR_JABBER_FILE, dict)


def drjabber_grab():
    req = urllib2.Request('http://jabberworld.info/'+u'Список_работающих_публичных_серверов_Jabber'.encode('utf8'))
    req.add_header = ('User-agent', 'Mozilla/5.0')
    res = urllib2.urlopen(req).read()
    serv = re.findall('<td style=\"text-align: left;\">(.*)\n',res)
    return serv


def register_try(cl, srv):
    iq = IQ(CLIENTS[cl], 'get')
    iq['type'] = 'get'
    iq['id'] = str(random.randrange(1, 999))
    iq['to'] = srv
    query = iq.addElement('query', 'jabber:iq:register')
    iq.addCallback(fld_chc_srv, srv)
    reactor.callFromThread(iq.send, srv)

def fld_chc_srv(srv, x):
    global DR_JABBER
    if x['type']=='result':
        try: ns = x.__dict__['children'][0].children[1].uri
        except: return
        if ns == 'jabber:x:data':
            DR_JABBER['captcha'][srv] = None
        elif ns == 'jabber:iq:register':
            DR_JABBER['open'][srv] = None
    else: DR_JABBER['close'][srv] = None

def hnd_drjabber(t, s, p):
    global DR_JABBER_FILE
    global DR_JABBER
    if p.lower() in DR_JABBER.keys():
        try: reply(t, s, ', '.join(eval(read_file(DR_JABBER_FILE))[p.lower()].keys()))
        except: pass
        return
    if not s[1] in GROUPCHATS:
        return
    list, w = drjabber_grab(), 0
    if not list:
        reply(t, s, u'Граббер сломался или сайт лежит!')
    reply(t, s, u'В списке найдено '+str(len(list))+u' серверов.')
    if time.time()-os.path.getmtime(DR_JABBER_FILE)>86400*3 or not eval(read_file(DR_JABBER_FILE)):
        w = 1
        reply(t, s, u'Проверка займет '+str(len(list)/4)+u' секунд, скорость 4 серв./с.')
        for x in list:
            register_try(s[3], x)
            time.sleep(0.25)
    reply(t, s, u'Серверов защищенных captcha form: '+str(len(DR_JABBER['captcha']))+u', серверов с открытой регистрацией которым будет закрыт вход в конференцию (outcast): '+str(len(DR_JABBER['open']))+u', серверов ответивших ошибкой либо с ограниченной владельцеми регистрацией: '+str(len(DR_JABBER['close'])))
    UNBAN = DR_JABBER['captcha']
    UNBAN.update(DR_JABBER['close'])
    for x in UNBAN.keys():
        room_access(s[3], s[1], 'affiliation', 'none', 'jid', x)
    for x in DR_JABBER['open'].keys():
        room_access(s[3], s[1], 'affiliation', 'outcast', 'jid', x)
    if w: write_file(DR_JABBER_FILE, str(DR_JABBER))
    for x in DR_JABBER.keys():
        DR_JABBER[x].clear()


register_command_handler(hnd_drjabber, 'dr.jabber', ['админ','все'], 20, 'Команда оптимизирует защиту вашей конференции от спам ботом, баня серверы с открытой регистрацией и в то же время удаляя из бана безопасные серверы!Список обновляеться из сайта http://jabberworld.info', 'dr.jabber', ['dr.jabber','dr.jabber open','dr.jabber captcha'])
