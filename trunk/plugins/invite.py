# -*- coding: utf-8 -*-

def hnd_ivite(type, source, parameters):
    if not source[1] in GROUPCHATS:
        reply(type, source, u'Команда работает только в конференции!')
        return
    if not parameters:
        return
    c = str()
    jid = None
    if parameters in GROUPCHATS[source[1]]:
        jid=get_true_jid(source[1]+'/'+parameters)
    else:
        if not parameters.count('@'):
            try:
                for x in MUC_USER[source[1]]:
                    c = x.lower()
                    if c == parameters.lower():
                        jid = MUC_USER[source[1]][x]['jid']
                        break
                if not jid:
                    reply(type, source, u'Я его не знаю')
                    return
            except:
                reply(type, source, u'Я его не знаю')
                return
        else:
            jid=parameters
    message = domish.Element(('jabber:client','message'))
    message['to'] = source[1]
    x=message.addElement('x', 'http://jabber.org/protocol/muc#user')
    inv = x.addElement('invite')
    inv['to'] = jid
    inv.addElement('reason').addContent(u'Вас приглашает '+source[2])
    #print unicode(message.toXml())
    reactor.callFromThread(dd, message, CLIENTS[source[3]])
    reply(type, source, u'Инвайт отправлен!')

register_command_handler(hnd_ivite, 'призвать', ['мук','все'], 10, 'Может приглашать заданного пользователя в конференцию', 'призвать [ник/JID]', ['призвать guy@jabber.aq'])

