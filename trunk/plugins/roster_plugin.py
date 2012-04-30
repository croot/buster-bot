# -*- coding: utf-8 -*-

ROSTER = {}

def get_roster_auto():
    time.sleep(6)
    get_roster()

def get_roster():
    packet = IQ(JAB, 'get')
    packet.addElement('query', 'jabber:iq:roster')
    packet.addCallback(roster_result_handler)
    reactor.callFromThread(packet.send, JABBER_ID)

def roster_result_handler(x):
    if x['type']=='result':
        ROSTER.clear()
        query = element2dict(x)['query']
        query = [i.attributes for i in query.children if i.__class__==domish.Element]
        for c in query:
            try:
                ROSTER[c['jid']]=c['subscription']
            except: pass

def hnd_roster_del(t, s, p):
    if p:
        roster_del(p)
        reply(t, s, u'ok')
        
def roster_del(jid):
    q = domish.Element(('jabber:client', 'iq'))
    q['type'] = 'set'
    q['id'] = str(random.randrange(1,999))
    query = q.addElement('query', 'jabber:iq:roster')
    i = query.addElement('item')
    i['jid'] = jid
    i['subscription'] = 'remove'
    reactor.callFromThread(dd, q)

def hnd_roster_add(t, s, p):
    if p:
        roster_add(p)
        reply(t, s, u'ok')

def roster_add(jid):
    p = domish.Element(('jabber:client', 'presence'))
    p['to'] = jid
    p['type'] = 'subscribe'
    reactor.callFromThread(dd, p)

def hnd_roster_all(t, s, p):
    global ROSTER
    get_roster()
    time.sleep(1)
    if not ROSTER:
        reply(t, s, u'Пусто!')
        return
    n=len(ROSTER)
    reply(t, s, u'Всего контактов '+str(n)+':\n'+'\n'.join(ROSTER.keys()))

register_command_handler(hnd_roster_del, 'roster_del', ['все'], 100, 'Удаляет контакты из ростера бота.', 'roster_del <jid>', ['roster_del any@jid.ru'])
register_command_handler(hnd_roster_add, 'roster_add', ['все'], 100, 'Добавляет контакты в ростер бота.', 'roster_add <jid>', ['roster_add any@jid.ru'])
register_command_handler(hnd_roster_all, 'roster_all', ['все'], 100, 'Выводит контакты из ростера бота.', 'roster_all', ['roster_all'])
register_stage0_init(get_roster_auto)
