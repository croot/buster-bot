# -*- coding: utf-8 -*-

def hnd_presence_access(x, cljid):
    try: hnd_presence_access_(x, cljid)
    except: pass

def hnd_presence_access_(x, cljid):
    jid = x['from'].split('/')
    groupchat = jid[0]
    nick = x['from'][len(groupchat)+1:]
    _x = [i for i in x.children if (i.name=='x') and (i.uri=='http://jabber.org/protocol/muc#user')][0]
    _item = [i for i in _x.children if i.name=='item'][0]
    afl = _item['affiliation']
    
    role = _item['role']
   
    try: realjid = _item['jid']
    except: realjid = x['from']
    
    hnd_prs_access(groupchat, nick, afl, role, cljid)

register_presence_handler(hnd_presence_access)

def hnd_prs_access(groupchat, nick, aff, role, cljid):
    if not groupchat in GROUPCHATS:
        return
    
    jid = get_true_jid(groupchat+'/'+nick)
    
    if jid in GLOBACCESS:
        return
    
    acc_aff, acc_role = 0, 0
    if role in ROLES:
        acc_role = ROLES[role]
    else:
        acc_role = 0
    if aff in AFFILIATIONS:
        acc_aff = AFFILIATIONS[aff]
    else:
        acc_aff = 0
    access = acc_aff+acc_role
    global ACCBYCONF
    try: level = int(access)
    except: level = 1
    if not ACCBYCONF.has_key(groupchat):
        ACCBYCONF[groupchat] = {}
    ###fixed
    ACCBYCONF[groupchat][jid]=level 
			

def check_s2s(cljid):
    db=eval(read_file('dynamic/chatroom.list'))
    if cljid in db.keys() and db[cljid]:
        for gch in db[cljid].keys():
            #if not gch in GROUPCHATS.keys():
            #    continue
            packet = IQ(CLIENTS[cljid], 'get')
            packet.addElement('query', 'jabber:iq:version')
            packet.addCallback(s2s_result_handler, gch, cljid)
            reactor.callFromThread(packet.send, gch+'/'+get_bot_nick(gch))
    reactor.callLater(480, check_s2s, cljid)

def s2s_result_handler(gch, cljid, x):
    if x['type'] == 'error':
        try: code = [c['code'] for c in x.children if (c.name=='error')]
        except: code = []
        if not ' '.join(code) in ['405']:
            threading.Timer(60, join(gch, get_bot_nick(gch), cljid))

BPING_STAT = {}
BPING_W = 0
BPING_LAST = 0

def check_jids_connect_start(*an):
    global BPING_W
    if BPING_W:
        return
    BPING_W = 1
    check_jids_connect()
    

def check_jids_connect(*an):
    global BPING_W
    global BPING_STAT
    global BPING_LAST

    BPING_LAST = time.time()

    def sender(packet, cljid, tt):
        if hasattr(packet, 'send'):
            d = packet.send()
            d.addErrback(errping, cljid)
            d.addCallback(resping, cljid, tt)

    def errping(x, cljid):
        print '- JID restart because self ping timeout (>120s)'
        try: CLIENTS[cljid].transport.abortConnection()
        except: pass

        
    def resping(x, cljid, i):
        global BPING_STAT
        if not hasattr(x, '__getitem__'):
            return
        if x['type'] == 'result':
            t = time.time()
            n = t-i
            print 'res ',n
            tl = time.localtime()
            BPING_STAT[cljid]['last']=str(round(n, 3))
            if n>10:
                BPING_STAT[cljid]['hist'][str(tl[2])+' ('+str(tl[3])+':'+str(tl[4])+')']=str(round(n, 3))
            if n>=50:
                BPING_STAT[cljid]['fail']+=1
                if BPING_STAT[cljid]['fail']>=3:
                    BPING_STAT[cljid]['fail'] = 0
                    print '- JID restart because self ping quest three times timeout (>50s).'
                    try: CLIENTS[cljid].transport.abortConnection()
                    except: pass
                    return
            else:
                if BPING_STAT[cljid]['fail']!=0:
                    BPING_STAT[cljid]['fail']=0

    if CLIENTS:
        for cljid in CLIENTS.keys():
            if not cljid in BPING_STAT.keys():
                BPING_STAT[cljid]={'hist':{},'fail':0,'last':0}
    
    ##print 'botping',round(n, 3)
    #threading.Timer(120, check_jids_connect,(cljid)).start()
            packet = xmlstream.IQ(CLIENTS[cljid], 'get')
            packet.timeout = 120
            packet['id'] = str(random.randrange(1,9999))
            packet['to'] = cljid+'/JabberBot'
            packet.addElement('query', 'jabber:iq:version')
            reactor.callFromThread(sender, packet, cljid, time.time())
    reactor.callLater(300, check_jids_connect)

def hnd_sping_stat(t, s, p):
    rep = str()
    for x in BPING_STAT.keys():
        if BPING_STAT[x]['hist']:
            rep+='\n'+x+':\n'
            for c in BPING_STAT[x]['hist']:
                rep+=c+' ping sec. - '+BPING_STAT[x]['hist'][c]
    if not rep or rep.isspace():
        reply(t, s, u'Все в порядке! Последний запрос '+timeElapsed(time.time()-BPING_LAST))
    else:
        reply(t, s, rep)

register_command_handler(hnd_sping_stat, 'sping', ['все'], 0, 'Показывает статистику собственного пинга подключений в XMPP', 'sping', ['sping'])
register_stage0_init(check_jids_connect_start)
register_stage0_init(check_s2s)
register_join_handler(hnd_prs_access)
