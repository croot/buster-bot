# -*- coding: utf-8 -*-

PRIVACY_DENY = []

PRIVACY_EDIT = {}

def privacy_iq(cljid='', title='', listname='', dic={}):
    q = domish.Element(('jabber:client', 'iq'))
    q['type'] = 'set'
    q['id'] = str(random.randrange(1,999))
    query = q.addElement('query', 'jabber:iq:privacy')
    i = query.addElement(title)#active/default/list
    if listname:
        i['name'] = listname
    if listname and dic:
        for x in dic.keys():
            lis = i.addElement('item')
            lis['type'] = dic[x]['type']
            lis['order'] = x
            lis['value'] = dic[x]['value']
            lis['action'] = dic[x]['action']
    reactor.callFromThread(dd, q, CLIENTS[cljid])
    

def get_privacy(t, s, p, edit=0):
    nl = ''
    global PRIVACY_EDIT
    if p:
        p=p.lower()
        ss=p.split()
        if len(ss)>1:
            if ss[0]=='edit':
                if len(ss)<5:
                    reply(t, s, u'edit <listname> <1|2|3|4..> <allow|deny> <jid|subscription> <and you parameter,like bot@jabber.ru or None>')
                    return
                if not ss[2].isdigit():
                    reply(t, s, ss[2]+u' - после названия списка должен быть указан номер правила(order)!')
                    return
                if not ss[3] in [u'allow',u'deny']:
                    reply(t, s, ss[3]+u' - может быть только deny (запретить) или allow (разрешить)')
                    return
                try:
                    PRIVACY_EDIT.clear()
                    get_privacy(t, s, ss[1], 1)
                    time.sleep(5)
                    PRIVACY_EDIT[ss[2]]={'action':ss[3],'type':ss[4],'value':ss[5]}
                    privacy_iq(s[3], 'list', ss[1], PRIVACY_EDIT)
                except: pass
                reply(t, s, u'ok')
                return
            if ss[0]=='active':
                privacy_iq(s[3], ss[0],ss[1])
                reply(t, s, u'ok')
                return
            if ss[0]=='remove':
                privacy_iq(s[3], 'list',ss[1])
                reply(t, s, u'ok')
                return
            if ss[0]=='default':
                privacy_iq(s[3], ss[0],ss[1])
                reply(t, s, u'ok')
                return
        else:
            if p == 'auto':
                privacy_set(s[3])
                reply(t, s, u'Автоматический список <<ignore>> создан!')
                return
            if p in ['0','undefault']:
                if p=='0':
                    privacy_iq(s[3], 'active')
                    reply(t, s, u'Активный список отключен!')
                    return
                if p=='undefault':
                    privacy_iq(s[3], 'default')
                    reply(t, s, u'Список по умолчанию Отключен!')
                    return
            else:
                nl = p
    packet = IQ(CLIENTS[s[3]], 'get')
    q = packet.addElement('query', 'jabber:iq:privacy')
    if nl:
        i = q.addElement('list')
        i['name'] = nl
    packet.addCallback(privacy_result_handler, t, s, nl, edit)
    reactor.callFromThread(packet.send, s[3])

rst=None

def privacy_result_handler(t, s, nl, edit, x):
    rep, n, info = '', 0, ''
    if x['type']=='result':
        #print x.toXml()
        global rst
        rst=x
        if nl:
            try:
                for c in x.children[0].children[0].elements():
                    n+=1
                    if not edit:
                        rep+=c.attributes['order']+' '+c.attributes['action']+' '+c.attributes['type']+' '+c.attributes['value']+'\n'
                    else:
                        PRIVACY_EDIT[c.attributes['order']]={'action':c.attributes['action'],'type':c.attributes['type'],'value':c.attributes['value']}
                if edit: return
                reply(t, s, '('+str(n)+'):\n'+rep)
            except: pass
            return
        try:
            if not x.elements():
                reply(t, s, u'Не найдено ни одного созданного списка!')
                return
            for i in x.elements():
                for c in i.elements():
                    DICT = {'active':u'Активный список: ','default':u'Список по умолчанию: '}
                    if c.name in DICT.keys():
                        info+= DICT[c.name]+c.attributes['name']+'\n'
                    else:
                        n+=1
                        rep+=c.attributes['name']+'\n'
            rep=u'Всего списков найдено '+str(n)+':\n'+rep+info
            reply(t, s, rep)
        except: reply(t, s, u'При получении списка приватностей произошла ошибка!')

