#===istalismanplugin===
# -*- coding: utf-8 -*-

FIND_JID = {}
FIND_TOP = {}
T_LAST_456 = 0

def hnd_find_jid_inban(t, s, p):
    if not p:
        reply(t, s, '\n'.join(COMMANDS['inban']['examples']))
        return
    if not s[1] in GROUPCHATS:
        return
    def hnd_find_jid_inban_res(p, t, s, x):
        if x['type']=='result':
            rep=''
            query = element2dict(x)['query']
            query = [i.attributes for i in query.children if i.__class__==domish.Element]
            if not query:
                print 'N1'
                return
            for c in query:
                if c['jid'].count(p):
                    rep+=str(query.index(c)+1)+u'n) '+c['jid']+'\n'
            if not rep or rep.isspace():
                reply(t,s,u'False')
                return
            reply(t, s, rep)
        else:
            reply(t,s,u'Список недоступен!')
    try: packet = IQ(CLIENTS[s[3]], 'get')
    except: print 'ERR'
    packet['id'] = 'item'+str(random.randrange(1000, 9999))
    query = packet.addElement('query', 'http://jabber.org/protocol/muc#admin')
    i = query.addElement('item')
    i['affiliation'] = 'outcast'
    packet.addCallback(hnd_find_jid_inban_res, p, t, s)
    reactor.callFromThread(packet.send, s[1])

def hnd_find_jid(t, s, p):
    top = (False if p.lower()!=u'топ' else True)
    if not p:
        reply(t, s, '\n'.join(COMMANDS[u'найти жид']['examples']))
        return
    reply(t, s, u'Поиск начат')
    global FIND_JID
    global FIND_TOP
    global T_LAST_456
    jid = get_true_jid(s)
    if not top:
        FIND_JID[jid] = {'d':{},'res':{},'err':{}}
    else:
        FIND_TOP[jid] = {}
    if not GROUPCHATS:
        reply(t, s, u'Функция работает только когда бот сидит минимум в одной Jabber-конференции!')
        return
    n = len(GROUPCHATS)
    cc = 0
    for x in GROUPCHATS:
        cc+=1
        for c in ['owner','admin','member',('outcast' if not top else '')]:
            try: packet = IQ(CLIENTS[GROUPCHATS[x][get_bot_nick(x)]['jid'].split('/')[0]], 'get')
            except: continue
            packet['id'] = 'item'+str(random.randrange(1000, 9999))
            query = packet.addElement('query', 'http://jabber.org/protocol/muc#admin')
            i = query.addElement('item')
            i['affiliation'] = c
            packet.addCallback(hnd_answ_find_jid, (False if cc!=n else True), p, t, s, jid, x)
            reactor.callFromThread(packet.send, x)
    #time.sleep(7)
    

def hnd_answ_find_jid(n, p, t, s, jid, chat, x):
    T_LAST_456 = time.time()
    top = (False if p.lower()!=u'топ' else True)
    id = str()
    sv = None
    z = None
    rep = ''
    if x['type']=='result':
        if not top and not chat in FIND_JID[jid]['res']:
            FIND_JID[jid]['res'][chat]={}
        query = element2dict(x)['query']
        query = [i.attributes for i in query.children if i.__class__==domish.Element]
        if not query: return
        for c in query:
            if top and jid in FIND_TOP.keys():
                id = c['jid']
                if id.count('@'):
                    sv = id.split('@')[1]
                    if not sv in FIND_TOP[jid].keys():
                        FIND_TOP[jid][sv]=1
                    else:
                        FIND_TOP[jid][sv]+=1
            else:
                if c['jid'].count(p):
                    FIND_JID[jid]['d'][c['jid']+' '+chat]=c['affiliation']
                
    else:
        try: FIND_JID[jid]['err'][chat]={}
        except: pass
    if n:
        time.sleep(7)
        while time.time() - T_LAST_456<5:
            time.sleep(1)
            pass
        if top and jid in FIND_TOP.keys():
            z=sorted(FIND_TOP[jid].items(), key=lambda x: x[1])
            z.reverse()
            if len(z)>10:
                z=z[:10]
            reply(t, s, u'Сервер | Пользователей:\n'+'\n'.join([x[0]+' - '+str(x[1]) for x in z]).replace('talkonaut','tal*konaut'))
            del FIND_TOP[jid]
        else:
            inf = u'-   Просканировал списки '+str(len(FIND_JID[jid]['res']))+u'\n из '+str(len(GROUPCHATS))+u' конференций.\n'
            if not FIND_JID[jid]['d']:
                reply(t, s, inf+u'Совпадений нет!')
                return
            reply(t, s, inf+'\n'.join([x+' '+FIND_JID[jid]['d'][x] for x in FIND_JID[jid]['d'].keys()]))
            del FIND_JID[jid]

register_command_handler(hnd_find_jid, '!найти_жид', ['все','админ'], 20, 'Поиск жида в овнер-,админ-,мембер-,бан- листах конференций.', '!найти_жид <jid>', ['!найти_жид buster@cc.ru'])
register_command_handler(hnd_find_jid, 'найти жид', ['все','админ'], 20, 'Поиск жида в овнер-,админ-,мембер-,бан- листах конференций. Ключ топ выведет топ 10 используемых серверов', 'найти жид <JID>', ['найти жид buster@cc.ru','найти жид топ'])
register_command_handler(hnd_find_jid_inban, 'inban', ['все','админ'], 20, 'Проверка на наличие жида в бан листе конференции.', 'inban <JID>', ['inban buster@cc.ru'])
