# -*- coding: utf-8 -*-

ANON_CHAT = {}

def hnd_send_an(type, source, parameters):
    global ANON_CHAT
    
    jid = get_true_jid(source)

    if source[1] in GROUPCHATS.keys():
        if type in ['public','groupchat']:
            jid = source[1]
        else:
            jid = source[1]+'/'+source[2]

    if not parameters:
        if not jid in ANON_CHAT.keys():
            return
        del ANON_CHAT[jid]
        try: del ANON_CHAT[''.join([x for x in ANON_CHAT.keys() if ANON_CHAT[x]['to']==jid])]
        except: pass
        reply(type, source, u'Ок, чат закрыт.')
        return

    if parameters == jid:
        reply(type, source, u'И зачем?')
        return
    
    if jid in ANON_CHAT.keys():
        if parameters==ANON_CHAT[jid]['to']:
            reply(type, source, u'Если хотите закрыть чат напишите команду без параметров!')
            return
        reply(type, source, u'В данный момент у вас уже открыт чат, eсли хотите закрыть чат напишите команду без параметров!')
        return
    s = parameters.split()
    if s[0].count('@con'):
        reply(type, source, u'В конфы запрещено!')
        return
    to=s[0]
    if to.isdigit():
        if not hasattr(ICQ, 'sendMessage'):
            reply(type, source, u'По всей видимости ICQ подключение бота не активно!')
            return
        to=str(to)

    ANON_CHAT[jid]={'to':to, 't':time.time(), 'f':1, 'b':source[3], 'n':0, 'tl':0, 'err':0}
    ANON_CHAT[to]={'to':jid, 't':time.time(), 'f':0, 'b':source[3], 'n':0, 'tl':0, 'err':0}
    
    #msg(source[3], to, u'Вам :\n'+' '.join(s[1:]))
    reply(type, source, u'Чат с '+parameters+u' открыт!')
    msg(source[3], to, u'Некто открыл с вами анонимную беседу!')


def hnd_anon_chat_msg(r, t, s, p):
    bnick=str()
    jid = get_true_jid(s)
    if s[1] in GROUPCHATS:
        bnick = get_bot_nick(s[1])
        if s[2]==bnick:
            return
        if t in ['public','groupchat']:
            jid = s[1]
        else:
            jid = s[1]+'/'+s[2]
        try:
            if p.split()[0].count(bnick):
                p = p[len(bnick)+1:].strip()
        except:
            pass
    if not p or p.isspace(): return
    ss, to = p.split(), None
    if ss[0].lower() in COMMANDS.keys(): return
    
    if 'MAFIA' in globals().keys() and jid in MAFIA.keys(): return

    global ANON_CHAT
    
    list = [x for x in ANON_CHAT.keys() if time.time()-ANON_CHAT[x]['t']>3600]
    
    if list:
        for x in list:
            if ANON_CHAT[x]['f']:
                msg(s[3], x, u'Анон чат с '+ANON_CHAT[x]['to']+u' автоматически закрыт по неактивности.')
            del ANON_CHAT[x]
            
    if jid in ANON_CHAT.keys():
        if time.time() - ANON_CHAT[jid]['tl']<2:
            if not ANON_CHAT[jid]['err']:
                ANON_CHAT[jid]['err']=1
                reply(t, s, u'Сообщения отправленные с интервалом чаще 1-го в 2 секунды не будут доставлены!')
                return
            return
        ANON_CHAT[jid]['tl'] = time.time()
        
        to = ANON_CHAT[jid]['to']

        if ANON_CHAT[jid]['n'] - ANON_CHAT[to]['n']>= 6:
            reply(t, s, u'У вас более 6-ти анонимных сообщений без ответа, дальнейшая отправка невозможна!')
            return
        ANON_CHAT[jid]['n'] +=1
        msg(s[3], to, p[:1000])

register_message_handler(hnd_anon_chat_msg)
register_command_handler(hnd_send_an, 'анон_чат', ['все'], 0, 'Анонимный чат с указанным в качестве параметров JID-oм или UIN', 'анон_чат <JID|UIN> <body>', ['анон_чат test@jabber.ua'])
