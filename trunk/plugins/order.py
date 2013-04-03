#===istalismanplugin===
# -*- coding: utf-8 -*-

FILTER = {}

FILTER_USER = {}

filtd = {'fly':u'Фильтр полетов','prs':u'Фильтр презенсов ( >5 с интервалом <5 минут)','nick':u'Фильтр частой смены никa ( >1 за 30 сек.)','caps':u'Фильтр по наличию капса в презенсе (примитивные спам-боты, примитивные jabber клиенты)','stmsg':u'Фильтр длинных статусных сообщений ( >150 )','like':u'Фильтр одинаковых сообщений','len':u'Фильтр длинных сообщений','speed':u'Фильтр скорости отправки сообщений','traf':u'Фильтр траффика (презенсы и сообщения от ника суммарный объем которых >1500байт за 25сек.)'}
    
ORDER_FILE = 'dynamic/filt.txt'


def hnd_filter_msg(r, t, s, p):
    global FILTER
    global FILTER_USER
    if not p: return
    if not s[1] in FILTER.keys(): return
    if s[2]==get_bot_nick(s[1]): return
    if not s[1] in FILTER_USER.keys():
        FILTER_USER[s[1]]={}
    jid = get_true_jid(s)
    if not jid in FILTER_USER[s[1]]:
        FILTER_USER[s[1]][jid]={'traf':0, 'traftimer':0, 'prsl':0, 'lastprs':0, 'lastmsg':'','lastmsgtime':0, 'nick':0,'lastnick':0}

    if FILTER[s[1]].has_key('traf'):
        if time.time()-FILTER_USER[s[1]][jid]['traftimer']>25:
            FILTER_USER[s[1]][jid]['traftimer']=time.time()
            FILTER_USER[s[1]][jid]['traf']=0
        else:
            if FILTER_USER[s[1]][jid]['traf']>1500:
                filter_moderate(s, FILTER[s[1]]['traf'], u'Много трафика!'+str(FILTER_USER[s[1]][jid]['traf']))
        FILTER_USER[s[1]][jid]['traf']+=sys.getsizeof(p)
            
    if FILTER[s[1]].has_key('like'):
        if FILTER_USER[s[1]][jid]['lastmsg']==p and time.time()-FILTER_USER[s[1]][jid]['lastmsgtime']<60:
            filter_moderate(s, FILTER[s[1]]['like'], u'Сообщения слишком похожи!')
            
    if FILTER[s[1]].has_key('len'):
        if len(p)>1000:
            filter_moderate(s, FILTER[s[1]]['len'], u'Сообщение слишком большое!')
            
    if FILTER[s[1]].has_key('speed'):
        if time.time()-FILTER_USER[s[1]][jid]['lastmsgtime']<2 and FILTER_USER[s[1]][jid]['lastmsg']:
            filter_moderate(s, FILTER[s[1]]['speed'], u'Слишком быстро отправляешь!')
            
    FILTER_USER[s[1]][jid]['lastmsg']=p
    FILTER_USER[s[1]][jid]['lastmsgtime']=time.time()
    

register_message_handler(hnd_filter_msg)


def hnd_filter_prs(prs, cljid):
    global FILTER
    global FILTER_USER

    
    try: jid = prs['from'].split('/')
    except: return
    
    groupchat = jid[0]
    nick = prs['from'][len(groupchat)+1:]

    if groupchat in GROUPCHATS and nick == get_bot_nick(groupchat):
        return

    try: type = prs['type']
    except: type = None

    s = [groupchat+'/'+nick, groupchat, nick, cljid]
    
    if not groupchat in FILTER.keys(): return
    
    if not groupchat in FILTER_USER.keys():
        FILTER_USER[groupchat]={}
        
    jid = get_true_jid(groupchat+'/'+nick)

    if not jid in FILTER_USER[groupchat].keys():
        FILTER_USER[groupchat][jid]={'lfly':0, 'traf':0, 'traftimer':0, 'prsl':0, 'lastprs':0, 'lastmsg':'','lastmsgtime':0,'nick':0,'lastnick':0}
    
    stmsg, status, afl, role, code, reason, caps = '', '', '', '', '', '', ''
    try:
        _x = [i for i in prs.children if (i.name=='x') and (i.uri == 'http://jabber.org/protocol/muc#user')][0]
        _item = [i for i in _x.children if i.name=='item'][0]
        try: caps = [i for i in prs.children if (i.name=='c') and (i.uri == 'http://jabber.org/protocol/caps')]
        except: pass
        try: stmsg = [i for i in prs.children if i.name=='status'][0].children[0]
        except: pass
        try: status = [i for i in prs.children if i.name=='show'][0].children[0]
        except: pass
        try: afl = _item['affiliation']
        except: pass
        try: role = _item['role']
        except: pass
        try: code = ''.join([i['code'] for i in _x.children if i.name=='status'])
        except: pass
        try: reason = [i for i in _item.children if i.name=='reason'][0].children[0]
        except: pass
    except: pass
    if role == "moderator": return
    
    if FILTER[groupchat].has_key('traf'):
        if time.time()-FILTER_USER[groupchat][jid]['traftimer']>25:
            FILTER_USER[groupchat][jid]['traftimer']=time.time()
            FILTER_USER[groupchat][jid]['traf']=0
        else:
            if FILTER_USER[groupchat][jid]['traf']>1500:
                filter_moderate(s, FILTER[groupchat]['traf'], u'Много трафика!')
        FILTER_USER[groupchat][jid]['traf']+=sys.getsizeof(prs)
        
    if FILTER[groupchat].has_key('caps') and not caps:
        filter_moderate(s, FILTER[groupchat]['caps'], u'Фильтр по наличию caps клиента!')
    if FILTER[groupchat].has_key('fly'):
        if time.time()-FILTER_USER[groupchat][jid]['lastprs']<=70:
            FILTER_USER[groupchat][jid]['lfly']+=1
            if FILTER_USER[groupchat][jid]['lfly']>4:
                FILTER_USER[groupchat][jid]['lfly']=0
                filter_moderate(s, FILTER[groupchat]['fly'], u'Хватит летать!')
        else:
            FILTER_USER[groupchat][jid]['lfly']=0
    if FILTER[groupchat].has_key('prs'):
        if time.time()-FILTER_USER[groupchat][jid]['lastprs']>300:
            FILTER_USER[groupchat][jid]['lprs']=0
        else:
            FILTER_USER[groupchat][jid]['lprs']+=1
            if FILTER_USER[groupchat][jid]['lprs']>5:
                filter_moderate(s, FILTER[groupchat]['prs'], u'Презенс-флуд!')
    if code=='303' and FILTER[groupchat].has_key('nick'):
        if time.time() - FILTER_USER[groupchat][jid]['lastnick']<30:
            filter_moderate(s, FILTER[groupchat]['nick'], u'Частая смена ника!')
        FILTER_USER[groupchat][jid]['lastnick']=time.time()
    if FILTER[groupchat].has_key('stmsg') and len(stmsg)>150:
        filter_moderate(s, FILTER[groupchat]['stmsg'], u'Статус-флуд!')
    FILTER_USER[groupchat][jid]['lastprs']=time.time()
    

