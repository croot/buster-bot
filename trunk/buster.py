# -*- coding: utf-8 -*-

import os
import sys
os.chdir(os.path.dirname(sys.argv[0]))

try: import zope.interface
except:
        print "Start Installed Zope.Interface.."
        for x in ['build','install']:
                cmd, pipe = os.getcwd()+'/zope.interface/setup.py '+x, None
                if os.name=='posix':
                        pipe = os.popen('sh -c "%s" 2>&1' % (cmd))
                        return_value = pipe.read()
                elif os.name=='nt':
                        pipe = os.popen('%s' % (cmd))
                        return_value = pipe.read()
                pipe.close
        print "Done!"

        

try:
        from twisted.words.protocols.jabber import client, jid, xmlstream
        from twisted.words.protocols.jabber.client import IQ
        from twisted.words.xish import domish, xmlstream
        from twisted.internet.defer import Deferred
        from tlib import oscar
        from twisted.internet import protocol, reactor
        try: from twisted.internet import ssl
        except: print 'If you want use SSl connection, you may install OpenSSL\n'
except Exception, err: raise

import time
import random
import base64
import chardet
import threading
import types
import traceback

GENERAL_CONFIG_FILE = 'config.list'

def set_exit_handler(func):
        if os.name == "nt":
                try:
                        import win32api
                        win32api.SetConsoleCtrlHandler(func, True)
                except ImportError:
                        pass
        else: pass
                #import signal
                #signal.signal(signal.SIGTERM, func)

def GENERAL_CONFIG(name):
        answ = ''
        try:
                fp = open(GENERAL_CONFIG_FILE, 'r')
                txt = fp.read()
                fp.close()
                k = txt.splitlines()
        except:
                print u'Error in config.list file!!!\n'
                time.sleep(1)
                return
        for x in k:
                if x and x[0]=='#':
                        continue
                sp = x.split(u'=')
                s = sp[0]
                s = s.strip()
                if s==name:
                        answ=sp[1].strip()
                        if answ.count('#'):
                                answ=answ.split('#')[0].strip()
                        if name in [u'ADMINS']:
                                return answ.split(',')
                        else:
                                return answ
        return answ

JABBER_ID = GENERAL_CONFIG("JABBER_ID")
ADMINS = GENERAL_CONFIG("ADMINS")
JABBER_PASS = GENERAL_CONFIG("JABBER_PASS")
UIN = GENERAL_CONFIG("UIN")
ICQ_PASS = GENERAL_CONFIG("ICQ_PASS")
DEFAULT_NICK = GENERAL_CONFIG("DEFAULT_NICK")
ADMIN_PASSWORD = GENERAL_CONFIG("ADMIN_PASSWORD")
ENABLE_ICQ = GENERAL_CONFIG("ENABLE_ICQ")
J2J = GENERAL_CONFIG("J2J")
PUBLIC_LOG_DIR = GENERAL_CONFIG("PUBLIC_LOG_DIR")
PRIVATE_LOG_DIR = GENERAL_CONFIG("PRIVATE_LOG_DIR")
USE_SSL = GENERAL_CONFIG("USE_SSL")

NS_DELAY = 'urn:xmpp:delay'
NS_JABBER_DELAY = 'jabber:x:delay'

CLIENTS = {}

GLOBACCESS = {}
ACCBYCONF = {}
ACCBYCONFFILE = {}
BOT_NICK = {}
COMMOFF = {}
JOIN_CALLBACK = {}
COMMOFF = {}

JOIN_HANDLERS = []
MESSAGE_HANDLERS = []
OUTGOING_MESSAGE_HANDLERS = []
OFFLINE_HANDLERS = []
PRESENCE_HANDLERS = []
LEAVE_HANDLERS = []
STAGE0_INIT =[]
STAGE1_INIT =[]
IQ_HANDLERS = []
COMMAND_HANDLERS = {}
COMMANDS = {}
GROUPCHATS = {}
JOIN_TIMER = {}

ROLES={'none':0, 'visitor':0, 'participant':10, 'moderator':15}
AFFILIATIONS={'none':0, 'member':1, 'admin':5, 'owner':15}

def call_message_handlers(raw, type, source, body):
        global MESSAGE_HANDLERS
	for handler in MESSAGE_HANDLERS:
                inmsg_hnd = handler
		try:
                        INFO['thr'] += 1
                        st_time = time.strftime('%H.%M.%S',time.localtime(time.time()))
			thr_name = 'inmsg%d.%s.%s' % (INFO['thr'],inmsg_hnd.func_name,st_time)
			thr = threading.Thread(None,inmsg_hnd,thr_name,(raw, type, source, body,))
			thr.start()
                except:
                        raise

def call_offline_handlers(jid):
	for handler in OFFLINE_HANDLERS:
                off_hnd = handler
                try:
                        INFO['thr'] += 1
                        st_time = time.strftime('%H.%M.%S',time.localtime(time.time()))
			thr_name = 'off%d.%s.%s' % (INFO['thr'],off_hnd.func_name,st_time)
			thr = threading.Thread(None,off_hnd,thr_name,(jid,))
			thr.start()
		except:
                        pass

