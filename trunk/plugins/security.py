# -*- coding: utf-8 -*-

PAR_SCAN = {}
WARNING_TRAF = {}

def get_participant(g, cljid):
    packet = IQ(CLIENTS[cljid], 'get')
    packet['id'] = 'item'+str(random.randrange(1000, 9999))
    query = packet.addElement('query', 'http://jabber.org/protocol/muc#admin')
    i = query.addElement('item')
    i['role'] = 'participant'
    packet.addCallback(get_participant_answ, g, cljid)
    reactor.callFromThread(packet.send, g)

def get_participant_answ(g, cljid, x):
    global PAR_SCAN
    global WARNING_TRAF
    
    list=[u'jabbrik.ru',u'jabber.ru',u'talkonaut.com',u'xmpp.ru',u'jabber.ua',u'qip.ru',u'jabberon.ru']
    
    if x['type']=='result':
        if not g in PAR_SCAN:
            PAR_SCAN[g] = 0
        query = element2dict(x)['query']
        query = [i.attributes for i in query.children if i.__class__==domish.Element]
        if not query:
            PAR_SCAN[g]+=1
        if PAR_SCAN[g] >= 120:
            try: del WARNING_TRAF[g]
            except: pass
            try: del PAR_SCAN[g]
            except: pass
            print '- Security scan participant end, because 120 quest show empty list.'
            return


        notnone = 0
        
        for c in query:

            if hasattr(c, 'has_key') and c.has_key('affiliation') and c['affiliation']!='none':
                notnone+=1
                continue
            
            try: jid = c['jid'].split('/')[0]
            except: continue
            
            if not jid in SECURITY_BUF[g]['serv']:
                ban(cljid, g, jid)
                SECURITY_BUF[g]['serv'].append(jid)
            try: print len(query)
            except: pass
            try: serv = re.findall('@(.*?)/', c['jid'])[0]
            except:
                print 'serv exception'
                return
            if not serv in list and not serv in SECURITY_BUF[g]['serv']:
                ban(cljid, g, serv)
                SECURITY_BUF[g]['serv'].append(serv)
        if len(query)==notnone:
            if len(query)!=0:
                PAR_SCAN[g]+=1
        else:
            PAR_SCAN[g] = 0

    

SECURITY = {}

SECURITY_MSG = {}

SECURITY_BUF = {}

SECURITY_FILE = 'dynamic/SECURITY.txt'

def security_set(type, source, parameters):
    if not source[1] in GROUPCHATS:
        return
    jid = get_true_jid(source[1]+'/'+source[2])
    SECURITY_MSG[jid]={}
    SECURITY_MSG[jid]['step1']={}
    reply(type, source, u'Вы в меню настройки безопасности конференции, выберите дейстивие:\n1-включить/настроить лимит новых пользователей,\n0-отключить')


def security_leave(g, n, r, c, cljid):
    if g in GROUPCHATS:
        if c=='303':
            security_join(g, n, None, None, cljid)

register_leave_handler(security_leave)

LIM_INFO_LAST = 0
BOTS_GET_SELF_PRESENCE = {}

