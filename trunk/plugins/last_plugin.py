# -*- coding: utf-8 -*-

def idle_handler(typ, ss, pp):
    if not pp:
        pp=ss[3].split('@')[1]
    jids = pp
    packet = IQ(CLIENTS[ss[3]], 'get')
    packet.addElement('query', 'jabber:iq:last')
    packet.addCallback(idle_result_handler, typ, ss, pp)
    reactor.callFromThread(packet.send, jids)

def idle_result_handler(typ, ss, pp, x):
    if x['type']=='result':
        t=x.children[0].getAttribute('seconds')
        if not t:
            reply(t, ss, u'Не получилось!')
            return
        reply(typ, ss, pp+u' работает уже '+timeElapsed(int(t)))
    else:
        reply(typ, ss, u'Адрес ответил ошибкой!')


def last_handler(t, s, p):
    if not p:
        reply(t, s, u'Живее всех живых!\nНик писать будешь?')
        return
    to = p
    i = 0
    if s[1] in GROUPCHATS.keys() and p in GROUPCHATS[s[1]]:
        to = s[1]+'/'+p
        i = 1
    iq = IQ(CLIENTS[s[3]], 'get')
    iq['to'] = to
    iq.addElement('query', 'jabber:iq:last')
    iq.addCallback(last_result_handler, t, s, p, i)
    reactor.callFromThread(iq.send, to)

def last_result_handler(t, s, p, i, x):
    tim=0
    rep=''
    if x['type']=='result':
        try: tim=x.children[0]['seconds']
        except:
            for c in x.elements():
                tim=c.getAttribute('seconds')
                if tim:
                    break
        rep+=u'Ответ клиента '+p+u' <iq:last> - '+timeElapsed(int(tim))+u' назад\n'
    else:
        rep+=u'Нет ответа на iq:last\n'
    if i:
        try: rep+=u'Посл. активность в чате - '+timeElapsed(time.time()-GROUPCHATS[s[1]][p]['idle'])+u'. назад'
        except: pass
    reply(t, s, rep)

LAST_IQ_ALL = {}

def hnd_last_all(t, s, p):
    if not s[1] in GROUPCHATS: return
    jid=None
    global LAST_IQ_ALL
    list=[x for x in GROUPCHATS[s[1]].keys() if GROUPCHATS[s[1]][x]['ishere']]
    if not list or len(list)<3:
        reply(t, s, u'Только мы с тобой тут!')
        return
    for m in list:
        if m==get_bot_nick(s[1]):
            continue
        jid=s[1]+'/'+m
        packet = IQ(CLIENTS[s[3]], 'get')
        packet.addElement('query', 'jabber:iq:last')
        packet.addCallback(lastall_result_handler, t, s, m)
        reactor.callFromThread(packet.send, jid)
    sl=(len(list)/2)+2
    if sl>6:
        sl=6
    time.sleep(sl)
    if not s[1] in LAST_IQ_ALL:
        reply(t, s, u'Косяк какойто')
        return
    if LAST_IQ_ALL[s[1]]['none']:
        for x in LAST_IQ_ALL[s[1]]['none']:
            if 'idle' in GROUPCHATS[s[1]][x] and time.time()-GROUPCHATS[s[1]][x]['idle']<200:
                if not x in LAST_IQ_ALL[s[1]]['live']:
                    LAST_IQ_ALL[s[1]]['live'].append(x)
            else:
                if not x in LAST_IQ_ALL[s[1]]['died']:
                    LAST_IQ_ALL[s[1]]['died'].append(x)
    try:
        liv=',  '.join(LAST_IQ_ALL[s[1]]['live'])
        die=', '.join(LAST_IQ_ALL[s[1]]['died'])
        if not die:
            die=u''
        if not liv:
            reply(t, s, u'Таак, как на марсе - глухо.')
            return
        reply(t, s, u'Итак, кто выжил:\n'+liv)
    except: pass
    del LAST_IQ_ALL[s[1]]
    

def lastall_result_handler(t, s, m, x):
    global LAST_IQ_ALL
    if not s[1] in LAST_IQ_ALL:
        LAST_IQ_ALL[s[1]]={'live':[],'died':[],'none':[]}
    if x['type']=='result':
        try: tim=x.children[0]['seconds']
        except:
            for c in x.elements():
                tim=c.getAttribute('seconds')
                if tim:
                    break
        if int(tim)<200:
            if not m in LAST_IQ_ALL[s[1]]['live']:
                LAST_IQ_ALL[s[1]]['live'].append(m)
        else:
            if not m in LAST_IQ_ALL[s[1]]['died']:
                LAST_IQ_ALL[s[1]]['died'].append(m)
    else:
        LAST_IQ_ALL[s[1]]['none'].append(m)



register_command_handler(idle_handler, 'аптайм', ['все'], 0, 'Показывает время работы сервера.', 'аптайм <server>', ['аптайм talkonaut.com'])
register_command_handler(last_handler, 'жив', ['все'], 0, 'Показывает время последней активности юзера.', 'жив <nick|jid>', ['жив вася'])
register_command_handler(hnd_last_all, 'живые', ['все'], 0, 'Показывает кто активен в чате, активными признаются юзеры с временем простоя клиента не более 200 секунд.', 'живые', ['живые'])