def call_join_handlers(groupchat, nick, afl, role, cljid):
	for handler in JOIN_HANDLERS:
                join_hnd = handler
                try:
                        INFO['thr'] += 1
                        st_time = time.strftime('%H.%M.%S',time.localtime(time.time()))
			thr_name = 'join%d.%s.%s' % (INFO['thr'],join_hnd.func_name,st_time)
			thr = threading.Thread(None,join_hnd,thr_name,(groupchat, nick, afl, role, cljid))
			thr.start()
		except:
                        pass

def call_iq_handlers(iq, cljid):
	for handler in IQ_HANDLERS:
                iq_hnd = handler
                INFO['thr'] += 1
                try:
                        st_time = time.strftime('%H.%M.%S',time.localtime(time.time()))
			thr_name = 'iq%d.%s.%s' % (INFO['thr'],iq_hnd.func_name,st_time)
			thr = threading.Thread(None,iq_hnd,thr_name,(iq, cljid))
			thr.start()
		except:
                        pass
                
def call_presence_handlers(prs, cljid):
	for handler in PRESENCE_HANDLERS:
                prs_hnd = handler
                try:
                        st_time = time.strftime('%H.%M.%S',time.localtime(time.time()))
			thr_name = 'prs%d.%s.%s' % (INFO['thr'],prs_hnd.func_name,st_time)
			thr = threading.Thread(None,prs_hnd,thr_name,(prs, cljid))
			thr.start()
		except:
                        pass

def call_leave_handlers(groupchat, nick, reason, code, cljid):
        for handler in LEAVE_HANDLERS:
                try:
                        INFO['thr'] += 1
                        threading.Thread(None,handler,'leave'+str(INFO['thr']),(groupchat, nick, reason, code, cljid)).start()
                except:
                        pass

def call_outgoing_message_handlers(target, body, obody):
        for handler in OUTGOING_MESSAGE_HANDLERS:
                omsg_hnd = handler
                try:
                        INFO['thr'] += 1
                        st_time = time.strftime('%H.%M.%S',time.localtime(time.time()))
			thr_name = 'outmsg%d.%s.%s' % (INFO['thr'],omsg_hnd.func_name,st_time)
			thr = threading.Thread(None,omsg_hnd,thr_name,(target, body, obody,))
			thr.start()
		except:
                        pass

COMMANDS_LIMIT = {}


def call_command_handlers(command, type, source, parameters):
        if COMMAND_HANDLERS.has_key(command):
                real_access = COMMANDS[command]['access']
                if has_access(source, real_access, source[1]):
                        cmd_hnd = COMMAND_HANDLERS[command]
                        try:
                                jid=get_true_jid(source)
                                if not jid in COMMANDS_LIMIT:
                                        COMMANDS_LIMIT[jid]={'time':time.time(),'cmd':command,'n':1,'ignore':0,'p':parameters}
                                else:
                                        if time.time() - COMMANDS_LIMIT[jid]['ignore']<300:
                                                return
                                        if COMMANDS_LIMIT[jid]['cmd']==command and COMMANDS_LIMIT[jid]['p']==parameters and time.time()-COMMANDS_LIMIT[jid]['time']<30:
                                                if COMMANDS_LIMIT[jid]['n']>3:
                                                        reply(type, source, u'Вы превысили лимит запроса одинаковых команд!Игнор на 5 минут!')
                                                        COMMANDS_LIMIT[jid]['ignore']=time.time()
                                                        return
                                                else:
                                                        COMMANDS_LIMIT[jid]['n']+=1
                                                        COMMANDS_LIMIT[jid]['time']=time.time()
                                        else:
                                                COMMANDS_LIMIT[jid]['cmd']=command
                                                COMMANDS_LIMIT[jid]['time']=time.time()
                                                COMMANDS_LIMIT[jid]['n']=1
                                                COMMANDS_LIMIT[jid]['p']=parameters
                        except: pass
                        try:
                                st_time = time.strftime('%H.%M.%S',time.localtime(time.time()))
                                thr_name = u'command%d.%s.%s' % (INFO['thr'],cmd_hnd.func_name,st_time)
                                thr = threading.Thread(None,try_cmd,thr_name,(cmd_hnd, type, source, parameters,))
                                thr.start()
                                #cmd_hnd(type, source, parameters)
                        except:
                                reply(type, source, u'Ошибка при выполнеении команды!\nСообщите об этом админам бота!')
                                INFO['tlasterr']['t']=time.time()
                                INFO['tlasterr']['err']=traceback.format_exc()
                else:
                        if not isinstance(real_access, basestring):
                                real_access = str(real_access)
                        reply(type, source, u'Необходимый доступ для данной команды '+real_access)

def try_cmd(cmd_hnd, type, source, parameters):
        try: cmd_hnd(type, source, parameters)
        except:
                reply(type, source, u'Ошибка при выполнеении команды!(wtf)')
                INFO['tlasterr']['t']=time.time()
                INFO['tlasterr']['err']=traceback.format_exc()
                

def register_message_handler(instance):
	MESSAGE_HANDLERS.append(instance)
def register_outgoing_message_handler(instance):
	OUTGOING_MESSAGE_HANDLERS.append(instance)
def register_join_handler(instance):
	JOIN_HANDLERS.append(instance)
def register_leave_handler(instance):
	LEAVE_HANDLERS.append(instance)
def register_iq_handler(instance):
	IQ_HANDLERS.append(instance)
def register_presence_handler(instance):
	PRESENCE_HANDLERS.append(instance)
def register_stage0_init(instance):
	STAGE0_INIT.append(instance)
def register_stage1_init(instance):
	STAGE1_INIT.append(instance)
