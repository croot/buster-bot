# -*- coding: utf-8 -*-

import gc

user_src = 0

src_con, src_cl, src_factory = None, None, None


def replace_ru_eng(body):
    body = body.replace(u'a', u'а').replace(u'A', u'А').replace(u'e', u'е').replace(u'E', u'Е').replace(u'T', u'Т').replace(u'O', u'О').replace(u'o', u'о').replace(u'p', u'р').replace(u'P', u'Р').replace(u'H', u'Н').replace(u'k', u'к').replace(u'K', u'К').replace(u'X', u'Х').replace(u'x', u'х').replace(u'C', u'С').replace(u'c', u'с').replace(u'B', u'В').replace(u'M', u'М').replace(u'Y', u'У').replace(u'0', u'О')
    return body

class user_search(object):
    """ user discovery search """
    def __init__(self, type, source, parameters):
        self.r = reactor
        self.source = source
        self.parameters = parameters
        self.type = type
        self.dict = {'allconf':0, 'alluser':0, 'object':str(),'search':0, 'rep':str(), 'con':0, 'see':0, 'res':0, 'err':0}
        self.factory = None
        self.con = None
        self.cl = None
        self.search()

    def src_err_ev(self, x):
        try: el=x.value.getElement()
        except: return
        if hasattr(el, 'firstChildElement') and el.firstChildElement().name == 'conflict':
            print '- search bot conflict'
            self.src_d()


    def hnd_usse_quest(self, jid, key):
        packet = IQ(self.cl, 'get')
        packet.addElement('query', 'http://jabber.org/protocol/disco#items')
        packet.addCallback(self.disco_result_handler, key)
        self.r.callFromThread(packet.send, jid)

    def disco_result_handler(self, key, x):
        if x['type'] == 'result':
            if not self.dict:
                print 'empty'
                return
            #try: print unicode(x.toXml())
            #except: pass
            query = element2dict(x)['query']
            query = [i.attributes for i in query.children if i.__class__==domish.Element]
            r = [i['jid'] for i in query]
            if key=='chat':
                lim = 350
                if x['from'] in ['conference.qip.ru']:
                    lim = 100
                l = []
                for i in query:
                    try: g = re.search('^(.+)\(([0-9]+)\)$', i['name']).groups()
                    except: g = (i['name'], '0')
                    if int(g[1]) < 99: l.append((g[0], i['jid'], g[1]))
                l.sort(lambda x, y: cmp(int(y[2]), int(x[2])))
                l = [i[1] for i in l]
                try: r = l[:lim]
                except: r = l
                #try: print unicode(r[0]),len(r)
                #except: pass
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
        else:
            if key=='user':
                self.dict['err']+=1
        


    def search(self):
        
        parameters = self.parameters
        type = self.type
        source = self.source
        if not parameters or parameters.isspace():
            globals()['user_src'] = 0
            reply(type, source, u'А кого искать будем?')
            return
        if len(parameters)<3:
            globals()['user_src'] = 0
            reply(type, source, u'В запросе должно быть минимум 3 символа!')
            return

        parameters = parameters.lower()
        parameters = replace_ru_eng(parameters)
        s, r, k = 0,0,0

        self.dict['search'] = time.time()
        self.dict['object'] = parameters

        reply(type, source, u'Результат смотри в привате через 3 минуты!')

        if not self.dict['con']:
            threading.Thread(None, self.search_con,'search_con'+str(INFO['thr'])).start()

        tim = time.time()
        while not self.dict['con'] and time.time()-tim<21:
            time.sleep(1)
            pass

        if not self.dict['con']:
            try: self.src_d()
            except: pass
            globals()['user_src'] = 0
            reply(type, source, u'Поиск остановлен из-за неудачной попытки подключения! Попробуйте позже!')
            return
        for x in ['conference.ya.ru','conference.xmpp.ru','conference.jabber.ru','conference.talkonaut.com','conference.qip.ru','conference.jabbrik.ru']:
            self.hnd_usse_quest(x, 'chat')
        time.sleep(150)
        all = u'\nВсего конференций: '+str(self.dict['allconf'])+u'\nВсего юзеров: '+str(self.dict['alluser'])+u'\nКонференций с закрытым списком: '+str(self.dict['err'])
        if not self.dict['rep'] or self.dict['rep'].isspace():
            reply('chat', source, u'Совпадений <'+parameters+u'> нет!\n'+all)
        else:
            reply('chat', source, u'Результатов '+str(self.dict['res'])+':\n'+self.dict['rep'][:2000]+all)
        
        globals()['user_src'] = 0
        self.dict = None
        reactor.callLater(1, self.src_d, None)
        gc.collect()


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
        
        if hasattr(self.factory,'stopTrying'):
            self.factory.stopTrying()
        
        if hasattr(self.factory,'stopFactory'):
            #print 'd3'
            self.factory.stopFactory()
        
        if hasattr(self.con,'disconnect'):
            self.con.disconnect()
            #print 'd1'
        
        self.con = None
        self.cl = None
        self.factory = None
        self.dict = None
        del self
        


    def _ConnectionLost(self, x, reason):
        print '- search bot connection lost'
        #print reason

    def xmlend(self, any):
        print '- search xmlstream end'


    def search_con(self):
        print 'SEARCH_CONNECTION_START'
        myJid = jid.JID(JABBER_ID+'/search')
        self.factory = client.basicClientFactory(myJid, JABBER_PASS)# = clien.bas
        self.factory.addBootstrap('//event/stream/authd', self.src_pass)#self.uss_authd_search_)
        self.factory.addBootstrap(xmlstream.STREAM_CONNECTED_EVENT, self.uss_authd_search_)
        self.factory.addBootstrap('//event/client/basicauth/authfailed', self.src_pass)
        self.factory.addBootstrap('//event/client/basicauth/invaliduser', self.src_pass)
        self.factory.addBootstrap(xmlstream.STREAM_END_EVENT, self.xmlend)
        self.factory.clientConnectionLost = self._ConnectionLost
        self.factory.maxRetries = 0
        self.factory.addBootstrap(xmlstream.STREAM_ERROR_EVENT, self.src_err_ev)
        self.con = self.r.connectTCP(JABBER_ID.split('@')[1], 5222, self.factory)






def hnd_usersearch(t, s, p):
    global user_src
    if time.time()-user_src<180:
        reply(t, s, u'Сейчас я выполняю другой запрос!')
        return
    user_src = time.time()
    user_search(t, s, p)

register_command_handler(hnd_usersearch, 'отыскать', ['все','поиск','юзеры'], 0, 'Поиск юзера онлайн по нику в лучших чатах сети jabber.\nАвтоматически не чувствителен к капсу (A - a), различию русских и английских символов в нике (Y - У) и нестрогому соотвествию параметров к нику ( вас = Вася, Василий и т.п) ', 'отыскать <ник>', ['отыскать вася'])
