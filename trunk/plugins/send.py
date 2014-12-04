# -*- coding: utf-8 -*-

sendqueue={}


def handler_send_save(ltype, source, parameters):
	groupchat=source[1]
	test = None
	if GROUPCHATS.has_key(groupchat):
		nicks = GROUPCHATS[groupchat].keys()
		args = parameters.split(' ')
		date=time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
		fromnick=source[2]+u' из '+source[1]+u' в '+date+u' (UTC) попросил меня передать тебе следующее:\n\n'
		if len(args)>=2:
			nick = args[0]
			body = ' '.join(args[1:])
			if nick == 'админу':
				reply(ltype, source, u'передам')
				test = [msg(source[3], x, fromnick+body) for x in GLOBACCESS.keys() if GLOBACCESS[x]>40]
				return
			if get_bot_nick(groupchat) != nick:
				tojid = groupchat+'/'+nick
				if nick in nicks and GROUPCHATS[groupchat][nick]['ishere']==1:
					reply(ltype, source, u'он тут сидит')
				else:
					if not groupchat in sendqueue:
						sendqueue[groupchat]=groupchat
						sendqueue[groupchat]={}
					if not tojid in sendqueue[groupchat]:
						sendqueue[groupchat][tojid] = tojid
						sendqueue[groupchat][tojid] = []
					sendqueue[groupchat][tojid].append(fromnick+body)
					reply(ltype, source, u'передам')
					if check_file(groupchat,file='send.txt'):
						sendfp='dynamic/'+groupchat+'/send.txt'
						write_file(sendfp,str(sendqueue[groupchat]))
					else:
						print 'send_plugin.py error'
						pass

def handler_send_join(groupchat, nick, aff, role, cljid):
	tojid = groupchat+'/'+nick
	if groupchat in sendqueue:
		if sendqueue[groupchat].has_key(tojid) and sendqueue[groupchat][tojid]:
			for x in sendqueue[groupchat][tojid]:
				msg(cljid, tojid, x)
			sendqueue[groupchat][tojid] = []
			if check_file(groupchat,file='send.txt'):
				sendfp='dynamic/'+groupchat+'/send.txt'
				write_file(sendfp,str(sendqueue[groupchat]))
			else:
				print 'send_plugin.py error'
				pass
	else:
		pass
		
def get_send_cache(gch):
	sfc='dynamic/'+gch+'/send.txt'
	if not check_file(gch,'send.txt'):
		print 'error with caches in send_plugin.py'
		raise
	try:
		cache = eval(read_file(sfc))
		sendqueue[gch]={}
		sendqueue[gch]=cache
	except:
		pass	

register_join_handler(handler_send_join)
register_command_handler(handler_send_save, 'передать', ['мук','все','конференции'], 10, 'Запоминает сообщение в базе и передаёт его указанному нику как только он зайдёт в конференцию.Если указать вместо nick админу, то сообщение будет передано админам бота.', 'передать <кому> <что>', ['передать Nick привет! забань Nick666'])

register_stage1_init(get_send_cache)

ANON_CHAT = {}

def hnd_send_an(type, source, parameters):
    global ANON_CHAT
    
    jid = get_true_jid(source)

    if 'MAFIA' in globals().keys() and jid in MAFIA.keys():
        reply(type, source, u'Команду можно использовать выйдя из мафии!')
        return

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
        reply(type, source, u'Ок, чат закрыт!')
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
    reply(type, source, u'Чат с '+parameters+u' открыт!\nДалее можете писать текст в приват без команды!')
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
    
    if 'MAFIA' in globals().keys() and jid in MAFIA.keys():
        return

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
register_command_handler(hnd_send_an, 'анон_чат', ['все'], 0, 'Анонимный чат с указанным в качестве параметров JID-oм или UIN.\nШаг 1. активируем чат указав JID.\n2.Просто пишем ваш текст в приват боту.\n3.Для закрытия используем команду без параметров.', 'анон_чат <JID|UIN>', ['анон_чат test@jabber.ua'])