def register_offline_handler(instance):
	OFFLINE_HANDLERS.append(instance)

def register_command_handler(instance, command, category=[], access=0, desc='', syntax='', examples=[]):
	command = command.decode('utf-8')
	COMMAND_HANDLERS[command] = instance
	COMMANDS[command] = {'category': category, 'access': access, 'desc': desc, 'syntax': syntax, 'examples': examples}

def initialize_file(filename, data=''):
	if not os.access(filename, os.F_OK):
		fp = file(filename, 'w')
		if data:
			fp.write(data)
		fp.close()


def check_file(gch='',file=''):
	pth,pthf='',''
	if not isinstance(gch, basestring) or not isinstance(file, basestring):
                return 0
	if gch:
		pthf='dynamic/'+gch+'/'+file
		pth='dynamic/'+gch
	else:
		pthf='dynamic/'+file
		pth='dynamic'
	if os.path.exists(pthf):
		return 1
	else:
		try:
			if not os.path.exists(pth):
				os.mkdir(pth,0755)
			if os.access(pthf, os.F_OK):
				fp = file(pthf, 'w')
			else:
				fp = open(pthf, 'w')
			fp.write('{}')
			fp.close()
			return 1
		except:
			return 0
		
def get_true_jid(jid):
	true_jid = ''
	
	if type(jid) is types.ListType:
		jid = jid[0]
	if type(jid) is types.InstanceType:
		jid = unicode(jid)
	stripped_jid = jid.split('/', 1)[0]
	resource = ''
	if len(jid.split('/', 1)) == 2:
		resource = jid.split('/', 1)[1]
	if GROUPCHATS.has_key(stripped_jid):
		if GROUPCHATS[stripped_jid].has_key(resource):
			true_jid = unicode(GROUPCHATS[stripped_jid][resource]['jid']).split('/', 1)[0]
			
			if GROUPCHATS.has_key(true_jid):
				return unicode(GROUPCHATS[stripped_jid][resource]['jid'])
		else:
			true_jid = stripped_jid
	else:
		true_jid = stripped_jid
	return true_jid

def user_level(source, gch):
	global ACCBYCONF
	global GLOBACCESS
	global ACCBYCONFFILE
	jid = get_true_jid(source)
	if jid in ADMINS:
                return 100
	if GLOBACCESS.has_key(jid):
		return GLOBACCESS[jid]
	if ACCBYCONFFILE.has_key(gch):
		if ACCBYCONFFILE[gch].has_key(jid):
			return ACCBYCONFFILE[gch][jid]
	if ACCBYCONF.has_key(gch):
		if ACCBYCONF[gch].has_key(jid):
			return ACCBYCONF[gch][jid]
	return 0

def has_access(source, level, gch):
	jid = get_true_jid(source)
	if user_level(jid,gch) >= int(level):
		return 1
	return 0

MAFIA_BOT = u'mafia_bot@jabber.cz'

host = ("login.icq.com", 5238)
icqMode = 1

JAB, ICQ = None, None

WIN_COD = {}

INFO = {'tlasterr':{'t':0,'err':''},'tin':0,'tout':0,'start':0, 'imsg':0, 'jmsg':0, 'auth':0, 'err':0, 'thr':0, 'cmd':0, 'out':0}

class err:
        def write(self, text):
                print 'ERROR REGISTER!'
                if text.isspace():
                        return
                err_write(text)
                INFO['err']+=1
                if time.time()-INFO['tlasterr']['t']>120:
                        list=[x for x in GLOBACCESS.keys() if GLOBACCESS[x]==100]
                        for x in list:
                                if CLIENTS:
                                        i=random.choice(CLIENTS.keys())
                                        msg(i, x, u'Ошибочка где-то произошла! \nСмотри err.html или юзай wtf!')
                        INFO['tlasterr']['t']=time.time()
                        INFO['tlasterr']['err']=text

def get_bot_nick(chat):
        nick=DEFAULT_NICK
        if chat in BOT_NICK.keys():
                nick=BOT_NICK[chat]
        if isinstance(nick, basestring): return nick
        else: return DEFAULT_NICK

def err_write(text):
        try: hnd_err_add(text)
        except: pass

def hnd_err_add(text):
  (year, month, day, hour, minute, second, weekday, yearday, daylightsavings) = time.localtime()
  tm=str(hour)+':'+str(minute)+':'+str(second)
  data=str(year)+':'+str(month)+':'+str(day)
  fName='err.html'
  try: open(fName)
  except:
    open(fName,'w').write("""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xml:lang="ru-RU" lang="ru-RU" xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="content-type" />
        <title>error log</title>
    </head>
    <body>
""")
  open(fName,'a').write(("%s [%s]:<br />%s<br />"%(data,tm,text)))

sys.stderr = err()

def timeElapsed(time):
	minutes, seconds = divmod(time, 60)
	hours, minutes = divmod(minutes, 60)
	days, hours = divmod(hours, 24)
	months, days = divmod(days, 30.44)
	year, months = divmod(months, 12)
	rep = u'%d сек' % (round(seconds))
	if time>=60: rep = u'%d мин %s' % (minutes, rep)
	if time>=3600: rep = u'%d час %s' % (hours, rep)
	if time>=86400: rep = u'%d дн %s' % (days, rep)
	if time>=2629743: rep = u'%d мес %s' % (months, rep)
	if time>=31556926: rep = u'%d лет %s' % (year, rep)
	return rep

