# -*- coding: utf-8 -*-

import urllib2,re,urllib

MAFIA_REMOTE={}

MF_GET_RES={}

RBOT=[]

def hnd_botremotemaf(raw, type, source, parameters):
    global MAFIA_REMOTE
    global RBOT
    global MF_GET_RES
    if parameters!=u'[no text]': return
    body, ns = '',''
    for e in raw.elements():
        if e.name == "x":
            body=e.__str__()
            ns=e.uri.__str__()
    if not body: return
    try: id = raw['id']
    except: id = '1'
    jid=get_true_jid(source[1]+'/'+source[2])
    if not jid in RBOT:
        return
    sp=ns.split(':')
    jj=sp[0]
    if id==u'info':
        #print 'info'
        i=len(MF_GET_RES)+1
        MF_GET_RES[i]={'jid':jid,'body':body}
        return
    if id==u'game_over':
        MAFIA_REMOTE.clear()
        return
    if id==u'vcard':
        if len(jj.split('@'))==2 and jj.split('@')[1]==u'icq.proc.ru':
            jj=jj.split('@')[0]
        get_mvcard(jid, jj)
        return
    if sp[0] in MAFIA_REMOTE.keys():
        jj=MAFIA_REMOTE[sp[0]]['private']
        if len(jj.split('@'))==2 and jj.split('@')[1]==u'icq.proc.ru':
            jj=jj.split('@')[0]
        msg(jj, body)

def get_mvcard(bot, user):
    if not user.isdigit(): return
    if not ENABLE_ICQ in ['1']: return
    ICQ.getShortInfo(user).addCallback(get_mresult, bot, user)

def get_mresult(bot, user, x):
    if not x: return
    x=' '.join(x)
    enc=chardet.detect(x)['encoding']
    try: mr_send(bot, x.decode(enc),'1',user+':x:public')
    except: pass

def mafia_get_info():
    if RBOT:
        for x in RBOT:
            if x!=JABBER_ID:
                mr_send(x,u'info','1','none@tld:x:public')

def mr_send(to, body, id, ns):
        message = domish.Element(('jabber:client','message'))
	message["to"] = jid.JID(to).full()
	message["type"] = "chat"
	message["id"] = id
	message.addElement("body", "jabber:client", "[no text]")
	message.addElement('x', ns, body)
	#global JAB
	#JAB.send(message)
	reactor.callFromThread(dd, message)


def mafremote_register(type, source, parameters):
    global MAFIA_REMOTE
    global MF_GET_RES
    rep=''
    jid=get_true_jid(source[1]+'/'+source[2])
    if source[0].isdigit():
        jid=source[0]+'@icq.proc.ru'
    nick=''
    if source[1] in GROUPCHATS.keys():
        nick=source[2]
    else:
        nick=jid.split('@')[0]
    try:
        if jid in MAFIA.keys():
            reply(type, source, u'you must leave from game to do this!')
            return
    except:
        pass
    if jid in MAFIA_REMOTE.keys() and not parameters:
        mr_send(MAFIA_REMOTE[jid]['bot'],'1','off',jid+':x:public')
        del MAFIA_REMOTE[jid]
        reply(type, source, u'Ок. Вы вышли из Игры!')
        return
    if parameters.isdigit():
        if int(parameters) in range(1, 9):
            if int(parameters) in MF_GET_RES:
                private=source[1]+'/'+source[2]
                if source[0].isdigit():
                    private=source[0]
                MAFIA_REMOTE[jid]={'bot':MF_GET_RES[int(parameters)]['jid'],'private':private}
                mr_send(MF_GET_RES[int(parameters)]['jid'],'1234','1',jid+':x:'+nick)
                return
            else:
                reply(type, source, u'Партия с таким номером не найденa!')
                return
    if not RBOT:
        reply(type, source, u'При инициализации небыло загружено ни одного jabberID игровых ботов!Повторите попытку через минуту!')
        mafia_url_get_jid()
        return
    MF_GET_RES.clear()
    mafia_get_info()
    t=time.time()
    while not MF_GET_RES and time.time() - t<5:
        time.sleep(1)
        pass
    if not MF_GET_RES:
        reply(type, source, u'извините, на данный момент сервер недоступен!')
        return
    for x in MF_GET_RES.keys():
        try:
            rep+=str(x)+'. '+MF_GET_RES[x]['body']+'\n'
        except:
            pass
    reply(type, source, u'Вот че я нашел:\n'+rep+u'\nВыберите номер партии, например:\n !мафия 1')


def mremote_msg(raw, type, source, parameters):
    if not parameters:
        return
    if parameters.lower() in COMMANDS or type=='groupchat':
        return
    if parameters.count(' '):
        s=parameters.split()
        if s[0].lower() in COMMANDS.keys():
            return
    jid=get_true_jid(source[1]+'/'+source[2])
    t='public'
    if source[0].isdigit():
        jid=source[0]+'@icq.proc.ru'
    if jid in MAFIA_REMOTE.keys():
        mr_send(MAFIA_REMOTE[jid]['bot'], parameters, str(random.randrange(0,222)), jid+':x:'+t)


def mfremote_leave(groupchat, nick, nw, nr):
    jid=get_true_jid(groupchat+'/'+nick)
    if jid in MAFIA_REMOTE.keys():
        if MAFIA_REMOTE[jid]['private']==groupchat+'/'+nick:
            mr_send(MAFIA_REMOTE[jid]['bot'],'1','off',jid+':x:public')


def mafia_url_get_jid():
    time.sleep(1)
    for x in [u'http://tysa.1gb.ru/mafia.txt',u'http://talisman.wen.ru/mafia.txt']:
        try:
            req = urllib2.Request(x)
            r = urllib2.urlopen(req)
            page = r.read().replace('\r','').split('\n')
            if page:
                for c in page:
                    c=c.strip()
                    if not c in RBOT and c.count('@'):
                        RBOT.append(c)
        except:
            pass

register_message_handler(hnd_botremotemaf)
register_leave_handler(mfremote_leave)        
register_message_handler(mremote_msg)
register_stage0_init(mafia_url_get_jid)    
register_command_handler(mafremote_register, '.мафия', ['все','игры'], 0, 'Игра мафия', '!мафия', ['!мафия'])