def filter_moderate(s, mode, reason):
    jid_nick = 'nick'
    rol_affl = 'role'
    set_to = 'none'
    user = s[2]

    jid = get_true_jid(s)
    if not isinstance(mode, basestring):
        mode = 'kick'
    
    if mode == 'ban':
        jid_nick = 'jid'
        rol_affl = 'affiliation'
        set_to = 'outcast'
        user = jid

    packet = IQ(CLIENTS[s[3]], 'set')
    query = packet.addElement('query', 'http://jabber.org/protocol/muc#admin')
    i = query.addElement('item')
    i[jid_nick] = user
    i[rol_affl] = set_to
    i.addElement('reason').addContent(reason)
    reactor.callFromThread(packet.send, s[1])

def hnd_filt_con(t, s, p):
    
    if not s[1] in GROUPCHATS: return

    rep=''
    
    ORDER_FILE = 'dynamic/filt.txt'
    db_file(ORDER_FILE, dict)
    db = eval(read_file(ORDER_FILE))
    d = {'fly':u'Фильтр полетов','prs':u'Фильтр презенсов','nick':u'Фильтр частой смены никa','caps':u'Фильтр по наличию капса в презенсе','stmsg':u'Фильтр длинных статусных сообщений','like':u'Фильтр одинаковых сообщений','len':u'Фильтр длинных сообщений','speed':u'Фильтр скорости отправки сообщений','traf':u'Фильтр траффика'}
    if p in ['off','0']:
        if s[1] in FILTER.keys():
            del FILTER[s[1]]
        write_file(ORDER_FILE, str(FILTER))
        reply(t, s, u'Все фильтры отключены!')
        return
    if p.count(' '):
        sp=p.split()
        if not sp[0].lower() in d.keys():
            reply(t, s, sp[0].lower()+u' нету в списке фильтров! Доступные фильтры '+', '.join(d.keys()))
            return
        if sp[1] in ['0','1']:
            if not s[1] in FILTER.keys():
                FILTER[s[1]]={}
            if sp[1]=='1':
                FILTER[s[1]][sp[0].lower()]={}
                write_file(ORDER_FILE, str(FILTER))
                reply(t, s, d[sp[0].lower()]+u' теперь включен!')
                return
            if sp[1]=='0':
                if sp[0].lower() in FILTER[s[1]]:
                    del FILTER[s[1]][sp[0].lower()]
                    write_file(ORDER_FILE, str(FILTER))
                    reply(t, s, d[sp[0].lower()]+u' отключен!')
                    return
            pass
        if len(sp)>2 and sp[1].lower() in ['mode'] and sp[2].lower() in ['kick','ban']:
            FILTER[s[1]][sp[0].lower()]=sp[2].lower()
            write_file(ORDER_FILE, str(FILTER))
            reply(t, s, u'ok')
        return
    if not p:
        if not s[1] in FILTER.keys():
            reply(t, s, u'Все фильтры выключены!')
            return
        on=[d[x] for x in FILTER[s[1]].keys()]
        off=[d[x] for x in d.keys() if not x in FILTER[s[1]].keys()]
        if not on:
            reply(t, s, u'Все фильтры выключены!')
            return
        rep+=u'Включены:\n'+',  '.join(on)
        if off: rep+=u'\nОтключены:\n'+',  '.join(off)
        reply(t, s, rep)
    else:
        reply(t, s, u'Смотри помощь по команде!')

def order_load(cl):
    global FILTER
    global ORDER_FILE
    if not FILTER:
        db_file(ORDER_FILE, dict)
        db=eval(read_file(ORDER_FILE))
        FILTER=db.copy()

register_stage0_init(order_load)        
register_presence_handler(hnd_filter_prs)
register_command_handler(hnd_filt_con, 'filt', ['все'], 20, 'Фильтр чата. Ключи: '+',\n '.join([x+' - '+filtd[x] for x in filtd.keys()]).encode('utf8')+'\nЧтобы включить или отключить определенный фильтр используем filt имя_фильтра и 1 для включения либо 0 для отключения например filt prs 1', 'filt <prs|stmsg|nick|len|caps|like|speed|traf|0|off> <0|1>', ['filt caps 1','filt len mode ban','filt','filt 0'])               