ICQ_LAST = 0

def icq_restart():
        global ICQ
        global ICQ_LAST
        try: ICQ.disconnect()
        except: pass
        ICQ = None
        protocol.ClientCreator(reactor, BotAuth, UIN, ICQ_PASS, icq=icqMode).connectTCP(*host)
        ICQ_LAST = 0
        

class Bot(oscar.BOSConnection):
 
    capabilities = [oscar.CAP_CHAT]

    def connectionFailed(self):
        print '- ICQ bot connection Failed!\n'
        global ICQ_LAST
        if ICQ_LAST: return
        ICQ_LAST = 1
        reactor.callLater(60, icq_restart)
 
    def initDone(self):
        print "- Connect ",UIN," to server", host[0], host[1]
        
        self.requestSelfInfo().addCallback(self.gotSelfInfo)
        self.requestSSI().addCallback(self.gotBuddyList)
        self.setICQStatus("chat")

        global ICQ
        ICQ = self

    def gotAuthorizationRequest(self, uin):
        print u'\n- Authorize quest:',uin
        self.sendAuthorizationResponse(uin, 1, "ok")
        INFO['auth']+=1

 
    def connectionLost(self, reason):
        print '- ICQ bot connection lost!\n'
        if ICQ_LAST: return
        ICQ_LAST = 1
        reactor.callLater(60, icq_restart)
        #protocol.ClientCreator(reactor, BotAuth, UIN, ICQ_PASS, icq=icqMode).connectTCP(*host)


    def offlineBuddy(self, user):
        call_offline_handlers(user.name)
        print '- offline', user.name
 
    def gotSelfInfo(self, user):
        self.name = user.name
 
 
    def gotBuddyList(self, l):
        self.activateSSI()
        self.setProfile("""ICQBot""")
        self.setIdleTime(0)
        self.clientReady()
 
    def gotAway(self, away, user):
        if away:
            try:
                print "User ", user,": ",away
            except:
                pass
 
    def receiveMessage(self, user, multiparts, flags):
        global WIN_COD

        try: INFO['tin']+=sys.getsizeof(multiparts)
        except: pass
        
        INFO['imsg']+=1

        enc=''

        try:
                enc=chardet.detect(multiparts[0][0])['encoding']
                #print enc
                #print multiparts[0][1]
        except:
                pass
        
        print "\n< From: ", user.name
        body=''
        if multiparts[0][1] in ['unicode']:
                try:
                        body = multiparts[0][0].decode('utf-16-be')
                except:
                        pass
        elif multiparts[0][1] in ['custom']:
                try:
                        body = multiparts[0][0].decode('windows-1251','ignore')
                except:
                        pass
        
        else:
                try:
                        body = multiparts[0][0].decode(enc,'ignore')
                except Exception:
                        return
        body=body.strip()
        call_message_handlers(None, 'icq', [user.name, '', '',CLIENTS.keys()[0]], body)
        cmd=body.lower()
        parameters=''
        if body.count(' '):
                s=body.split()
                cmd=s[0].lower()
                parameters=' '.join(s[1:])
        if cmd in COMMANDS:
                call_command_handlers(cmd, 'icq', [user.name, user.name, '', CLIENTS.keys()[0]], unicode(parameters))
        #if body in [u'тест']:
        #    self.sendMessage(user.name, u'пассед'.encode('cp1251','replace'))
        #    return
        if len(JOIN_TIMER)>0:
                for x in JOIN_TIMER.keys():
                        if time.time()-JOIN_TIMER[x]['time']>70:
                                join(x, JOIN_TIMER[x]['nick'])
                                del JOIN_TIMER[x]

                
        def test_s(self, b):
                print '_cbGetInfo'
 
class BotAuth(oscar.OscarAuthenticator):
    print 'Start...\n'
    BOSClass = Bot


TIMER_500 = {'t':0,'clc':0}
TIMER_403 = 0


