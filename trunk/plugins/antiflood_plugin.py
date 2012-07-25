#===istalismanplugin===
# -*- coding: utf-8 -*-

import string
import time

from twisted import names
from twisted.internet import protocol, error
from twisted.words.protocols.jabber import client,jid
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.words.protocols.jabber.client import *

SANT_SP_JID = {}


class Anti_Spam_JID(object):
    """ it's work """

    def __init__(self, jid, password, reactor=reactor, port=5222, resource="ANTISPAM_BOT"):
        self.jid = jid
        self.list = []
	self.password = password
	self.n = 0
	self.servername = jid[jid.find('@')+1:]
	self.port = port
	self.resource = str(random.randrange(100,999))
	self._jid = None
	self._factory = None
	self._reactor = reactor
	self._resource = None
	self._xmlstream = None
	self.tryandregister = 1
	self.connect()

    def connect(self):
        from twisted.names import client as dns
        d = dns.lookupService('_xmpp-client._tcp.'+self.servername, timeout = [2,10])
        d.addCallback(self._dnsLookup)
        d.addErrback(self._dnsLookupErr)

    def _dnsLookup(self, resp):
        r = random.choice(resp[0])
        self._connect(unicode(r.payload.target), int(r.payload.port))

    def _dnsLookupErr(self, resp):
        self._connect(self.servername, self.port)

    def _connect(self, host, port):
        myJid = jid.JID(self.jid+'/'+self.resource)
        self.factory = client.basicClientFactory(myJid, self.password)
        #self.factory.addBootstrap('//event/stream/start',self._streamstart)
        self.factory.addBootstrap('//event/stream/authd',self._authd)
        self.factory.addBootstrap("//event/client/basicauth/invaliduser", self._invaliduser)
        self.factory.addBootstrap("//event/client/basicauth/authfailed", self._authfailed)
        #self.factory.addBootstrap("//event/client/basicauth/registerfailed", self._regfailed)
        #self.factory.addBootstrap('/iq[@type="result"]/bind', self._bind)
        self.factory.clientConnectionLost = self.connectionLost
        self.factory.clientConnectionFailed = self.connectionFailed
        self.connection = reactor.connectTCP(host,port,self.factory)

    def connectionLost(self, connector, reason=protocol.connectionDone):
        pass

    def connectionFailed(self, connector, reason=protocol.connectionDone):
        a = SANT_SP_JID[self.jid]
        reply(a['t'],a['s'],u'Неудачное подключение!')

    def _authd(self, xmlstream):
        if xmlstream:
            SANT_SP_JID[self.jid]['cl'] = xmlstream
            self._presence = domish.Element(('jabber:client', 'presence'))
	    self._presence.addElement('status').addContent('Online')
	    self._presence.addElement('show').addContent('chat')
	    SANT_SP_JID[self.jid]['cl'].send(self._presence)
            SANT_SP_JID[self.jid]['cl'].addObserver('/message', self._gotMessage)
            SANT_SP_JID[self.jid]['cl'].addObserver('/presence', self._gotPresence)
            #SANT_SP_JID[self.jid]['cl'].addObserver('/*', self._any)
            threading.Thread(None,self._start,'start_'+str(INFO['thr'])).start()


    def _start(self):
            self._reactor.callFromThread(self.privacy, None)
            time.sleep(7)
            SANT_SP_JID[self.jid]['cl'].factory.stopTrying()
            self.connection.disconnect()
            a = SANT_SP_JID[self.jid]
            if not a['msg'] and not a['sub']:
                reply(a['t'],a['s'],u'Спамерской активности не зарегестрировано!')
                return
            reply(a['t'],a['s'], u'Получено сообщений '+str(a['msg'])+u', удалено запросов авторизации '+str(a['sub']))
            del SANT_SP_JID[self.jid]


    def _gotMessage(self, el):
        try: mtype=el["type"]
        except: return
        
        if mtype == "error": return
        
        fromjid = el["from"]
        jid = fromjid.split('/')[0]
        if not jid in self.list:
            self.list.append(jid)
            q = domish.Element(('jabber:client', 'iq'))
            q['type'] = 'set'
            q['id'] = str(random.randrange(1,999))
            query = q.addElement('query', 'jabber:iq:roster')
            i = query.addElement('item')
            i['jid'] = jid
            i['subscription'] = 'remove'
            SANT_SP_JID[self.jid]['cl'].send(q)
            if self.jid in SANT_SP_JID.keys():
                if 'sub' in SANT_SP_JID[self.jid]:
                    SANT_SP_JID[self.jid]['sub']+=1
	if self.jid in SANT_SP_JID.keys():
            if 'msg' in SANT_SP_JID[self.jid]:
                SANT_SP_JID[self.jid]['msg']+=1

    def _gotPresence(self, el):
        try: typ = el["type"]
        except: typ = "available"

        fromjid = el["from"]

        if typ in ['subscribe']:
            q = domish.Element(('jabber:client', 'iq'))
            q['type'] = 'set'
            q['id'] = str(random.randrange(1,999))
            query = q.addElement('query', 'jabber:iq:roster')
            i = query.addElement('item')
            i['jid'] = fromjid
            i['subscription'] = 'remove'
            SANT_SP_JID[self.jid]['cl'].send(q)
            if self.jid in SANT_SP_JID.keys():
                if 'sub' in SANT_SP_JID[self.jid]:
                    SANT_SP_JID[self.jid]['sub']+=1

    def sender(self, x):
        SANT_SP_JID[self.jid]['cl'].send(x)


    def privacy(self, a):
        n = 0
        message = domish.Element(('jabber:client','message'))
        message["type"] = 'chat'
        message["to"] = 'some_user@jabbrik.ru'
        message.addElement("body", "jabber:client", '1')
        self._reactor.callFromThread(self.sender, message)
        q = IQ(self._xmlstream, 'set')
        #q['type'] = "set"
        q['id'] = str(random.randrange(1,999))
        query = q.addElement('query', 'jabber:iq:privacy')
        i = query.addElement('list')
        i['name'] = "ignore2"
        for x in [self.jid, 'conference.jabber.ru', 'conference.talkonaut.com', 'conference.qip.ru']:
            n+=1
            one = i.addElement('item')
            one['type'] = "jid"
            one['order'] = str(n)
            one['value'] = x
            one['action'] = "allow"
        lis = i.addElement('item')
        lis['type'] = 'subscription'
        lis['order'] = str(n+1)
        lis['value'] = 'none'
        lis['action'] = 'deny'
        q.addCallback(self._t)
        self._reactor.callFromThread(self.sender, q)
        for x in ['active','default']:
            q = IQ(self._xmlstream, 'set')
            #q['type'] = "set"
            q['id'] = str(random.randrange(1,999))
            query = q.addElement('query', 'jabber:iq:privacy')
            i = query.addElement(x)
            i['name'] = "ignore2"
            self._reactor.callFromThread(self.sender, q)

    def _t(self, x):
        a = SANT_SP_JID[self.jid]
        if x['type']=='error':
            reply(a['t'], a['s'], u'Ошибка при активации списка!')
            return
        if x['result']:
            self.n+=1
            if self.n>3: return
            D={1:u'Список установлен',2:u'Активация',3:u'Установка по умолчанию'}
            reply(a['t'], a['s'], D[self.n])
            
    def _streamEnd(self, el):
        print 'Stream END!'

    def _bind(self, el):
        print el.toXml()
        pass

    def _authfailed(self, el):
        a = SANT_SP_JID[self.jid]
        reply(a['t'],a['s'],u'Неверный логин или пароль!')

    def _invaliduser(self, el):
        a = SANT_SP_JID[self.jid]
        reply(a['t'],a['s'],u'Неверный логин или пароль!')



def hnd_antispam_jid(t, s, p):
    if not p:
        reply(t, s, u'?')
        return
    if not p.count(' '):
        reply(t, s, u'<jid> <password>!')
        return
    ss = p.split()
    jid = ss[0]
    pas = ss[1]
    if not jid.count('@') or not jid.count('.'):
        reply(t, s, u'Это еще что за jid такой?')
        return
    SANT_SP_JID[jid]={'msg':0, 'sub':0, 't':t, 's':s, 'cl':None}
    reply(t, s, u'Минуточку..Для вступления в силу новых настроек вам нужно переподключиться!')
    Anti_Spam_JID(jid, pas)
    


register_command_handler(hnd_antispam_jid, 'антиспамжид', ['все'], 20, 'Защита жида во время спама', 'антиспамжид <jid> <password>', ['антиспамжид admin@vasi.net 1234'])

