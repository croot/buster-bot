# -*- coding: utf-8 -*-

#USER_SEARCH = {'allconf':0, 'alluser':0, 'object':str(),'search':0, 'rep':str(), 'con':0, 'see':0, 'res':0}
user_src = 0
#src_con, src_cl, src_factory = None, None, None

def replace_ru_eng(body):
    body = body.replace(u'a', u'а').replace(u'A', u'А').replace(u'e', u'е').replace(u'E', u'Е').replace(u'T', u'Т').replace(u'O', u'О').replace(u'o', u'о').replace(u'p', u'р').replace(u'P', u'Р').replace(u'H', u'Н').replace(u'k', u'к').replace(u'K', u'К').replace(u'X', u'Х').replace(u'x', u'х').replace(u'C', u'С').replace(u'c', u'с').replace(u'B', u'В').replace(u'M', u'М').replace(u'Y', u'У').replace(u'0', u'О')
    return body

class user_search(object):
    """ user discovery search """
    def __init__(self, type, source, parameters):
        self.source = source
        self.parameters = parameters
        self.type = type
        self.dict = {'allconf':0, 'alluser':0, 'object':str(),'search':0, 'rep':str(), 'con':0, 'see':0, 'res':0}
        self.factory = None
        self.con = None
        self.cl = None
        self.search()

    def src_err_ev(self, x):
        try: el=x.value.getElement()
        except: return
        if hasattr(el, 'firstChildElement') and el.firstChildElement().name == 'conflict':
            print 'search bot conflict'
            self.src_d()


    def hnd_usse_quest(self, jid, key):
        packet = IQ(self.cl, 'get')
        packet.addElement('query', 'http://jabber.org/protocol/disco#items')
        packet.addCallback(self.disco_result_handler, key)
        reactor.callFromThread(packet.send, jid)

    def disco_result_handler(self, key, x):
        if x['type'] == 'result':
            #try: print unicode(x.toXml())
            #except: pass
            query = element2dict(x)['query']
            query = [i.attributes for i in query.children if i.__class__==domish.Element]
            r = [i['jid'] for i in query]
            if key=='chat':
                for x in r:
                    self.hnd_usse_quest(x, 'user')
                    self.dict['allconf'] += 1
            elif key=='user':
                for x in r:
                    self.dict['alluser'] += 1
                    chat=x.split('/')[0]
                    user=x.split('/')[1]
                    user=replace_ru_eng(user)
                    l=user.lower()
                    if l.count(self.dict['object']):
                        self.dict['res'] += 1
                        self.dict['rep'] += chat+'    '+user+'\n'
        #USER_SEARCH[key].extend(r)


    def search(self):
        USER_SEARCH = self.dict
        parameters = self.parameters
        type = self.type
        source = self.source
        if not parameters or parameters.isspace():
            global user_src
            user_src = 0
            reply(type, source, u'А кого искать будем?')
            return
        if len(parameters)<3:
            global user_src
            user_src = 0
            reply(type, source, u'В запросе должно быть минимум 3 символа!')
            return

        parameters = parameters.lower()
        parameters = replace_ru_eng(parameters)
        s, r, k = 0,0,0

        USER_SEARCH['search'] = time.time()
        USER_SEARCH['object'] = parameters

        reply(type, source, u'Результат смотри в привате через 3 минуты!')

        if not USER_SEARCH['con']:
            threading.Thread(None, self.search_con,'search_con'+str(INFO['thr'])).start()

        tim = time.time()
        while not USER_SEARCH['con'] and time.time()-tim<21:
            time.sleep(1)
            pass

        if not USER_SEARCH['con']:
            try: self.src_d()
            except: pass
            reply(type, source, u'Поиск остановлен из-за неудачной попытки подключения! Попробуйте позже!')
            return
        for x in ['conference.ya.ru','conference.xmpp.ru','conference.jabber.ru','conference.talkonaut.com','conference.qip.ru','conference.jabbrik.ru']:
            self.hnd_usse_quest(x, 'chat')
        time.sleep(150)
        all = u'\nВсего конференций: '+str(USER_SEARCH['allconf'])+u'\nВсего юзеров: '+str(USER_SEARCH['alluser'])
        if not USER_SEARCH['rep'] or USER_SEARCH['rep'].isspace():
            reply('chat', source, u'Совпадений <'+parameters+u'> нет!\n'+all)
        else:
            reply('chat', source, u'Результатов '+str(USER_SEARCH['res'])+':\n'+USER_SEARCH['rep'][:2000]+all)
        USER_SEARCH['allconf'] = 0
        USER_SEARCH['alluser'] = 0
        USER_SEARCH['rep'] = str()
        USER_SEARCH['search'] = 0
        USER_SEARCH['con'] = 0
        USER_SEARCH['res'] = 0
        del USER_SEARCH
        self.src_d()


    def src_pass(self, x):
        pass

    def uss_authd_search_(self, xmlstream):
        self.cl = xmlstream
        self.dict['con']=1

    def src_d(self, x = None):
        if hasattr(self.cl, 'transport') and hasattr(self.cl.transport, 'abortConnection'):
            self.cl.transport.abortConnection()
        try: self.con.transport.abortConnection()
        except: pass
        try: self.factory.transport.stopConnecting()
        except: pass
        try: self.cl.transport.stopConnecting()
        except: pass
        if hasattr(self.factory,'stopTrying'):
            self.factory.stopTrying()
        if hasattr(self.con,'disconnect'):
            self.con.disconnect()
        self.con = None
        self.cl = None
        self.factory = None
        self.dict = None
        #self.dict.clear()


    def search_con(self):
        print 'SEARCH_CONNECTION_START'
        myJid = jid.JID(JABBER_ID+'/search')
        self.factory = client.basicClientFactory(myJid, JABBER_PASS)
        self.factory.addBootstrap('//event/stream/authd', self.uss_authd_search_)
        self.factory.addBootstrap('//event/client/basicauth/authfailed', self.src_pass)
        self.factory.addBootstrap('//event/client/basicauth/invaliduser', self.src_pass)
        self.factory.addBootstrap(xmlstream.STREAM_END_EVENT, self.src_d)
        self.factory.addBootstrap(xmlstream.STREAM_ERROR_EVENT, self.src_err_ev)
        self.con = reactor.connectTCP(JABBER_ID.split('@')[1], 5222, self.factory)






def hnd_usersearch(t, s, p):
    global user_src
    if time.time()-user_src<180:
        reply(t, s, u'Сейчас я выполняю другой запрос!')
        return
    user_src = time.time()
    user_search(t, s, p)

register_command_handler(hnd_usersearch, 'отыскать', ['все','поиск','юзеры'], 0, 'Поиск юзера онлайн по нику в лучших чатах сети jabber.\nАвтоматически не чувствителен к капсу (A - a), различию русских и английских символов в нике (Y - У) и нестрогому соотвествию параметров к нику ( вас = Вася, Василий и т.п) ', 'отыскать <ник>', ['отыскать вася'])
