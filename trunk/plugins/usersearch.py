# -*- coding: utf-8 -*-

USER_SEARCH = {'allconf':0, 'alluser':0, 'object':str(),'search':0, 'rep':str(), 'con':0, 'see':0, 'res':0}

src_con, src_cl, src_factory = None, None, None

def replace_ru_eng(body):
    body = body.replace(u'a', u'а').replace(u'A', u'А').replace(u'e', u'е').replace(u'E', u'Е').replace(u'T', u'Т').replace(u'O', u'О').replace(u'o', u'о').replace(u'p', u'р').replace(u'P', u'Р').replace(u'H', u'Н').replace(u'k', u'к').replace(u'K', u'К').replace(u'X', u'Х').replace(u'x', u'х').replace(u'C', u'С').replace(u'c', u'с').replace(u'B', u'В').replace(u'M', u'М').replace(u'Y', u'У').replace(u'0', u'О')
    return body


def hnd_usersearch(type, source, parameters):
    global src_cl
    global src_con
    global src_factory
    global USER_SEARCH
    if not parameters or parameters.isspace():
        reply(type, source, u'А кого искать будем?')
        return
    if len(parameters)<3:
        reply(type, source, u'В запросе должно быть минимум 3 символа!')
        return
    tl = time.time() - USER_SEARCH['search']
    if tl < 180:
        reply(type, source, u'Сейчас я выполняю другой запрос! Время до завершения - '+timeElapsed(180 - (time.time() - USER_SEARCH['search'])))
        return

    parameters = parameters.lower()
    parameters = replace_ru_eng(parameters)
    s, r, k = 0,0,0
    
    USER_SEARCH['search'] = time.time()
    USER_SEARCH['object'] = parameters

    reply(type, source, u'Результат смотри в привате через 3 минуты!')
    
    if not USER_SEARCH['con']:
        threading.Thread(None, search_con,'search_con'+str(INFO['thr'])).start()
        
    tim = time.time()
    while not USER_SEARCH['con'] and time.time()-tim<21:
        time.sleep(1)
        pass
    if not USER_SEARCH['con']:
        try: src_d()
        except: pass
        reply(type, source, u'Поиск остановлен из-за неудачной попытки подключения! Попробуйте позже!')
        return
    for x in ['conference.ya.ru','conference.xmpp.ru','conference.jabber.ru','conference.talkonaut.com','conference.qip.ru','conference.jabbrik.ru']:
        hnd_usse_quest(x, 'chat')
    #time.sleep(7)
    #for x in USER_SEARCH['chat']:
    #    hnd_usse_quest(x, 'user')
    time.sleep(150)
    all = u'\nВсего конференций: '+str(USER_SEARCH['allconf'])+u'\nВсего юзеров: '+str(USER_SEARCH['alluser'])
    if not USER_SEARCH['rep'] or USER_SEARCH['rep'].isspace():
        reply('chat', source, u'Совпадений нет!\n'+all)
    else:
        reply('chat', source, u'Результатов '+str(USER_SEARCH['res'])+':\n'+USER_SEARCH['rep'][:2000]+all)
    USER_SEARCH['allconf'] = 0
    USER_SEARCH['alluser'] = 0
    USER_SEARCH['rep'] = str()
    USER_SEARCH['search'] = 0
    USER_SEARCH['con'] = 0
    USER_SEARCH['res'] = 0
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
        if key=='chat':
            for x in r:
                hnd_usse_quest(x, 'user')
                USER_SEARCH['allconf'] += 1
        elif key=='user':
            for x in r:
                USER_SEARCH['alluser'] += 1
                chat=x.split('/')[0]
                user=x.split('/')[1]
                user=replace_ru_eng(user)
                l=user.lower()
                if l.count(USER_SEARCH['object']):
                    USER_SEARCH['res'] += 1
                    USER_SEARCH['rep'] += chat+'    '+user+'\n'
        #USER_SEARCH[key].extend(r)

def uss_authd_search_(xmlstream):
    global src_cl
    src_cl = xmlstream
    USER_SEARCH['con']=1

def src_pass(x):
    pass

def src_err_ev(x):
    try: el=x.value.getElement()
    except: return
    if hasattr(el, 'firstChildElement') and el.firstChildElement().name == 'conflict':
        print 'search bot conflict'
        src_d()

def src_d(x=None):
    global src_cl
    global src_con
    global src_factory
    if hasattr(src_cl, 'factory'):
        if hasattr(src_cl.factory, 'stopTrying'):
            src_cl.factory.stopTrying()
        if hasattr(src_cl.factory, 'doStop'): src_cl.factory.doStop()
    if hasattr(src_con, 'factory'):
        if hasattr(src_con.factory, 'stopTrying'):
            src_con.factory.stopTrying()
        if hasattr(src_con.factory, 'doStop'): src_con.factory.doStop()
    if hasattr(src_factory, 'stopTrying'): src_factory.stopTrying()
    if hasattr(src_factory, 'doStop'): src_factory.doStop()
    if hasattr(src_con, 'disconnect'): src_con.disconnect()
    src_con = None
    src_factory = None
    src_cl = None

def search_con():
    print 'SEARCH_CONNECTION_START'
    myJid = jid.JID(JABBER_ID+'/search')#+str(random.randrange(111,9999)))
    global src_factory
    src_factory = client.basicClientFactory(myJid, JABBER_PASS)
    src_factory.addBootstrap('//event/stream/authd', uss_authd_search_)
    src_factory.addBootstrap('//event/client/basicauth/authfailed', src_pass)
    src_factory.addBootstrap('//event/client/basicauth/invaliduser', src_pass)
    src_factory.addBootstrap(xmlstream.STREAM_END_EVENT, src_d)
    src_factory.addBootstrap(xmlstream.STREAM_ERROR_EVENT, src_err_ev)
    global src_con
    src_con = reactor.connectTCP(JABBER_ID.split('@')[1], 5222, src_factory)

register_command_handler(hnd_usersearch, 'отыскать', ['все','поиск','юзеры'], 0, 'Поиск юзера онлайн по нику в лучших чатах сети jabber.\nАвтоматически не чувствителен к капсу (A - a), различию русских и английских символов в нике (Y - У) и нестрогому соотвествию параметров к нику ( вас = Вася, Василий и т.п) ', 'отыскать <ник>', ['отыскать вася'])
