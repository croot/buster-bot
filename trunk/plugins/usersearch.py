# -*- coding: utf-8 -*-

USER_SEARCH = {'search':0,'chat':[],'user':[],'con':0, 'see':0, 'add_source':{}}

USER_SEARCH_HISTORY = 'dynamic/user_search_history.txt'

db_file(USER_SEARCH_HISTORY, dict)

src_con, src_cl, src_factory = None, None, None

def replace_ru_eng(body):
    body = body.replace(u'a', u'а').replace(u'A', u'А').replace(u'e', u'е').replace(u'E', u'Е').replace(u'T', u'Т').replace(u'O', u'О').replace(u'o', u'о').replace(u'p', u'р').replace(u'P', u'Р').replace(u'H', u'Н').replace(u'k', u'к').replace(u'K', u'К').replace(u'X', u'Х').replace(u'x', u'х').replace(u'C', u'С').replace(u'c', u'с').replace(u'B', u'В').replace(u'M', u'М').replace(u'Y', u'У').replace(u'0', u'О')
    return body

def hnd_usersearch_history(type, source, parameters):
    if not parameters: return
    db = eval(read_file(USER_SEARCH_HISTORY))
    if not db:
        reply(type, source, u'База данных пуста')
        return
    if parameters.lower() in [u'top']:
        sp = list()
        dic = dict()
        for x in db.keys():
            for c in db[x]:
                usr = c.split('/')[1]
                sp.append(usr)
        for x in sp:
            dic[x]=sp.count(x)
        import operator
        sr = sorted(dic.iteritems(), key=operator.itemgetter(1))
        sr.reverse()
        sr = sr[:20]
        print sr
        reply(type, source, u'Top 20 users for all conference: '+'\n'.join([str(sr.index(x)+1)+u') '+x[0]+' '+str(x[1]) for x in sr]))
        return
    rep = str()
    for x in db.keys():
        for c in db[x]:
            usr = c.split('/')[1]
            cha = c.split('/')[0]
            if usr.count(parameters):
                rep+= ' '.join([x[:19], cha, usr])+'\n'
    if rep.isspace():
        reply(type, source, u'Нет результатов')
        return
    reply(type, source, rep)

register_command_handler(hnd_usersearch_history, 'ush', ['все','поиск','юзеры'], 0, 'Поиск юзера в истории обзора конференций ботом.\n Ключ top - выведет топ 20 юзеров по всем чатам.'+('Для онлайн поиска смотрите команду отыскать' if u'отыскать' in COMMANDS.keys() else ''), 'ush <ник>', ['ush вася'])

