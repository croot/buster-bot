# -*- coding: utf-8 -*-

#portable from http://cvs.berlios.de/svnroot/repos/freq-dev/trunk/src/plugins/query/version.py

from busterapi import opener

###############

def hnd_version(t, s, p):
    jid = p
    if s[1] in GROUPCHATS.keys() and p in GROUPCHATS[s[1]].keys():
        jid = s[1]+'/'+p
    packet = IQ(CLIENTS[s[3]], 'get')
    q = packet.addElement('query', 'jabber:iq:version')
    packet.addCallback(version_result_handler, t, s, p)
    reactor.callFromThread(packet.send, jid)

def version_result_handler(t, s, p, x):
    if x['type'] == 'error':
        reply(t, s, u'Сервис ответил ошибкой')
    else:
        query = element2dict(x)['query']
        r = element2dict(query)
        reply(t, s, p+u' использует клиент: '+r.get('name')+u'\nверсия: '+r.get('version')+u'\nось: '+r.get('os'))
   
register_command_handler(hnd_version, '!в', ['все'], 0, 'Показывает версию юзера в конференции либо сервера', '!в ник либо жид', ['!в вася'])
