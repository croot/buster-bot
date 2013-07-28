#!/usr/bin/env python 
# -*- coding: utf8 -*-

#Edit 06.04.13

RBOT = [u'mafia_bot@jabber.cz/JabberBot',u'mafia@oneteam.im/JabberBot', u'mafiozo@worldskynet.net/pybot', u'mafia@oneteam.im/JabberBot','bot@oneteam.im/JabberBot']
REPITER_BOTS = [u'mafia_bot@jabber.cz/JabberBot',u'mafia@oneteam.im/JabberBot']
MAFIA_REMOTE = {}

FROM_BOT_CLIENT = {}

REPLACE_CLJID = {}

MF_GET_RES = {}

VALID_MJID = {}

MAFIA_REPITER = {}

REPITER_JID = {}

CMD_MNAME = '.мафия'

db_file('dynamic/mrecovery.txt', dict)

MAFIA_REMOTE = eval(read_file('dynamic/mrecovery.txt'))

if CMD_MNAME in COMMANDS.keys():
    CMD_MNAME = '?мафия'

MAFIA_MEM = {}

def stmrep():
    return [x for x in MAFIA_REPITER.keys() if time.time()-MAFIA_REPITER[x]<600]

def mafiozo_leave_handler(g, n, r, a, cljid):
    jid, f = get_true_jid(g+'/'+n), 'off'
    
    if jid in MAFIA_REMOTE.keys():
        if MAFIA_REMOTE[jid]['private'] == g+'/'+n:
             mafiozo_send_iq(cl, MAFIA_REMOTE[jid]['bot'], f, f, jid, 'public')

            
register_leave_handler(mafiozo_leave_handler)

LAST_VALID_JID_QUEST = 0

def mafiozo_send_iq(cl = None, botjid = None, body = None, id = None, jid = None, typ = None, nick = None, cityid=None):
    global REPLACE_CLJID
    global LAST_VALID_JID_QUEST
    global FROM_BOT_CLIENT
    if not REPLACE_CLJID and len(CLIENTS)>1 and time.time()-LAST_VALID_JID_QUEST>7:
        LAST_VALID_JID_QUEST = time.time()
        for x in CLIENTS.keys():
            if x==cl:
                continue
            mafiozo_send_iq(x, botjid, body, id, jid, typ, nick, cityid)
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
    if cityid: query['cityid'] = cityid
    query.addContent(body)
    if botjid in FROM_BOT_CLIENT.keys():
        cl = FROM_BOT_CLIENT[botjid]
    #try:
    #    print iq.toXml(),'send\n',cl
    #except:
    #    pass
    reactor.callFromThread(CLIENTS[cl].send, iq)

def mafiozo_resiq(cl, to, id):
    global REPLACE_CLJID
    if len(REPLACE_CLJID)>0 and not cl in REPLACE_CLJID.keys():
        cl = random.choice(REPLACE_CLJID.keys())
    iq = domish.Element(('jabber:client', 'iq'))
    iq['type'] = 'result'
    iq['id'] = id
    iq['to'] = to
    query = iq.addElement('query', 'xmpp:iq:mafia')
    reactor.callFromThread(dd, iq, CLIENTS[cl])
 

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
    global MAFIA_REPITER

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
            
            MAFIA_REMOTE[jid] = {'bot':MF_GET_RES[n]['jid'], 'private':private, 'spec':None, 'cl':s[3]}
            
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


TEMP_TT = {}    
      