class JabberBot(object):
	"""Basic jabber bot"""
	
	def __init__(self, jid, password, reactor=reactor, port=5222, resource="JabberBot"):
		global INFO
		INFO['start'] = time.time()
		self.jabberid = jid
		self.password = password
		self.restart = 1
		self.servername = jid[jid.find('@')+1:]
		self.port = port
		self.resource = resource#str(random.randrange(100,999))
		
		# internal values
		self._jid = None
		self._factory = None
		self._reactor = reactor
		self._resource = None
		self._xmlstream = None
		self.tryandregister = 1
		self.__initFactory()

	
	def run(self):
		self.__initFactory()
	
	def __repr__(self):
		return "<%s (%s)>" % (type(self).__name__, self.jabberid)
	
	def __initFactory(self):
                self._conn = None
		self._jid = jid.JID("%s/%s" % (self.jabberid, self.resource))
		self._factory = client.basicClientFactory(self._jid, self.password)
		
		self._factory.addBootstrap('//event/stream/authd', self._authd)
		self._factory.addBootstrap('//event/client/basicauth/authfailed', self.failed)
		self._factory.addBootstrap('//event/client/basicauth/invaliduser', self.failed)
		self._factory.addBootstrap(xmlstream.STREAM_END_EVENT, self.Disconnected)
		self._factory.addBootstrap(xmlstream.STREAM_ERROR_EVENT, self._streamError)
		self._factory.clientConnectionFailed = self._ConnectionFailed
		#self._factory.clientConnectionLost = self._ConnectionLost
		if USE_SSL in [1,'1']:
                        print 'Use SSL\n'
                        try: self._conn = self._reactor.connectSSL(JABBER_ID.split('@')[1],443,self._factory,ssl.ClientContextFactory())
                        except: print u'For use SSL you may download pyOpenSSL http://pypi.python.org/pypi/pyOpenSSL'
                else:
                        self._conn = self._reactor.connectTCP(self.servername, self.port, self._factory)
		if not reactor.running:
                        if ENABLE_ICQ in [1,'1']:
                                protocol.ClientCreator(reactor, BotAuth, UIN, ICQ_PASS, icq=icqMode).connectTCP(*host)
                        self._reactor.run()

        def _connoff(self):
                if self.restart:
                        a, b = self.jabberid, self.password
                        if hasattr(self._factory, 'stopTrying'):
                                self._factory.stopTrying()
                        if hasattr(self._conn, 'disconnect'):
                                self._conn.disconnect()
                        self._factory = None
                        self._conn = None
                        threading.Thread(None,JabberBot,'JabberBotInit'+str(INFO['thr']),(a, b,)).start()


	def _ConnectionFailed(self, x, reason):
                print 'Connection Failed!'
                reactor.callLater(60, self._connoff)

        def _ConnectionLost(self,x, reason):
                print 'Connection Lost!'
                try: err_write(self.jabberid+' Connection Lost!')
                except: pass
                reactor.callLater(60, self._connoff)


	def _streamError(self, xs):
                print 'Xmpp Stream Error'
                err_write('STREAM_ERROR_EVENT')
                try: err_write(unicode(xs))
                except: pass
                try: el=xs.value.getElement()
                except: return
                if el.firstChildElement().name == 'conflict':
                        self.restart = 0
                        print 'XMPP Conflict'
                        if hasattr(self._factory, 'stopTrying'):
                                self._factory.stopTrying()
                        if hasattr(self._conn, 'disconnect'):
                                self._conn.disconnect()
                        self._factory = None
                        self._conn = None

	def Disconnected(self, x):
                print 'XMPP Disconnected'
                err_write(self.jabberid+' STREAM_END_EVENT')
                try: err_write(unicode(x))
                except: pass
                reactor.callLater(60, self._connoff)

	
	def _authd(self, xmlstream):
		if xmlstream:
			self._xmlstream = xmlstream
			
			# set it as online
			self._presence = domish.Element(('jabber:client', 'presence'))
			self._presence.addElement('status').addContent('Online')
			self._presence.addElement('show').addContent('chat')
			self._xmlstream.send(self._presence)

			self.__initOnline()
			try: print 'Xmpp User ',unicode(self.jabberid),'Success Connected!' 
			except: pass
			

			global CLIENTS
			CLIENTS[self.jabberid] = self._xmlstream
			#JAB = self._xmlstream

			threading.Thread(None, stage0, 'stage0_thread'+str(INFO['thr']),(self.jabberid,)).start()

			threading.Thread(None,load_rooms,'load_rooms'+str(INFO['thr']),(self.jabberid,)).start()


	def IqHnd(self, el):
                try: INFO['tin']+=sys.getsizeof(el)
                except: pass
                
                #print el.toXml()
                xmlns = ''
                typ = el.getAttribute('type')

                for query in el.elements(): xmlns = query.uri

		action = el["type"]
		
		if (xmlns == 'jabber:iq:version') and (typ == 'get'):
                        answer = domish.Element(('jabber:client', 'iq'))
                        answer['type'] = 'result'
                        answer['id'] = el.getAttribute('id')
                        answer['to'] = el.getAttribute('from')
                        query = answer.addElement('query', 'jabber:iq:version')
                        query.addElement('name').addContent(u'Buster')
                        query.addElement('version').addContent(u'v.1.0')
                        osver,pyver='',''
                        if os.name=='nt':
                                osname=os.popen("ver")
				osver=osname.read().strip().decode('cp866')+'\n'
				osname.close()
			else:
                                osname=os.popen("uname -sr", 'r')
				osver=osname.read().strip()+'\n'
				osname.close()
				pyver = sys.version
                        query.addElement('os').addContent(osver+' '+pyver)
                        self._xmlstream.send(answer)
                if (xmlns == 'urn:xmpp:ping') and (typ == 'get'):
                        answer = domish.Element(('jabber:client', 'iq'))
                        answer['type'] = 'result'
                        answer['id'] = el.getAttribute('id')
                        answer['to'] = el.getAttribute('from')
                        self._xmlstream.send(answer)
		
		call_iq_handlers(el, self.jabberid)
	
	def __initOnline(self):
		self._xmlstream.addObserver('/message', self._gotMessage)
		self._xmlstream.addObserver('/presence', self.Presence)
		self._xmlstream.addObserver('/iq', self.IqHnd)

	def failed(self, x):
                print 'Connect failed! invalid username/password?'
                self.restart = 0
                reactor.callLater(2, self._connoff)

	def Presence(self, x):
                try: typ = x['type']
                except: typ = 'available'
                try: INFO['tin']+=sys.getsizeof(x)
                except: pass
                
                jid = x['from'].split('/')
                groupchat = jid[0]
                
                nick = x['from'][len(groupchat)+1:]
                
                SUB = {'subscribe':'subscribed','unsubscribe':'unsubscribed'}
                if typ in SUB:
                    p = domish.Element(('jabber:client', 'presence'))
                    p['type'] = SUB[typ]
                    p['to'] = x['from']
                    self._xmlstream.send(p)
                reason = ''
                if typ == 'available':
                        try:
                                _x = [i for i in x.children if (i.name=='x') and (i.uri=='http://jabber.org/protocol/muc#user')][0]
                                _item = [i for i in _x.children if i.name=='item'][0]
                                afl = _item['affiliation']
                                role = _item['role']
                                try: realjid = _item['jid']
                                except: realjid = x['from']
                                if groupchat in GROUPCHATS:
                                        if groupchat in JOIN_CALLBACK and nick==get_bot_nick(groupchat):
                                                msg(self.jabberid, JOIN_CALLBACK[groupchat], u'Зашел с ником '+get_bot_nick(groupchat))
                                                del JOIN_CALLBACK[groupchat]
                                        if nick in GROUPCHATS[groupchat] and GROUPCHATS[groupchat][nick]['jid']==realjid and GROUPCHATS[groupchat][nick]['ishere']==1:
                                                pass
                                        else:
                                                GROUPCHATS[groupchat][nick] = {'jid': realjid, 'idle': time.time(), 'joined': time.time(), 'ishere': 1, 'status': '', 'stmsg': ''}
                                                if role=='moderator' or user_level(realjid,groupchat)>=15:
                                                        GROUPCHATS[groupchat][nick]['ismoder'] = 1
                                                else:
                                                        GROUPCHATS[groupchat][nick]['ismoder'] = 0
                                                call_join_handlers(groupchat, nick, afl, role, self.jabberid)
                        except: pass
                        
                if typ == 'unavailable':
                        try:
                                if groupchat == JABBER_ID: return
                                
                                _x = [i for i in x.children if (i.name=='x') and (i.uri == 'http://jabber.org/protocol/muc#user')][0]
                                _item = [i for i in _x.children if i.name=='item'][0]

                                try: reason = [i for i in _item.children if i.name=='reason'][0].children[0]
                                except: pass
                                
                                _status = [i['code'] for i in _x.children if i.name=='status']
                                if groupchat in GROUPCHATS:
                                        if '301' in _status and nick==get_bot_nick(groupchat):
                                                to_admin(u'Бота забанили в '+groupchat)
                                        if '307' in _status and nick==get_bot_nick(groupchat):
                                                to_admin(u'Бота кикнули в '+groupchat)
                                        if '303' in _status:
                                                try: newnick = _item['nick']
                                                except: newnick = '[unknown nick]'
                                                GROUPCHATS[groupchat][newnick] = {'jid': jid, 'idle': time.time(), 'joined': GROUPCHATS[groupchat][nick]['joined'], 'ishere': 1}
                                                for x in ['idle','status','stmsg']:
                                                        try:
                                                                del GROUPCHATS[groupchat][nick][x]
                                                                if GROUPCHATS[groupchat][nick]['ishere']==1:
                                                                        GROUPCHATS[groupchat][nick]['ishere']=0
                                                        except:
                                                                pass
                                        else:
                                                for x in ['idle','status','stmsg','joined']:
                                                        try:
                                                                del GROUPCHATS[groupchat][nick][x]
                                                                if GROUPCHATS[groupchat][nick]['ishere']==1:
                                                                        GROUPCHATS[groupchat][nick]['ishere']=0
                                                        except:
                                                                pass
                                        call_leave_handlers(groupchat, nick, reason, ' '.join(_status), self.jabberid)
                                else:
                                        call_offline_handlers(gropchat)
                                        
                        except: pass
                        
                if typ == 'error' and groupchat in GROUPCHATS:
                        try:
                                add=''
                                list = [i['code'] for i in x.children if (i.name=='error')]
                                ERROR={'400':u'Плохой запрос','401':u'Не авторизирован','402':u'Требуется оплата','403':u'Запрещено','404':u'Не найдено','405':u'Не разрешено','406':u'Не приемлемый','407':u'Требуется регистация','408':u'Время ожидания ответа вышло','409':u'Конфликт','500':u'Внутренняя ошибка сервера','501':u'Не реализовано','503':u'Сервис недоступен','504':u'Сервер удалил запрос по тайм-ауту'}
                                if ''.join(list) in ERROR:
                                        add=ERROR[''.join(list)]
                                if groupchat in JOIN_CALLBACK and nick==get_bot_nick(groupchat):
                                        try: msg(self.jabberid, JOIN_CALLBACK[groupchat], u'Не смог зайти в '+groupchat+u', Код ошибки: '+' '.join(list)+' '+add)
                                        except: msg(JOIN_CALLBACK[groupchat], u'Не смог зайти в '+groupchat)
                                        del JOIN_CALLBACK[groupchat]
                                if '409' in list:
                                        join(groupchat, nick+'_', self.jabberid)
                                if '404' in list or '503' in list:
                                        global JOIN_TIMER
                                        JOIN_TIMER[groupchat]={'time':time.time(),'nick':nick}
                                if ' '.join(list) in ['401','403','405']:
                                        print 'GROUPCHATS clean'
                                        del GROUPCHATS[groupchat]
                        except: print '- Some exception in Presence (typ err)'
                        
                if len(JOIN_TIMER)>0:
                        for x in JOIN_TIMER.keys():
                                if time.time()-JOIN_TIMER[x]['time']>70:
                                        join(x, JOIN_TIMER[x]['nick'], self.jabberid)
                                        del JOIN_TIMER[x]
                call_presence_handlers(x, self.jabberid)
                
     
	
	def _gotMessage(self, el):
                INFO['jmsg']+=1
                
                try: INFO['tin']+=sys.getsizeof(el)
                except: pass
                try: mtype=el["type"]
                except: return

                fromjid = el["from"]
		jid = fromjid.split('/')[0]
		res, body, ns = '', '', ''
                
                if mtype == "error":
                        print '- XMPP Message error-in'
                        try: list = [i['code'] for i in el.children if (i.name=='error')]
                        except: list = []
                        code = ''.join(list)
                        print code
                        if code == '403':
                                if time.time() - TIMER_403 < 2 and TIMER_403 > 0: return
                                TIMER_403 = time.time()
                                if jid in GROUPCHATS and fromjid.split('/')>1 and hasattr(el, 'body'):
                                        time.sleep(1.3)
                                        try: msg(self.jabberid, jid, u'Перенаправлено с привата (код 403):\n'+unicode(el.body))
                                        except: msg(self.jabberid, jid, u'Необходимо включить приватные сообщени в настройках комнаты!')
                        if code == '500' and hasattr(el, 'body'):
                                if time.time()-TIMER_500['t'] < 1.2 and TIMER_500['t'] > 0:
                                        if TIMER_500['clc']>20: return
                                        TIMER_500['clc']+=1
                                else:
                                        TIMER_500['clc'] = 0
                                TIMER_500['t'] = time.time()
                                msg(self.jabberid, jid, el.body)
                        return
		
		if len(fromjid.split('/'))==2:
                        res = fromjid.split('/')[1]
		
                for e in el.elements():
                        if e.uri in [NS_DELAY,NS_JABBER_DELAY]: return
                        if e.name == "body": body = e.__str__()
		
		call_message_handlers(el, mtype, [fromjid, jid, res, self.jabberid], body)

		bot_nick = get_bot_nick(jid)

		if res == bot_nick: return

                for x in [bot_nick+x for x in [':',',','>']]:
                        body=body.replace(x,'')

                body = body.strip()
                cbody = body
                if not body: return
		cmd = body.lower()
		parameters=''
		if body.count(' '):
                        s=body.split()
                        cmd=s[0].lower()
                        parameters=' '.join(s[1:])
                if cbody.count(' '): parameters = cbody[(cbody.find(' ') + 1):].strip()
                if cmd in COMMANDS:
                        print '- Commands Register'
                        if jid in COMMOFF and cmd in COMMOFF[jid]: return
                        call_command_handlers(cmd, mtype, [fromjid, jid, res, self.jabberid], unicode(parameters))
               
