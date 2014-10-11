#!/usr/bin/env python 
# -*- coding: utf8 -*-

#Edit 

RBOT = [u'mafia_bot@jabber.cz/JabberBot', u'mafiozo@worldskynet.net/pybot', u'mafia@oneteam.im/JabberBot','bot@oneteam.im/JabberBot']

MAFIA_REMOTE = {}

REPLACE_CLJID = {}

MF_GET_RES = {}

CMD_MNAME = '.мафия'

db_file('dynamic/mrecovery.txt', dict)

MAFIA_REMOTE = eval(read_file('dynamic/mrecovery.txt'))

if CMD_MNAME in COMMANDS.keys():
    CMD_MNAME = '?мафия'

MAFIA_MEM = {}

def mafiozo_leave_handler(g, n, r, a, cljid):
    jid, f = get_true_jid(g+'/'+n), 'off'
    
    if jid in MAFIA_REMOTE.keys():
        if MAFIA_REMOTE[jid]['private'] == g+'/'+n:
             mafiozo_send_iq(cl, MAFIA_REMOTE[jid]['bot'], f, f, jid, 'public')

            
register_leave_handler(mafiozo_leave_handler)

def mafiozo_send_iq(cl = None, botjid = None, body = None, id = None, jid = None, typ = None, nick = None):
    global REPLACE_CLJID
    if len(REPLACE_CLJID)>0 and not cl in REPLACE_CLJID.keys():
        cl = random.choice(REPLACE_CLJID.keys())
    iq = domish.Element(('jabber:client', 'iq'))
    iq['type'] = 'set'
    iq['id'] = id
    iq['to'] = botjid
    query = iq.addElement('query', 'xmpp:iq:mafia')
    if jid: query['jid'] = jid
    if typ: query['typ'] = typ
    if nick: query['nick'] = nick
    query.addContent(body)
    reactor.callFromThread(CLIENTS[cl].send, iq)
 

def mafia_get_info(cl):
    global RBOT
    i = u'info'
    if RBOT:
        [mafiozo_send_iq(cl, x, i, i) for x in RBOT]

def mafiozo_url_jid():
    global RBOT
    time.sleep(1.5)
    for x in [u'http://mafiozo.in/mafia.txt',u'http://talisman.wen.ru/mafia.txt']:
        try:
            import urllib2 
            req = urllib2.Request(x) 
            r = urllib2.urlopen(req) 
            page = r.read().splitlines() 
            if page:
                for c in page:
                    c=c.strip() 
                    if not c in RBOT and c.count('@'):
                        RBOT.append(c) 
        except: pass

threading.Thread(None, mafiozo_url_jid, 'mafiozo_url_jid'+str(random.randrange(1,10))).start() 

      
def hnd_mafiozo_start(t, s, p):
    global MAFIA_REMOTE 
    global RBOT 
    global MF_GET_RES
    global REPLACE_CLJID

    jid = get_true_jid(s)
    nick = s[2]
    rep = str()
    JOIN = '1234'
      
    if not s[1] in GROUPCHATS:
        nick = jid.split('@')[0] 
      
    if jid in MAFIA_REMOTE.keys() and not p:
        if 'spec' in MAFIA_REMOTE[jid] and MAFIA_REMOTE[jid]['spec']:
            
            mafiozo_send_iq(s[3], MAFIA_REMOTE[jid]['bot'], 'off', 'off', jid, 'public')

            del MAFIA_REMOTE[jid]
            return
        
    if p.isdigit():

        n = int(p)
        
        if n in MF_GET_RES: 
            private = s[1]+'/'+s[2]
            
            MAFIA_REMOTE[jid] = {'bot':MF_GET_RES[n]['jid'], 'private':private, 'spec':None}
            
            mafiozo_send_iq(s[3], MF_GET_RES[n]['jid'], JOIN, str(), jid, 'public', nick)

            return
        
        else:
            reply(t, s, u'Партия с таким номером не найденa!')
            return

    MF_GET_RES.clear() 

    for x in CLIENTS.keys():
        mafia_get_info(x) 

    tt = time.time() 
      
    while not MF_GET_RES and time.time() - tt<5.5: 
        time.sleep(1) 
        pass

    time.sleep(0.5)

    if not MF_GET_RES:
        reply(t, s, u'Нет ответа от сервера. Попробуйте добавить в контакты одного из игровых ботов: '+','.join(RBOT))
        return

    SP=[]
    cid = []
    for x in MF_GET_RES.keys():
        try:
            if MF_GET_RES[x].get('id',None):
                if MF_GET_RES[x].get('id',None) in cid:
                    continue
                else: cid.append(MF_GET_RES[x].get('id',None))
            if not MF_GET_RES[x]['jid'] in SP:
                SP.append(MF_GET_RES[x]['jid'])
            else:
                continue
            rep+=str(x)+'. '+MF_GET_RES[x]['body']+'\n'
        except:
            pass
      
    reply(t, s, u'Вот че я нашел:\n'+rep+u'\nВыберите номер партии, например:\n '+CMD_MNAME.decode('utf8')+' 1') 

IQ_MFLOG = {}    
      
