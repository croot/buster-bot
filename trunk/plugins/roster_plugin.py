# -*- coding: utf-8 -*-

ROSTER = {}

def get_roster_auto(cljid):
    time.sleep(6)
    get_roster(cljid)

def get_roster(cljid):
    packet = IQ(CLIENTS[cljid], 'get')
    packet.addElement('query', 'jabber:iq:roster')
    packet.addCallback(roster_result_handler, cljid)
    reactor.callFromThread(packet.send, cljid)

def roster_result_handler(cljid, x):
    if x['type']=='result':
        if cljid in ROSTER.keys():
            ROSTER[cljid].clear()
        query = element2dict(x)['query']
        query = [i.attributes for i in query.children if i.__class__==domish.Element]
        if not cljid in ROSTER:
            ROSTER[cljid] = {}
        for c in query:
            try: ROSTER[cljid][c['jid']]=c['subscription']
            except: pass

def hnd_roster_del(t, s, p):
    if p:
        roster_del(p, s[3])
        reply(t, s, u'ok')
        
def roster_del(jid, cljid):
    q = domish.Element(('jabber:client', 'iq'))
    q['type'] = 'set'
    q['id'] = str(random.randrange(1,999))
    query = q.addElement('query', 'jabber:iq:roster')
    i = query.addElement('item')
    i['jid'] = jid
    i['subscription'] = 'remove'
    reactor.callFromThread(dd, q, CLIENTS[cljid])

def hnd_roster_add(t, s, p):
    if p:
        roster_add(p, s[3])
        reply(t, s, u'ok')

def roster_add(jid, cljid):
    p = domish.Element(('jabber:client', 'presence'))
    p['to'] = jid
    p['type'] = 'subscribe'
    reactor.callFromThread(dd, p, CLIENTS[cljid])

def hnd_roster_all(t, s, p):
    global ROSTER
    get_roster(s[3])
    time.sleep(1)
    if not s[3] in ROSTER:
        reply(t, s, u'Пусто!')
        return
    n=len(ROSTER[s[3]])
    reply(t, s, u'Всего контактов '+str(n)+':\n'+'\n'.join(ROSTER[s[3]].keys()))

register_command_handler(hnd_roster_del, 'roster_del', ['все'], 100, 'Удаляет контакты из ростера бота.', 'roster_del <jid>', ['roster_del any@jid.ru'])
register_command_handler(hnd_roster_add, 'roster_add', ['все'], 100, 'Добавляет контакты в ростер бота.', 'roster_add <jid>', ['roster_add any@jid.ru'])
register_command_handler(hnd_roster_all, 'roster_all', ['все'], 100, 'Выводит контакты из ростера бота.', 'roster_all', ['roster_all'])
register_stage0_init(get_roster_auto)