def hnd_usersearch(type, source, parameters):
    global src_cl
    global src_con
    global src_factory
    global USER_SEARCH
    if not parameters or parameters.isspace():
        reply(type, source, u'А кого искать будем?')
        return
    tl = time.time() - USER_SEARCH['search']
    if tl < 180:
        if tl < 150 and len(USER_SEARCH['add_source'])<3:
            USER_SEARCH['add_source'][str(source)]={'p':parameters, 'rep':str()}
            reply(type, source, u'Смотри результат в привате через '+timeElapsed(180-(tl)))
        else:
            reply(type, source, u'Сейчас я выполняю другой запрос! Время до завершения - '+timeElapsed(180 - (time.time() - USER_SEARCH['search'])))
        return

    parameters = parameters.lower()
    parameters = replace_ru_eng(parameters)
    s, r, k = 0,0,0
    
    USER_SEARCH['search'] = time.time()

    reply(type, source, u'Результат смотри в привате через 3 минуты!')
    search_con()
    tim=time.time()
    while not USER_SEARCH['con'] and time.time()-tim<21:
        time.sleep(1)
        pass
    if not USER_SEARCH['con']:
        try: src_d()
        except: pass
        reply(type, source, u'Поиск остановлен из-за неудачной попытки подключения! Попробуйте позже!')
        return
    for x in ['conference.xmpp.ru','conference.jabber.ru','conference.talkonaut.com','conference.qip.ru','conference.jabbrik.ru']:
        hnd_usse_quest(x, 'chat')
    time.sleep(7)
    for x in USER_SEARCH['chat']:
        hnd_usse_quest(x, 'user')
    time.sleep(150)
    rep=''
    res=0
    DICT = {}
    for x in USER_SEARCH['user']:
        chat=x.split('/')[0]
        user=x.split('/')[1]
        user=replace_ru_eng(user)
        l=user.lower()
        if USER_SEARCH['add_source']:
            for m in USER_SEARCH['add_source']:
                try:
                    if l.count(USER_SEARCH['add_source'][m]['p']):
                        USER_SEARCH['add_source'][m]['rep']+=chat+' '+user+'\n'
                except: pass
        if l.count(parameters):
            res+=1
            rep+=chat+' '+user+'\n'
    try: [reply('private',eval(x), (USER_SEARCH['add_source'][x]['rep'] if USER_SEARCH['add_source'][x]['rep'] else u'По запросу < '+USER_SEARCH['add_source'][x]['p']+u'> cовпадений нет!')) for x in USER_SEARCH['add_source'].keys()]
    except: pass
    try:
        db=dict()
        db[str(datetime.datetime.now())] = []
        db[str(datetime.datetime.now())].extend(USER_SEARCH['user'])
        write_file(USER_SEARCH_HISTORY, str(db))
    except: pass
    all = u'\nВсего конференций: '+str(len(USER_SEARCH['chat']))+u'\nВсего юзеров: '+str(len(USER_SEARCH['user']))
    if not rep or rep.isspace():
        reply('chat', source, u'Совпадений нет!\n'+all)
        return
    reply('chat', source, u'Результатов '+str(res)+':\n'+rep[:2000]+all)
    USER_SEARCH['chat']=[]
    USER_SEARCH['user']=[]
    USER_SEARCH['search']=0
    USER_SEARCH['con']=0
    USER_SEARCH['add_source']={}
    src_d()


def hnd_usse_quest(jid, key):
    packet = IQ(src_cl, 'get')
    packet.addElement('query', 'http://jabber.org/protocol/disco#items')
    packet.addCallback(disco_result_handler, key)
    reactor.callFromThread(packet.send, jid)

def disco_result_handler(key, x):
    if x['type'] == 'result':
        #try: print unicode(x.toXml())
        #except: pass
        query = element2dict(x)['query']
        query = [i.attributes for i in query.children if i.__class__==domish.Element]
        r = [i['jid'] for i in query]
        USER_SEARCH[key].extend(r)

def authd_search(xmlstream):
    #presence = domish.Element(('jabber:client','presence'))
    #xmlstream.send(presence)
    global src_cl
    src_cl = xmlstream
    USER_SEARCH['con']=1

def src_pass(x):
    pass

def src_d():
    global src_cl
    global src_con
    global src_factory
    if hasattr(src_factory, 'stopTrying'): src_factory.stopTrying()
    if hasattr(src_con, 'disconnect'): src_con.disconnect()
    src_con = None
    src_factory = None
    src_cl = None

def search_con():
    myJid = jid.JID(JABBER_ID+'/search'+str(random.randrange(1,999)))
    global src_factory
    src_factory = client.basicClientFactory(myJid, JABBER_PASS)
    src_factory.addBootstrap('//event/stream/authd', authd_search)
    src_factory.addBootstrap('//event/client/basicauth/authfailed', src_pass)
    src_factory.addBootstrap('//event/client/basicauth/invaliduser', src_pass)
    src_factory.addBootstrap(xmlstream.STREAM_END_EVENT, src_pass)
    src_factory.addBootstrap(xmlstream.STREAM_ERROR_EVENT, src_pass)
    global src_con
    src_con = reactor.connectTCP(JABBER_ID.split('@')[1], 5222, src_factory)

register_command_handler(hnd_usersearch, 'отыскать', ['все','поиск','юзеры'], 0, 'Поиск юзера онлайн по нику в лучших чатах сети jabber.\nАвтоматически не чувствителен к капсу (A - a), различию русских и английских символов в нике (Y - У) и нестрогому соотвествию параметров к нику ( вас = Вася, Василий и т.п) ', 'отыскать <ник>', ['отыскать вася'])