def iq_mafiozo(iq, cljid):
    global MAFIA_REMOTE
    global RBOT 
    global MF_GET_RES
    global MAFIA_MEM
    global REPLACE_CLJID
    global IQ_MFLOG


    try: fromjid = iq['from']
    except: return

    if fromjid.split('/')[0] == cljid or fromjid.split('/')[0] in CLIENTS.keys():
        return

    nsuri = iq.firstChildElement().uri
    if nsuri!= 'xmpp:iq:mafia': return

    if len(IQ_MFLOG)>100:
        IQ_MFLOG.clear()
    try: IQ_MFLOG[len(IQ_MFLOG)]=iq.toXml()
    except: pass


    id = iq.getAttribute('id')

    if iq.getAttribute('type')=='result':
        
        if id in MAFIA_REMOTE and 'spec' in MAFIA_REMOTE[id]:# and MAFIA_REMOTE[id]['bot']==fromjid:
            MAFIA_REMOTE[id]['spec']=1
            return

    if iq.getAttribute('type')=='set':

        try:
            if not cljid in REPLACE_CLJID:
                REPLACE_CLJID[cljid] = {}
            for x in REPLACE_CLJID:
                if not x in CLIENTS.keys():
                    del REPLACE_CLJID[x]
        except:
            pass


        fromjid = iq.getAttribute('from')
        try: el = iq.children[0].attributes
        except: return

        try: body = iq.children[0].__dict__['children'][0]#element2dict(iq).get('query',None)#iq.firstChildElement()#(None if not hasattr(el,'children') else el.children)
        except: return
        if not body: return


        try:
            jid = el.get('jid','')
            typ = el.get('typ','')
            nick = el.get('nick', '')
            cityid = el.get('cityid', '')
        except:
            jid = str()
            typ = str()
            nick = str()
            cityid = str()
        try:
            if id == u'info':
                if body.strip()==u'info':
                    return
                i = len(MF_GET_RES)+1
                MF_GET_RES[i] = {'jid':fromjid,'body':body,'id':cityid}
                return

            if id == u'game_over' or id.count('game_over'):
                for x in MAFIA_REMOTE.keys():
                    if 'private' in MAFIA_REMOTE[x]:
                        body = u'Для повторного входа в игру отправьте 1 или #'
                        msg(cljid, MAFIA_REMOTE[x]['private'], body)
                        MAFIA_MEM[x] = MAFIA_REMOTE[x]['bot']
                MAFIA_REMOTE.clear()
                return
            
            if not typ or typ == 'public':
                for x in [c for c in MAFIA_REMOTE.keys() if MAFIA_REMOTE[c].get('bot')==fromjid]:
                    to = MAFIA_REMOTE[x]['private']
                    msg(cljid, to, body)
                return

            if jid in MAFIA_REMOTE.keys():
                try:
                    if time.time()-MAFIA_REMOTE_CALC>60:
                        MAFIA_REMOTE_CALC = time.time()
                        write_file('dynamic/mrecovery.txt',str(MAFIA_REMOTE))
                except: pass

                to = MAFIA_REMOTE[jid]['private']
                msg(cljid, to, body)
        except: print 'MAFIA exception'


register_iq_handler(iq_mafiozo)
      

def mafiozo_message(r, t, s, p):

    global MAFIA_REMOTE
    
    jid, tt, nick, join = get_true_jid(s), 'public', s[2], '1234'


    if not p or p.split()[0].lower() in COMMANDS.keys():
        return

    if t in ['public','groupchat']:
        return
    
    if not s[1] in GROUPCHATS:
        nick = jid.split('@')[0]

      
    if jid in MAFIA_REMOTE.keys():
        mafiozo_send_iq(s[3], MAFIA_REMOTE[jid]['bot'], p, str(random.randrange(0,222)), jid, tt)
    else:
        if jid in MAFIA_MEM.keys() and p in [u'1',u'#']:
            if not nick:
                nick = jid.split('@')[0]
                
            botjid = MAFIA_MEM[jid]
            
            if not isinstance(botjid, basestring): return
            
            MAFIA_REMOTE[jid] = {'bot':botjid, 'private':s[1]+'/'+s[2], 'spec':0}
            mafiozo_send_iq(s[3], MAFIA_REMOTE[jid]['bot'], join, str(), jid, 'public', nick)

def hnd_maflog_show(t, s, p):
    rep = ''
    global IQ_MFLOG
    if p == 'c':
        IQ_MFLOG.clear()
        reply(t, s, 'done')
        return
    i = sorted(IQ_MFLOG)
    i.reverse()
    for x in i:
        rep+=IQ_MFLOG[x]+'\n'
    reply(t, s, rep)
    
register_message_handler(mafiozo_message)     
register_command_handler(hnd_mafiozo_start, CMD_MNAME, ['все','игры'], 0, 'Ролевая психологическая онлайн игра с элементами детектива. Играть могут пользователи с разных конференций через приват бота.', CMD_MNAME, [CMD_MNAME])
register_command_handler(hnd_maflog_show, 'mstanz', ['все'], 40, 'Тестовая команда, лог станз команды .мафия', 'mstanz', ['mstanz'])