register_command_handler(get_privacy, 'privacy', ['суперадмин','все'], 100, 'Работа со списком приватностей бота. Команда без параметров выведет список листов и их состояние.\nКлючи: auto - сформирует автоматический список ignore, active <list>, remove <list>, default <list>, undefault, edit <listname> <1|2|3> <allow|deny> <jid|subscription> <some@jabber.ua or None>\nПросто название листа в качестве параметра покажет вам его содержимое.\nЧтобы отключить все активные списки используется параметер 0.', 'privacy <key> <name_list>', ['privacy','privacy active ignore','privacy ignore','privacy remove ignore','privacy default ignore','privacy 0'])


def privacy_activ(cljid, list=''):
    q = domish.Element(('jabber:client', 'iq'))
    q['type'] = 'set'
    q['id'] = str(random.randrange(1,999))
    query = q.addElement('query', 'jabber:iq:privacy')
    i = query.addElement('active')
    if list:
        i['name'] = list
    reactor.callFromThread(dd, q, CLIENTS[cljid])


def privacy_set(cljid, deny=[]):
    n=0
    list=[u'conference.jagplay.ru',u'conference.talkonaut.com',u'conference.jabber.ru',u'conference.qip.ru']
    if 'ROSTER' in globals().keys() and cljid in ROSTER.keys():
        list.extend(ROSTER[cljid].keys())
    if 'ADMINS' in globals().keys() and ADMINS:
        list.extend(ADMINS)
    #print list
    q = domish.Element(('jabber:client', 'iq'))
    q['type'] = 'set'
    q['id'] = str(random.randrange(1,999))
    query = q.addElement('query', 'jabber:iq:privacy')
    i = query.addElement('list')
    i['name'] = 'ignore'
    if deny:
        for c in deny:
            n+=1
            lis = i.addElement('item')
            lis['type'] = 'jid'
            lis['order'] = str(n)
            lis['value'] = c
            lis['action'] = 'deny'
    for x in list:
        if x in deny:
            continue
        n+=1
        lis = i.addElement('item')
        lis['type'] = 'jid'
        lis['order'] = str(n)
        lis['value'] = x
        lis['action'] = 'allow'
    lis = i.addElement('item')
    lis['type'] = 'subscription'
    lis['order'] = str(n+1)
    lis['value'] = 'none'
    lis['action'] = 'deny'
    st1 = lis.addElement('message')
    st2 = lis.addElement('presence-in')
    #print q.toXml()
    reactor.callFromThread(dd, q, CLIENTS[cljid])
    #############

MFL_LIMIT = {}

PRIVACY_WARNING=0

def privacy_protect(raw, type, source, p):
    jid=get_true_jid(source)
    n=3
    if type in ['public','groupchat']:
        pass
    else:
        global PRIVACY_WARNING
        global PRIVACY_DENY
        global MFL_LIMIT
        if jid in [x for x in GLOBACCESS.keys() if GLOBACCESS[x]==100]: return
        if jid == JABBER_ID: return
        if jid in ROSTER:
            n=6
        if p in [u'[no text]']:
            n=10
        if not jid in MFL_LIMIT:
            MFL_LIMIT[jid]={'time':time.time(),'n':0}
        else:
            if time.time() - MFL_LIMIT[jid]['time']<1 or len(p)>1000:
                MFL_LIMIT[jid]['time']=time.time()
                if MFL_LIMIT[jid]['n']>n:
                    if jid in PRIVACY_DENY: return
                    privacy_iq(source[3], 'active', 'ignore')
                    PRIVACY_DENY.append(jid)
                    if 'roster_del' in globals().keys():
                        try: roster_del(jid, source[3])
                        except: pass
                    privacy_set(source[3], PRIVACY_DENY)
                    time.sleep(1)
                    privacy_iq(source[3], 'active', 'ignore')
                    if not PRIVACY_WARNING or time.time()-PRIVACY_WARNING>120:
                        PRIVACY_WARNING=time.time()
                        for c in [x for x in GLOBACCESS.keys() if GLOBACCESS[x]==100]:
                            msg(source[3], c, u'В связи с подозрением на спам в боте активирован список приватностей!(смотри privacy)')
                else:
                    MFL_LIMIT[jid]['n']+=1
            else:
                MFL_LIMIT[jid]['n']=0
                MFL_LIMIT[jid]['time']=time.time()

register_message_handler(privacy_protect)

def privacy_init(cljid):
    f = 'dynamic/privacy.txt'
    if not os.path.exists(f):
        initialize_file(f, '{}')

    try: txt=eval(read_file(f))
    except:
        write_file(f,'{}')
        txt={}

    if not txt or time.time() - txt.keys()[0]>8640:
        time.sleep(60)

        privacy_set(cljid)

        try: del txt[txt.keys()[0]]
        except: pass
        txt[time.time()]={}
        write_file(f, str(txt))

register_stage0_init(privacy_init)