def read_file(filename):
        data=None
        try:
                fp = file(filename)
                data = fp.read()
                fp.close()
        except: pass
	return data

TO_ADMIN = {}

def to_admin(body):
        global TO_ADMIN
        global CLIENTS
        for x in [x for x in GLOBACCESS.keys() if GLOBACCESS[x]==100]:
                if not x in TO_ADMIN:
                        TO_ADMIN[x]={'m':body, 't':time.time()}
                else:
                        if time.time() - TO_ADMIN[x]['t']<15:
                                continue
                        if body == TO_ADMIN[x]['m']:
                                continue
                        TO_ADMIN[x]['m']=body
                        TO_ADMIN[x]['t']=time.time()
                i=random.choice(CLIENTS.keys())
                msg(i, x, body)

def write_file_gag(filename, data):
        fp = file(filename, 'w')
	fp.write(data)
	fp.close()

def write_file(filename, data):
        try: write_file_gag(filename, data)
        except: pass

def db_file(filename, typ=dict):
        attr, i = {dict:'{}',list:'[]'}, None
        if not os.path.exists(filename):
                fp = file(filename, 'w')
                fp.write(attr[typ])
                fp.close()
        else:
                fp = read_file(filename)
                try: i=eval(fp)
                except: write_file(filename, attr[typ])
                if not isinstance(i, typ):
                        write_file(filename, attr[typ])