def security_join(g, n, r, a, cljid):
    global WARNING_TRAF
    global BOTS_GET_SELF_PRESENCE

    if not g in BOTS_GET_SELF_PRESENCE:
        BOTS_GET_SELF_PRESENCE[g] = {}
    if n==get_bot_nick(g):
        BOTS_GET_SELF_PRESENCE[g][n]=time.time()
    
    if time.time() - INFO['start']<60:
        return
    
    global SECURITY
    global LIM_INFO_LAST
    global SECURITY_BUF
    
    if not g in SECURITY:
        return
    
    if not 'time' in SECURITY[g] or not 'n' in SECURITY[g]:
        return
    
    
    jid = get_true_jid(g+'/'+n)

    #print jid
    if g in WARNING_TRAF.keys(): return
    #print 'join'

    try:
        if time.time()-GROUPCHATS[g][get_bot_nick(g)]['joined']<20:
            return
        if time.time()-CLIENTS_UPTIME[cljid]<30:
            return
        if time.time()-BOTS_GET_SELF_PRESENCE[g][n]<7:
            return
    except: pass

    sv = jid.split('@')[1]
    if not jid or jid==None: return
    if jid.count('@conf.') or jid.count('@conference.') or jid.count('@muc.') or jid.count('@chat.'): return
    
    acc = int(user_level(g+'/'+n, g))
    if acc>=11: return
    if not g in SECURITY_BUF.keys():
        SECURITY_BUF[g]={'time':time.time(),'n':1,'serv':[]}
    else:
        if time.time()-SECURITY_BUF[g]['time']<SECURITY[g]['time']:
            #print ''
            SECURITY_BUF[g]['n']+=1
            if SECURITY_BUF[g]['n']==SECURITY[g]['n']:
                if time.time()-LIM_INFO_LAST>860:
                    try: msg(cljid, g, u'/me Достигнут лимит Гостей.. Следующий - в топку!')
                    except: pass
                    LIM_INFO_LAST=time.time()
            if SECURITY_BUF[g]['n']>SECURITY[g]['n']:
                if not g in WARNING_TRAF.keys():
                    print '- Security muc run'
                    WARNING_TRAF[g] = {}
                else: return
                privacy_set(cljid, denypm=[g])
                privacy_iq(cljid, 'active', 'ignore')
                while g in WARNING_TRAF.keys():
                    get_participant(g, cljid)
                    time.sleep(1)
                time.sleep(5)
                SECURITY_BUF[g]['n'] = 0
                
                privacy_set(cljid)
                msg(cljid, g, u'/me Перехожу в нормальный режим, список команд доступен.\nБыло выполнено банов '+str(len(SECURITY_BUF[g]['serv'])))
                
                #privacy_iq(cljid, 'active', 'ignore')
                SECURITY_BUF[g]['serv'] = []
                    

            SECURITY_BUF[g]['time']=time.time()
        else:
            SECURITY_BUF[g]['n']=1
            SECURITY_BUF[g]['time']=time.time()
            SECURITY_BUF[g]['serv']=[]

register_join_handler(security_join)

def security_msg(raw, type, source, parameters):
    if not source[1] in GROUPCHATS:
        return
    jid=get_true_jid(source[1]+'/'+source[2])
    if not jid in SECURITY_MSG or not parameters.isdigit():
        return
    db=eval(read_file(SECURITY_FILE))
    if 'step1' in SECURITY_MSG[jid]:
        if int(parameters)==1:
            del SECURITY_MSG[jid]['step1']
            SECURITY_MSG[jid]['step2']={}
            if not source[1] in db:
                db[source[1]]={}
                write_file(SECURITY_FILE,str(db))
            reply(type, source, u'Ок. Выберите промежуток во времени в секундах, за который будет вестись подщет вошедших Гостей')
            return
        if int(parameters)==0:
            del SECURITY_MSG[jid]
            if source[1] in SECURITY:
                del SECURITY[source[1]]
            if source[1] in db:
                del db[source[1]]
                write_file(SECURITY_FILE,str(db))
            reply(type, source, u'Отключено')
            return
    elif 'step2' in SECURITY_MSG[jid]:
        if int(parameters)<2:
            reply(type, source, u'Меньше двух секунд нельзя!')
            return
        if source[1] in db.keys():
            db[source[1]]['time']=int(parameters)
            write_file(SECURITY_FILE,str(db))
        del SECURITY_MSG[jid]['step2']
        SECURITY_MSG[jid]['step3']={}
        reply(type, source, u'Ок. Введите количество вошедших Гостей за '+parameters+u' секунд, после превышения которого будет включен временный автобан подозрительных серверов.')
        return
    elif 'step3' in SECURITY_MSG[jid]:
        if source[1] in db.keys():
            db[source[1]]['n']=int(parameters)
            write_file(SECURITY_FILE,str(db))
            for x in db.keys():
                SECURITY[x]=db[x]
        del SECURITY_MSG[jid]
        reply(type, source, u'Ок. Настройка завершена!')

register_message_handler(security_msg)

def security_load(cljid):
    global SECURITY
    global SECURITY_FILE
    
    db_file(SECURITY_FILE, dict)
    
    db=eval(read_file(SECURITY_FILE))
    for x in db:
        SECURITY[x]=db[x]

register_stage0_init(security_load)
register_command_handler(security_set, 'security', ['все','антивайп'], 20, 'Настройка лимита новых пользователей в конференции.', 'security', ['security'])		


