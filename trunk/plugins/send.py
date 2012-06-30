# -*- coding: utf-8 -*-

def hnd_send(type, source, parameters):
    if not parameters:
        return
    if not parameters.count(' '):
        return
    jid=get_true_jid(source)
    s=parameters.split()
    if s[0].count('@con'):
        reply(type, source, u'В конфы запрещено!')
        return
    to=s[0]
    if to.isdigit():
        to=str(to)
    msg(source[3], to, u'Вам сообщение от '+jid+':\n'+' '.join(s[1:]))
    reply(type, source, u'Отправил!')
    
register_command_handler(hnd_send, 'send', ['все'], 0, 'send', 'send <JID|UIN> <body>', ['send test@jabber.ua hello'])