def load_plugin():
        if os.path.exists('plugins'):
                f=os.listdir('plugins')
                n=0
                for x in f:
                        if x[-3:].lower() != '.py':
                                continue
                        try:
                                fp=file('plugins/'+x)
                                exec fp in globals()
                                fp.close()
                                n+=1
                        except Exception, err: print 'err in plugin load ',x,err
                print n,' plugin load'

def join(groupchat, nick, cljid):
        if not isinstance(groupchat, unicode):
                groupchat = groupchat.decode('utf-8','replace')
        BOT_NICK[groupchat] = nick
        if not GROUPCHATS.has_key(groupchat):
                GROUPCHATS[groupchat] = {}
        pth, i = '',''
        try:
                i=os.path.exists('dynamic/'+groupchat)
                pth='dynamic/'+groupchat
        except:
                i=os.path.exists('dynamic/'+groupchat.encode('utf8'))
                pth='dynamic/'+groupchat.encode('utf8')
        if not i:
                os.mkdir(pth,0755)
        db, status, show = {}, '', 'chat'
        try: db=eval(read_file('dynamic/chatroom.list'))
        except: pass
        if cljid in db.keys() and groupchat in db[cljid].keys():
                status=db[cljid][groupchat]['status']
                show=db[cljid][groupchat]['show']
        p = domish.Element(('jabber:client', 'presence'))
        p['to'] = u'%s/%s' % (groupchat, nick)
        p.addElement('status').addContent(status)
        p.addElement('show').addContent(show)
        p.addElement('x', 'http://jabber.org/protocol/muc').addElement('history').__setitem__('maxchars', '0')
        reactor.callFromThread(dd, p, CLIENTS[cljid])

