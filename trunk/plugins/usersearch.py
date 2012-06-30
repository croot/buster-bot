# -*- coding: utf-8 -*-

USER_SEARCH = {'search':0,'chat':[],'user':[],'con':0, 'see':0}

src_con, src_cl, src_factory = None, None, None

def hnd_usersearch(type, source, parameters):
    global src_cl
    global src_con
    global src_factory
    global USER_SEARCH
    if time.time() - USER_SEARCH['search'] < 180:
        reply(type, source, u'Сейчас я выполняю другой запрос! Время до завершения - '+timeElapsed(180 - (time.time() - USER_SEARCH['search'])))
        return
    if not parameters or parameters.isspace():
        reply(type, source, u'А кого искать будем?')
        return

    parameters = parameters.lower()
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
    for x in ['conference.jabber.ru','conference.talkonaut.com','conference.qip.ru','conference.jabbrik.ru']:
        hnd_usse_quest(x, 'chat')
    time.sleep(7)
    for x in USER_SEARCH['chat']:
        hnd_usse_quest(x, 'user')
    time.sleep(150)
    rep=''
    res=0
    for x in USER_SEARCH['user']:
        chat=x.split('/')[0]
        user=x.split('/')[1]
        l=user.lower()
        if l.count(parameters):
            res+=1
            rep+=chat+' '+user+'\n'
    all = u'\nВсего конференций: '+str(len(USER_SEARCH['chat']))+u'\nВсего юзеров: '+str(len(USER_SEARCH['user']))
    if not rep or rep.isspace():
        reply('chat', source, u'Совпадений нет!\n'+all)
        return
    reply('chat', source, u'Результатов '+str(res)+':\n'+rep[:2000]+all)
    USER_SEARCH['chat']=[]
    USER_SEARCH['user']=[]
    USER_SEARCH['search']=0
    USER_SEARCH['con']=0
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

register_command_handler(hnd_usersearch, 'отыскать', ['все'], 0, 'отыскать', 'отыскать', ['отыскать'])
