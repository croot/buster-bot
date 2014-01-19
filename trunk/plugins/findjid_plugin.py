#===istalismanplugin===
# -*- coding: utf-8 -*-

FIND_JID = {}

def hnd_find_jid(t, s, p):
    if not p:
        reply(t, s, u'?')
        return
    reply(t, s, u'Поиск начат')
    global FIND_JID
    jid = get_true_jid(s)
    FIND_JID[jid] = {}
    for x in GROUPCHATS:
        for c in ['owner','admin','member','outcast']:
            try: packet = IQ(CLIENTS[GROUPCHATS[x][get_bot_nick(x)]['jid'].split('/')[0]], 'get')
            except: continue
            packet['id'] = 'item'+str(random.randrange(1000, 9999))
            query = packet.addElement('query', 'http://jabber.org/protocol/muc#admin')
            i = query.addElement('item')
            i['affiliation'] = c
            packet.addCallback(hnd_answ_find_jid, p, t, s, jid, x)
            reactor.callFromThread(packet.send, x)
    time.sleep(7)
    if not FIND_JID[jid]:
        reply(t, s, u'Ничего не найдено!')
        return
    reply(t, s, '\n'.join([x+' '+FIND_JID[jid][x] for x in FIND_JID[jid].keys()]))
    del FIND_JID[jid]

def hnd_answ_find_jid(p, t, s, jid, chat, x):
    if x['type']=='result':
        query = element2dict(x)['query']
        query = [i.attributes for i in query.children if i.__class__==domish.Element]
        if not query: return
        for c in query:
            if c['jid'].count(p):
                FIND_JID[jid][c['jid']+' '+chat]=c['affiliation']

register_command_handler(hnd_find_jid, '!найти_жид', ['все','админ'], 20, 'Поиск жида в овнер-,админ-,мембер-,бан- листах конференций.', '!найти_жид <ключ>', ['!найти_жид buster@cc.ru'])