def leave(groupchat, reason, cljid):
        p = domish.Element(('jabber:client', 'presence'))
        p['to'] = u'%s' % (groupchat)
        p['type'] = 'unavailable'
        p.addElement('status').addContent(reason)
        reactor.callFromThread(dd, p, CLIENTS[cljid])

def section(body, lenn, sys=0):
        rep=''
        k=' '
        if not body.count(' '):
                return body[:lenn]
        s=body.split(' ')
        if sys:
                if body.count('.'):
                        s=body.split('.')
                        k='.'
                if body.count('\n'):
                        s=body.split('\n')
                        k='\n'
        for x in s:
                if len(rep+k+x)<lenn:
                        rep+=k+x
                else:
                        break
        return rep
        

def reply(type, source, body):
        INFO['out']+=1
        if type=='private':
                type='chat'
        if type=='public':
                type='groupchat'
        if len(body)>5000:
                body = section(body, 5000, 1)
                body = body[:5000]
        if not isinstance(body, unicode):
                body=body.decode('utf-8','replace')
        for x in body:
                try:
                        if ord(x)<32 and ord(x) not in [10, 13]:
                                body=body.replace(x, str(ord(x)))
                except: pass
        if source[0].isdigit():
                time.sleep(1.5)
                reactor.callFromThread(icqs, source[0], body)
        else:
                try:
                        jids=get_true_jid(source)
                        if jids.count('mrim.'):
                                time.sleep(1.5)
                except: pass
                message = domish.Element(('jabber:client','message'))
                message["type"] = type
                if type in ['groupchat','tochat']:
                        if len(body)>1000 and type=='groupchat':
                                msg(source[3], source[1], source[2]+u': '+section(body, 500)+u' >>> [смотри в привате!]')
                                msg(source[3], source[1]+'/'+source[2], body)
                                return
                        message.addElement("body", "jabber:client", source[2]+': '+body)
                        message["to"] = jid.JID(source[1]).full()
                else:
                        message["to"] = jid.JID(source[0]).full()
                        message.addElement("body", "jabber:client", body)
                reactor.callFromThread(dd, message, CLIENTS[source[3]])
        call_outgoing_message_handlers(get_true_jid(source), body, body)

def msg(cljid, jid, body):
        INFO['out']+=1
        type = 'chat'
        if jid in GROUPCHATS:
                type = 'groupchat'
        if jid.isdigit():
                try:
                        reactor.callFromThread(icqs, jid, body)
                except: print 'Exception in msg'
        else:
                message = domish.Element(('jabber:client','message'))
                message["type"] = type
                message["to"] = jid
                message.addElement("body", "jabber:client", body)
                reactor.callFromThread(dd, message, CLIENTS[cljid])
        call_outgoing_message_handlers(jid, body, body)

def icqs(to, body):
        try: INFO['tout'] += sys.getsizeof(body)
        except: pass
        ICQ.sendMessage(to, [(body.encode('windows-1251','ignore'),"windows-1251")])
        
def dd(x, cl=''):
        if not cl: return
        try: INFO['tout'] += sys.getsizeof(x)
        except: pass
        
        if not hasattr(cl, 'send'):
                pass
        else: cl.send(x)
        

def stage0(cljid):
        global INFO
        for process in STAGE0_INIT:
                INFO['thr'] += 1
		try: threading.Thread(None,process,'stage0_init'+str(INFO['thr']),(cljid,)).start()
		except: pass

def load_rooms(selfjid):
        f = 'dynamic/chatroom.list'
        db_file(f, dict)
        db = eval(read_file(f))
        if not selfjid in db.keys() or not selfjid in CLIENTS.keys():
                return
        for x in db[selfjid]:
                if 'nick' in db[selfjid][x] and 'status' in db[selfjid][x] and 'show' in db[selfjid][x]:
                        for process in STAGE1_INIT:
                                try: threading.Thread(None,process,'stage1_init'+str(INFO['thr']),(x,)).start()
                                except: pass
                        join(x, db[selfjid][x]['nick'], selfjid)

def load_account():
        a, b = GENERAL_CONFIG("JABBER_ID2"), GENERAL_CONFIG("JABBER_PASS2")
        if a and b:
                reactor.callFromThread(JabberBot, a, b)
        c, d = GENERAL_CONFIG("JABBER_ID3"), GENERAL_CONFIG("JABBER_PASS3")
        if c and d:
                reactor.callFromThread(JabberBot, c, d)
        JabberBot(JABBER_ID, JABBER_PASS)


if __name__ == "__main__":
        def hnd_exit(sig, func=None):
                print '\nGood bye!\n'
                time.sleep(2)
                os._exit(1)
        set_exit_handler(hnd_exit)
	try:
                load_plugin()
                load_account()
        except KeyboardInterrupt:
                print 'CTRL+C'
                os._exit()
        except UnicodeWarning:
                pass
        except Exception as err:
                try: print err
                except: pass
                err_write(err)

