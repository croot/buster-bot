#===istalismanplugin===
# -*- coding: utf-8 -*-

import string

from twisted import names
from twisted.internet import protocol, error
from twisted.words.protocols.jabber import client,jid
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.words.protocols.jabber.client import *

def basicClientFactory(jid, secret):
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

rjid_con, rjid_cl, rjid_factory, regDone, regSource, rjidNP = None, None, None, None, None, None


def connected_rjid(x):
    print '- Regjid connected..'
    xmlstream = x

    def rawDataIn(j):
        print 'con in'
        try: print unicode(j)
        except: pass

    def rawDataOut(j):
        print 'con out'
        try: print unicode(j)
        except: pass

    x.rawDataInFn = rawDataIn
    x.rawDataOutFn = rawDataOut


def rjiduserEvent(xmlstream):
    print 'Invalid user,trying to register!'
    global regDone
    global rjidNP
    if not regDone:
        regDone = True 
        print 'register...'
        global rjid_factory
        rjid_factory.authenticator.registerAccount(rjidNP[0], rjidNP[1])
    else:
        rjid_stop()


def rjid_stop():
    global rjid_cl
    global rjid_con
    global rjid_factory
    global rjidNP
    global regSource
    global regDone
    global RJID_C

    try:
        rjid_con.transport.stopConnecting()
        rjid_factory.transport.stopConnecting()
        rjid_cl.transport.stopConnecting()
    except: pass
    
    if hasattr(rjid_factory,'stopTrying'):
        rjid_factory.stopTrying()
    if hasattr(rjid_con,'disconnect'):
        rjid_con.disconnect()

    del rjid_con
    del rjid_factory
    
    rjid_con = None
    rjid_factory = None
    rjid_cl = None
    rjidNP = None
    regSource = None
    regDone = None
    RJID_C = None

TIMER_LAST_REGJID = 0

def hnd_regjid(t, s, p):
    if not p or not p.count('@') or not p.count('.'):
        reply(t, s, u'Неверный формат jid-a, либо не введены параметры!')
        return
    
    global regSource
    global TIMER_LAST_REGJID
    
    if regSource:
        if time.time() - TIMER_LAST_REGJID>=180:
            rjid_stop()
        else:
            reply(t, s, u'Команда будет доступной через пару минут!')
            return
        
    TIMER_LAST_REGJID = time.time()
    
    passw, login, serv, xid = '', '', '', p
    if not p.count(' '):
        passw = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(6))
        login = xid.split('@')[0]
        serv = xid.split('@')[1]
    else:
        xid = p.split()[0]
        passw = p.split()[1]
        login = xid.split('@')[0]
        serv = xid.split('@')[1]
    reply(t, s, u'Регистрируем JID:\nЛогин : '+login+u'\nСервер : '+serv+u'\nПароль : '+passw)
    global rjidNP
    regSource = t, s
    rjidNP = login, passw
    regjid_con(xid)
    
def rjid_pass(x):
    pass

def authd_rjid(xmlstream):
    global rjid_cl
    rjid_cl = xmlstream
    reply(regSource[0], regSource[1], u'Регистрация успешно выполнена!')
    try: xmlstream.transport.stopConnecting()
    except: pass
    rjid_stop()

fi = None

def rjidfailedEvent(x):
    global fi
    fi=x
    try:
        if x['type'] == 'error':
            code, add = [], ''
            ERROR={'400':u'Плохой запрос','401':u'Не авторизирован','402':u'Требуется оплата','403':u'Запрещено','404':u'Не найдено','405':u'Не разрешено','406':u'Не приемлемый','407':u'Требуется регистация','408':u'Время ожидания ответа вышло','409':u'Конфликт','500':u'Внутренняя ошибка сервера','501':u'Не реализовано','503':u'Сервис недоступен','504':u'Сервер удалил запрос по тайм-ауту'}
            try: code = [c['code'] for c in x.children if (c.name=='error')]
            except: pass
            if ''.join(code) in ERROR: add=ERROR[' '.join(code)]
            reply(regSource[0], regSource[1], u'Регистрация завершилась ошибкой!\n'+' '.join(code)+' '+add)
    except: reply(regSource[0], regSource[1], u'Регистрация завершилась ошибкой!\n')
    rjid_stop()

RJID_C = None

def rjid_coonection_failed(x, reason):
    print "- Regjid connection failed"
    try:
        #print type(x)
        reply(regSource[0], regSource[1], u'Немогу подключится к '+rjid_factory.authenticator.jid.host)
    except: pass
    rjid_stop()

def rjid_dns(x):
    z=None
    global RJID_C
    from twisted.names import client as dns
    dns.lookupService('_xmpp-client._tcp.'+x, timeout = [2,10]).addCallback(rjid_clbc)
    t=time.time()
    while not RJID_C and time.time()-t<4.5:
        time.sleep(1)
        pass
    r = random.choice(RJID_C[0])
    RJID_C = None
    return unicode(r.payload.target), int(r.payload.port)

def rjid_clbc(x):
    global RJID_C
    RJID_C = x


def regjid_con(xid):
    try: a = rjid_dns(xid.split('@')[1])
    except:
        print '- Regjid dns error'
        a = xid.split('@')[1], 5222
    global rjidNP
    myJid = jid.JID(xid+'/jabbim')
    global rjid_factory
    rjid_factory = basicClientFactory(myJid, rjidNP[1])
    rjid_factory.addBootstrap('//event/stream/start', _streamstart)
    rjid_factory.addBootstrap('//event/stream/authd', authd_rjid)
    rjid_factory.addBootstrap(xmlstream.STREAM_CONNECTED_EVENT, connected_rjid)
    rjid_factory.addBootstrap(client.BasicAuthenticator.AUTH_FAILED_EVENT, rjiduserEvent)
    rjid_factory.addBootstrap(client.BasicAuthenticator.REGISTER_FAILED_EVENT, rjidfailedEvent)
    rjid_factory.addBootstrap(xmlstream.STREAM_END_EVENT, rjid_pass)
    rjid_factory.addBootstrap(xmlstream.STREAM_ERROR_EVENT, rjid_pass)
    rjid_factory.clientConnectionFailed = rjid_coonection_failed
    rjid_factory.maxRetries = 0
    global rjid_con
    serv = unicode(a[0])
    port = int(a[1])
    try: print serv, port
    except: pass
    rjid_con = reactor.connectTCP(serv.strip(), port, rjid_factory, timeout=11)


def _streamstart(x):
    x.authenticator.registerAccount(rjidNP[0], rjidNP[1])

    def rawDataIn(j):
        print 'st in'
        try: print unicode(j)
        except: pass

    def rawDataOut(j):
        print 'st out'
        try: print unicode(j)
        except: pass

    x.rawDataInFn = rawDataIn
    x.rawDataOutFn = rawDataOut


register_command_handler(hnd_regjid, 'регжид', ['все'], 0, 'Регистрация jabber-id через бота, для данного типа регистрации сервер должен поддерживать открытую регистрацию.', 'регжид <jid> <pass>', ['регжид vasya@mafiozo.in 1234'])