def iq_mafiozo(iq, cljid):
    global TEMP_TT #delete
    
    global MAFIA_REMOTE
    global RBOT 
    global MF_GET_RES
    global MAFIA_MEM
    global REPLACE_CLJID
    global MAFIA_REPITER
    global VALID_MJID
    global REPITER_JID
    global REPITER_BOTS


    try: fromjid = iq['from']
    except: return

    if fromjid.split('/')[0] == cljid:
        return
    if fromjid.split('/')[0] in CLIENTS.keys():
        return

    nsuri = (iq.firstChildElement().uri if hasattr(iq.firstChildElement(),'uri') else '')
    if nsuri!= 'xmpp:iq:mafia': return


    TEMP_TT[iq]={}


    id = iq.getAttribute('id')


    if not fromjid in RBOT:
        botjid = None
        ###  REPITER STANZA PROCESSING
        if iq.getAttribute('type')=='error':
            return
        MAFIA_REPITER[fromjid] = time.time()
        FROM_BOT_CLIENT[fromjid] = cljid

        if iq.getAttribute('type')=='set':
            try: el = iq.children[0].attributes
            except: return
            try: body = iq.children[0].__dict__['children'][0]
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
            if jid in MAFIA_REMOTE.keys():
                return
            if jid:
                if not jid in REPITER_JID.keys():
                    REPITER_JID[jid] = {'true':0, 'bot':fromjid}
                else:
                    if REPITER_JID[jid]['bot']!=fromjid:
                        if not REPITER_JID[jid]['true']:
                            REPITER_JID[jid]['bot']=fromjid
            if VALID_MJID:
                botjid = VALID_MJID.keys()[0]
                mafiozo_send_iq(cljid, botjid, body, id, jid, typ, nick)
            else:
                for x in REPITER_BOTS:
                    mafiozo_send_iq(cljid, x, body, id, jid, typ, nick)
        return



    if iq.getAttribute('type')=='result':
        
        if id in MAFIA_REMOTE and 'spec' in MAFIA_REMOTE[id]:# and MAFIA_REMOTE[id]['bot']==fromjid:
            MAFIA_REMOTE[id]['spec']=1
            return
        else:
            if id in REPITER_JID:
                REPITER_JID[id]['true'] = 1
                mafiozo_resiq(cljid, REPITER_JID[id]['bot'], id)

    if iq.getAttribute('type')=='set':

        try:
            if not fromjid in VALID_MJID:
                VALID_MJID[fromjid] = {}
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
            if not jid in MAFIA_REMOTE.keys() and (stmrep() or REPITER_JID):
                #try:
                #    print unicode(body)
                #    print iq.toXml(),'get'
                #
                #except: pass
                for x in REPITER_JID.keys():
                    if jid==x:
                        mafiozo_send_iq(cljid, REPITER_JID[x]['bot'], body, id, jid, typ, nick)
                
                if not jid in REPITER_JID.keys():
                    for x in stmrep():
                        mafiozo_send_iq(cljid, x, body, id, jid, typ, nick, cityid)
                    
            if id == u'info':
                i = len(MF_GET_RES)+1
                MF_GET_RES[i] = {'jid':fromjid,'body':body,'id':cityid}
                return

            if id == u'game_over' or id.count('game_over'):
                for x in MAFIA_REMOTE.keys():
                    if 'private' in MAFIA_REMOTE[x]:
                        body = u'Для повторного входа в игру отправьте 1 или #'
                        msg(MAFIA_REMOTE[x]['cl'], MAFIA_REMOTE[x]['private'], body)
                        MAFIA_MEM[x] = MAFIA_REMOTE[x]['bot']
                MAFIA_REMOTE.clear()
                return
            
            if not typ or typ == 'public':
                for x in [c for c in MAFIA_REMOTE.keys() if MAFIA_REMOTE[c].get('bot')==fromjid]:
                    to = MAFIA_REMOTE[x]['private']
                    msg(MAFIA_REMOTE[x]['cl'], to, body)
                return

            if jid in MAFIA_REMOTE.keys():
                try:
                    if time.time()-MAFIA_REMOTE_CALC>60:
                        MAFIA_REMOTE_CALC = time.time()
                        write_file('dynamic/mrecovery.txt',str(MAFIA_REMOTE))
                except: pass

                to = MAFIA_REMOTE[jid]['private']
                msg(MAFIA_REMOTE[jid]['cl'], to, body)
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
    
register_message_handler(mafiozo_message)     
register_command_handler(hnd_mafiozo_start, CMD_MNAME, ['все','игры'], 0, 'Ролевая психологическая онлайн игра с элементами детектива. Играть могут пользователи с разных конференций через приват бота.', CMD_MNAME, [CMD_MNAME])
