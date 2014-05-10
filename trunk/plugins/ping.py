# -*- coding: utf-8 -*-

#e = threading.Event()
#e.wait()

USER_PING_FILE = 'dynamic/user_ping.txt'

initialize_file(USER_PING_FILE, '{}')

TURBO_PING = {}

features = {'http://jabber.org/protocol/activity':'XEP-0108: User Activity',
            'http://jabber.org/protocol/address':'XEP-0033: Extended Stanza Addressing',
            'http://jabber.org/protocol/amp':'XEP-0079: Advanced Message Processing',
            'http://jabber.org/protocol/bytestreams':'XEP-0065: SOCKS5 Bytestreams',
            'http://jabber.org/protocol/caps':'XEP-0115: Entity Capabilities',
            'http://jabber.org/protocol/chatstates':'XEP-0085: Chat State Notifications',
            'http://jabber.org/protocol/commands':'XEP-0050: Ad-Hoc Commands',
            'http://jabber.org/protocol/compress':'XEP-0138: Stream Compression',
            'http://jabber.org/protocol/disco':'XEP-0030: Service Discovery',
            'http://jabber.org/protocol/feature-neg':'XEP-0020: Feature Negotiation',
            'http://jabber.org/protocol/geoloc':'XEP-0080: User Geolocation',
            'http://jabber.org/protocol/http-auth':'XEP-0072: SOAP Over XMPP',
            'http://jabber.org/protocol/httpbind':'XEP-0124: Bidirectional-streams Over Synchronous HTTP',
            'http://jabber.org/protocol/ibb':'XEP-0047: In-Band Bytestreams',
            'http://jabber.org/protocol/mood':'XEP-0107: User Mood',
            'http://jabber.org/protocol/muc':'XEP-0045: Multi-User Chat',
            'http://jabber.org/protocol/offline':'XEP-0013: Flexible Offline Message Retrieval',
            'http://jabber.org/protocol/physloc':'XEP-0080: User Geolocation',
            'http://jabber.org/protocol/pubsub':'XEP-0060: Publish-Subscribe',
            'http://jabber.org/protocol/rosterx':'XEP-0144: Roster Item Exchange',
            'http://jabber.org/protocol/sipub':'XEP-0137: Publishing SI Requests',
            'http://jabber.org/protocol/soap':'XEP-0072: SOAP Over XMPP',
            'http://jabber.org/protocol/waitinglist':'XEP-0130: Waiting Lists',
            'http://jabber.org/protocol/xhtml-im':'XEP-0071: XHTML-IM',
            'http://jabber.org/protocol/xdata-layout':'XEP-0141: Data Forms Layout',
            'http://jabber.org/protocol/xdata-validate':'XEP-0122: Data Forms Validation',
            'ipv6':'Support of IPv6',
            'jabber:client':'RFC 3921: XMPP IM',
            'jabber:component:accept':'XEP-0114: Existing Component Protocol',
            'jabber:component:connect':'XEP-0114: Existing Component Protocol',
            'jabber:iq:auth':'XEP-0078: Non-SASL Authentication',
            'jabber:iq:browse':'XEP-0011: Jabber Browsing',
            'jabber:iq:gateway':'XEP-0100: Gateway Interaction',
						'jabber:iq:last':															'XEP-0012: Last Activity',
						'jabber:iq:oob':															'XEP-0066: Out of Band Data',
						'jabber:iq:pass':															'XEP-0003: Proxy Accept Socket Service',
						'jabber:iq:privacy':													'RFC 3921: XMPP IM',
						'jabber:iq:private':													'XEP-0049: Private XML Storage',
						'jabber:iq:register':													'XEP-0077: In-Band Registration',
						'jabber:iq:roster':														'RFC 3921: XMPP IM',
						'jabber:iq:rpc':															'XEP-0009: Jabber-RPC',
						'jabber:iq:search':														'XEP-0055: Jabber Search',
						'jabber:iq:time':															'XEP-0202: Entity Time',
						'jabber:iq:version':													'XEP-0092: Software Version',
						'jabber:server':															'RFC 3921: XMPP IM',
						'jabber:x:data':															'XEP-0004: Data Forms',
						'jabber:x:delay':															'XEP-0203: Delayed Delivery',
						'jabber:x:encrypted':													'XEP-0027: Current OpenPGP Usage',
						'jabber:x:event':															'XEP-0022: Message Events',
						'jabber:x:expire':														'XEP-0023: Message Expiration',
						'jabber:x:oob':																'XEP-0066: Out of Band Data',
						'jabber:x:roster':														'XEP-0093: Roster Item Exchange',
						'jabber:x:signed':														'XEP-0027: Current OpenPGP Usage',
						'urn:xmpp:delay':															'XEP-0203: Delayed Delivery',
						'urn:xmpp:ping':															'XEP-0199: XMPP Ping',
						'urn:xmpp:receipts':													'XEP-0199: XMPP Ping',
						'urn:xmpp:ssn':																'XEP-0155: Stanza Session Negotiation',
	    'urn:xmpp:time':'XEP-0202: Entity Time',
            'vcard-temp':'XEP-0054: vcard-temp'}

def hnd_disco_info(t, s, p):
    if not p:
        return
    if s[1] in GROUPCHATS and p in GROUPCHATS[s[1]].keys():
        p = s[1]+'/'+p
    packet = IQ(CLIENTS[s[3]], 'get')
    packet.addElement('query', 'http://jabber.org/protocol/disco#info')
    packet.addCallback(disco_info_answ, t, s, p)
    reactor.callFromThread(packet.send, p)


def disco_info_answ(t, s, p, x):
    cat = ''
    info = 1
    rep = ''
    client = 0

    
    if x['type'] == 'result':
        
        try:
            cat = x.children[0].children[0].attributes['category']
            if cat in ['client']:
                client = 1
        except:
            client = 1
        if client:
            try:
                list = [c.attributes for c in element2dict(x)['query'].children if hasattr(c, 'attributes')]
                if list[0].get('category','')=='client':
                    rep+=u'Фичи клиента '+str(len(list)-1)+':\n'
                    for c in list[1:]:
                        a = c.get('var','').__str__()
                        rep+=(a if not a in features else features[a])+'\n'
                    info = [c for c in x.children[0].elements() if c.uri == 'jabber:x:data']
                    info = ([] if not info else info[0])
                    if info and info.children:
                        
                        for m in info.children:
                            try:
                                i = element2dict(m)['value'].__str__()
                                if not i.isspace():
                                   
                                    
                                    rep+= m.attributes['var']+': '+i+'\n'
                            except: pass
                    reply(t, s, rep)
            except:
                raise
                reply(t, s, u'Глюк')
                return
        if cat in ['server','pubsub']:
            list = [c.attributes.get('var',None) for c in x.children[0].children if c.attributes.get('var',None)]
            reply(t, s, u'Фичи сервера '+str(len(list))+':\n'+'\n'.join([(x if not x in features else features[x]) for x in list]))
        elif cat == 'conference':
            rep+=x.children[0].children[0].attributes.get('name','')+'\n'

            list = [c.attributes.get('var',None) for c in x.children[0].children if c.attributes.get('var',None)]
            rep+=', '.join(list); rep+='\n'
            info = [c for c in x.children[0].elements() if c.uri == 'jabber:x:data']
            info = ([] if not info else info[0])
            if info and info.children:
                for x in info.children:
                    try:
                        i = element2dict(x)['value'].__str__()
                        if not i.isspace():
                            rep+= x.attributes['label']+': '+i+'\n'
                    except: pass
            rep+=''
            reply(t, s, rep)
        
    else:
        reply(t, s, u'Не судьба')#390 41 22

register_command_handler(hnd_disco_info, 'инфо', ['все'], 0, 'Информация о сервере,конференции или нике, улучшеный аналог команды фичи.', 'инфо <jid>', ['инфо mafiozo.in'])


def hnd_turbo_info(t, s, p):
    rep = str()
    if TURBO_PING:
        if not p:
            reply(t, s, '\n'.join([str(TURBO_PING.keys().index(x)+1)+') '+x for x in TURBO_PING.keys()])+u'\nВыберите номер')
            return
        if p and p.isdigit() and len(TURBO_PING)>=int(p)-1:
            reply(t, s, '\n'+', '.join([str(x) for x in TURBO_PING[TURBO_PING.keys()[int(p)-1]]['jid']]))
    else:
        reply(t, s, u'Пусто')

TRB_BUF = {}

#sh = None

def hnd_turboping(t, s, p):
    global TURBO_PING
    global TURBO_SERVER
    global TURBO_S2S
    VAR = {'jid':[0,3,5,7,9,11,12,14,17,19],'bot':[1,6,13,15,18],'s2s':[2,4,8,10,16]}

    usr = get_true_jid(s)

    if usr in TRB_BUF.keys():
        reply(t, s, u'Дождитесь окончания тестирования!')
        return

    TRB_BUF[usr] = time.time()

    def errping(x, t, s, jid, i):
        out = 'IQ timed out'

        ##print jid
        
        try:
            err = re.findall('\'(.*?)\'',x.getErrorMessage())
            if not err:
                err = x.getErrorMessage()
            else:
                err = err[0]
        except:
            err = str()
        if get_true_jid(s) in TRB_BUF:
            if err and err=='IQ timed out':
                if jid.split('/')[0]==s[3]:
                    reply(t, s, u'Что-то я вишу, попробуйте позже!')
                    
                else:
                    reply(t, s, u'Понг провален, таймаут 120 секунд истек!')
            else:
                reply(t, s, u'Фигня какаято: '+(err if err else u'сообщение об ошибке не прочитано')+u'\nПотрачено времени ожидания: '+str(round(time.time()-i, 3))+'c.')
        try: del TRB_BUF[get_true_jid(s)]
        except: pass

    def turboping_handler(x, jid, i, type, s):
        if not hasattr(x, '__getitem__'):
            return
        if x['type'] == 'result':
            t = time.time()

            if int(x['id'])==0:
                reply(type, s, u'Идет тестирование, первый отклик без учета ботпинга '+str(round(t-i, 3))+'c.')

            if int(x['id']) in VAR['bot']:#range(11, 16):
                TURBO_PING[jid]['bot'].append(round(t-i, 3))
            if int(x['id']) in VAR['s2s']:
                TURBO_PING[jid]['s2s'].append(round(t-i, 3))
            if int(x['id']) in VAR['jid']:
                TURBO_PING[jid]['jid'].append(round(t-i, 3))
        else:
            ERROR={'400':u'Плохой запрос','401':u'Не авторизирован','402':u'Требуется оплата','403':u'Запрещено','404':u'Не найдено','405':u'Не разрешено','406':u'Не приемлемый','407':u'Требуется регистация','408':u'Время ожидания ответа вышло','409':u'Конфликт','500':u'Внутренняя ошибка сервера','501':u'Не реализовано','503':u'Сервис недоступен','504':u'Сервер удалил запрос по тайм-ауту'}
            if x['type'] == 'error':
                try: del TRB_BUF[get_true_jid(s)]
                except: pass
                try: code = [c['code'] for c in x.children if (c.name=='error')]
                except: code = []
                if ' '.join(code) in ERROR: add=ERROR[' '.join(code)]
                reply(type, s, u'Не пингуется. '+' '.join(code)+' '+add)
        
    
    if s[0].isdigit():
        reply(t, s, u'Only for Jabber protocol!')
        return
    jid = s[1]+'/'+s[2]
    if p:
        jid = p
        if s[1] in GROUPCHATS and p in GROUPCHATS[s[1]]:
            jid = s[1]+'/'+p

    TURBO_PING[jid]={'jid':[],'bot':[],'s2s':[]}
    
    #reply(t, s, u'Тестирование займет несколько минут')
    tojid = ''
    srv = ''
    smb = ''
    for x in range(20):

        if not usr in TRB_BUF.keys():
            return

        tojid = jid
        
        if x in VAR['s2s']:
            if jid.count('@'):
                smb = '@'
                if jid.count('@conference.'):
                    smb = '@conference.'
                tojid = jid.split(smb)[1]
                if tojid.count('/'):
                    tojid = tojid.split('/')[0]
                srv = tojid
                
            else:
                break
        if x in VAR['bot']:#range(11, 16):
            tojid = s[3]+'/JabberBot'
        
        packet = xmlstream.IQ(CLIENTS[s[3]], 'get')
        packet.timeout = 120
        packet['id'] = str(x)
        packet['to'] = tojid
        ##print tojid,x
        packet.addElement('query', 'jabber:iq:version')
        #packet.addCallback(turboping_handler, jid, time.time())
        #reactor.callFromThread(packet.send, tojid)
        def sender(packet, jid, t, s, tojid):
            ts = time.time()
            d = packet.send()
            d.addErrback(errping, t, s, tojid, ts)
            d.addCallback(turboping_handler, jid, ts, t, s)
        reactor.callFromThread(sender, packet, jid, t, s, tojid)
        time.sleep(3)
    tt = time.time()
    while len(TURBO_PING[jid]['jid'])+len(TURBO_PING[jid]['bot'])+len(TURBO_PING[jid]['s2s'])<19:
        if time.time()-tt<160:
            time.sleep(1)
            pass
        break
    if len(TURBO_PING[jid]['jid'])<3:
        if usr in TRB_BUF.keys():
            del TRB_BUF[usr]
            reply(t, s, u'Часть пакетов утеряна, облом')
        return
    try:
        l = getMedian(TURBO_PING[jid]['jid'])
        bot = getMedian(TURBO_PING[jid]['bot'])
    except:
        if usr in TRB_BUF.keys():
            del TRB_BUF[usr]
            reply(t, s, u'Глюк какойто')
        return
    s2s = 0
    if len(TURBO_PING[jid]['s2s'])>2:
        s2s = getMedian(TURBO_PING[jid]['s2s']) - bot
        if s2s<0:
            s2s=0.00
    rez = round((l-bot)-s2s, 3)
    rep = '\n- '+str(rez)+u' секунд.\n'
    mp = (min(TURBO_PING[jid]['jid'])-bot)-s2s
    rep += u'- Минимальный '+(str(mp) if mp>0.01 else '0.01')+u'с. ;\n - Mаксимальный '+str((max(TURBO_PING[jid]['jid'])-bot)-s2s)+u'с. ;\n - Cредний результат '
    rep += u' из '+str(len(TURBO_PING[jid]['jid']))+u' запросов '+str(round(l, 3))+u' с. ;\n'
    rep += u'- Ботпинг '+str(bot)+u'c. ;\n'
    rep += u'- Понг от сервера '+s[3].split('@')[1]+u' до '+srv+' '+str(round(s2s, 2))+u'c. ;\n'
    rep += u'- Результат = ('+str(round(l, 3))+' - '+str(bot)+') - '+str(round(s2s, 2))+' = '+str(rez)+'\n'
    res = (l-bot)-s2s
    #if res < 0:
    #    if usr in TRB_BUF.keys():
    #        del TRB_BUF[usr]
    #        reply(t, s, u'Что-то глюкнуло!'+('\nPING JID: '+', '.join([str(x) for x in TURBO_PING[jid]['jid']])+'\nPING BOT: '+', '.join([str(x) for x in TURBO_PING[jid]['bot']]) if len(TURBO_PING[jid]['bot'])>1 and len(TURBO_PING[jid]['jid'])>1 else ''))
    #    return
    rep +=u'- Оценка понга по шкале от 0 до 5-ти '
    if res <= 0.1:
        rep+=u' 5+'
    if res <= 0.6 and res> 0.1:
        rep+=u' 5'
    if res <= 1.1 and res>0.6:
        rep+=u' 4'
    if res <=2.2 and res>1.1:
        rep+=u' 3'
    if res <=5.5 and res>2.2:
        rep+=u' 2'
    if res <=8.8 and res>5.5:
        rep+=u' 1'
    if res >8.8:
        rep+=u' 0'
    if usr in TRB_BUF.keys():
        reply(t, s, rep)
        del TRB_BUF[usr]


register_command_handler(hnd_turboping, 'турбопинг', ['все'], 0, 'Проверяет пинг указаного адреса в течении минуты, выводит медиану, максимальное и минимально значение.', 'турбопинг', ['турбопинг'])
register_command_handler(hnd_turbo_info, 'турбоинфа', ['все'], 0, 'Журнал турбопинга', 'турбоинфа', ['турбоинфа'])


def turboping_handler_(jid, i, x):
    global TURBO_PING
    global TURBO_SERVER
    
    if x['type'] == 'result':
        t = time.time()
        
        if int(x['id']) in range(11, 16):
            TURBO_PING[jid]['bot'].append(round(t-i, 3))
        if int(x['id']) in range(16, 21):
            TURBO_PING[jid]['s2s'].append(round(t-i, 3))
        if int(x['id'])<11:
            TURBO_PING[jid]['jid'].append(round(t-i, 3))
    else:
        pass


def getMedian(numericValues):
    theValues = sorted(numericValues)
    if len(theValues) % 2 == 1:
        return theValues[(len(theValues)+1)/2-1]
    else:
        lower = theValues[len(theValues)/2-1]
        upper = theValues[len(theValues)/2]
    return (float(lower + upper)) / 2
    


def ping_handler(t, s, p):
    if s[0].isdigit():
        reply(t, s, u'Понг')
        return
    def errping(x, t, s):
        try:
            err = re.findall('\'(.*?)\'',x.getErrorMessage())
            if not err:
                err = x.getErrorMessage()
            else:
                err = err[0]
        except:
            err = str()
        reply(t, s, u'Сервер ответил ошибкой: '+err)
    if t == 'irc':
        if s[0] in IRC_PING.keys():
            reply(t, s, u'Запрос выполняется')
            return
        if s[1]!=IRC_NICK:
            IRC_PING[s[0]] = s[1]
        else:
            IRC_PING[s[0]] = s[0]
        IRC.ping(ircn(s[0]))
        return
    jid = s[1]+'/'+s[2]
    if p:
        if s[1] in GROUPCHATS and p in GROUPCHATS[s[1]]:
            jid = s[1]+'/'+p
        else:
            jid = p
    packet = xmlstream.IQ(CLIENTS[s[3]], 'get')#IQ
    packet.timeout = 20
    packet.addElement('query', 'jabber:iq:version')
    packet['id'] = str(random.randrange(1,9999))
    packet['to'] = jid
    #packet.addCallback(ping_result_handler, t, s, p, time.time())
    #reactor.callFromThread(packet.send, jid)
    def sender(packet, t, s, p):
        d = packet.send()
        d.addErrback(errping, t, s)
        d.addCallback(ping_result_handler, t, s, p, time.time())
            
    reactor.callFromThread(sender, packet, t, s, p)
    
    



def ping_result_handler(x, type, s, p, i):#last x arg, first type to old method
    add=''
    if not hasattr(x, '__getitem__'):
        return
    ERROR={'400':u'Плохой запрос','401':u'Не авторизирован','402':u'Требуется оплата','403':u'Запрещено','404':u'Не найдено','405':u'Не разрешено','406':u'Не приемлемый','407':u'Требуется регистация','408':u'Время ожидания ответа вышло','409':u'Конфликт','500':u'Внутренняя ошибка сервера','501':u'Не реализовано','503':u'Сервис недоступен','504':u'Сервер удалил запрос по тайм-ауту'}
    if x['type'] == 'error':
        try: code = [c['code'] for c in x.children if (c.name=='error')]
        except: code = []
        if ' '.join(code) in ERROR: add=ERROR[' '.join(code)]
        reply(type, s, u'Не пингуется. '+' '.join(code)+' '+add)
        return
    elif x['type'] == 'result':
        t = time.time()
        rep = u'понг от '
	if p:
            rep += p
	else:
            rep += u'тебя'
	rep+=u' '+str(round(t-i, 3))+u' секунд'
        reply(type, s, rep)


def time_handler(t, s, p):
    jid = s[1]+'/'+s[2]
    if p: jid = p
    if s[1] in GROUPCHATS and p:
        if p in GROUPCHATS[s[1]]:
            jid=s[1]+'/'+p
        else:
            jid=p
    packet = IQ(CLIENTS[s[3]], 'get')
    packet.addElement('query', 'jabber:iq:time')
    packet.addCallback(time_result_handler, t, s, p)
    reactor.callFromThread(packet.send, jid)

def time_result_handler(t, s, p, x):
    try:
        query = element2dict(x)['query']
        display = element2dict(query)['display']
        reply(t, s, display.children[0])
    except:
        urnxmpptime(t, s, p)


def urnxmpptime(t, s, p):
    jid = s[1]+'/'+s[2]
    if p: jid = p
    if s[1] in GROUPCHATS and p:
        if p in GROUPCHATS[s[1]]:
            jid=s[1]+'/'+p
        else:
            jid=p
    packet = IQ(CLIENTS[s[3]], 'get')
    packet.addElement('time', 'urn:xmpp:time')
    packet.addCallback(timenew_result, t, s, p)
    reactor.callFromThread(packet.send, jid)


def getTag(element,name,xmlns = None):
	for el in element.elements():
		if not isinstance(el,basestring) and el.name == name:
			if xmlns and el.uri == xmlns:
				return el
			return el
	return None

def getTags(element,name,xmlns=None):
	if xmlns is None:
		filtAlg = lambda el : not isinstance(el,basestring) and el.name == name
	else:
		filtAlg = lambda el : not isinstance(el,basestring) and el.name == name and el.uri == xmlns
	result = filter(filtAlg,element.elements())
	return (result if result else None)

def timenew_result(t, s, p, x):
    try:
        def tm_grab():
            try: url = urllib.urlopen('http://wap.infan.ru/serv/time/').read()
            except: url = ''
            ft = re.findall('\d{1,2}.\d{1,2}.\d{4} \d{1,2}:\d{1,2}:\d{1,2}', url, re.DOTALL)
            return ft
        tzo, utc, dt2 = '','',0

        
        if x['type']=='error':
            reply(t, s, u'На urn:xmpp:time сервис ответил ошибкой!')
            return
        
        fmt = '%Y-%m-%d %H:%M:%S'

        try:
            tzo = getTag(x.children[0],'tzo')
            utc = getTag(x.children[0],'utc')
        except:
            query = element2dict(x)['time']
            tzo = element2dict(query)['tzo']
            utc = element2dict(query)['utc']

        tzo, utc = tzo.children[0], utc.children[0]

        utc = utc.replace('T',' ').replace('Z','')
        if utc.count('.'): utc = utc.split('.')[0]

        ss = tzo[1:].split(':')
        h = int(ss[0])
        m = int(ss[1])
        import datetime
        if tzo[:1] in ['-']:
            try: dt2 = datetime.datetime(*time.strptime(utc, fmt)[:6])-datetime.timedelta(hours=h, minutes=m)
            except: dt2 = 0
        if tzo[:1] in ['+']:
            try: dt2 = datetime.datetime(*time.strptime(utc, fmt)[:6])+datetime.timedelta(hours=h, minutes=m)
            except: dt2 = 0
        i = tm_grab()
        reply(t, s, ('' if not i or len(i)<2 else u'\nИнформация WEB:\n   Москoвское время:\n     '+i[0]+'\n')+u'Ответ клиента:\n  Часовой пояс '+tzo+u'\n     Время по Гринвичу (GMT) '+utc+u'\n    На экране '+str(dt2))
    except:
        reply(t, s, u'Невозможно определить время!')


def disco_handler(t, s, p):
    if p:
        if p.count(' '):
            n = p.split()
            p, grep = n[0], n[1]
        else:
            p, grep = p, ' '
        if not p.count('.'):
            p=p+'@conference.jabber.ru'
        packet = IQ(CLIENTS[s[3]], 'get')
        packet.addElement('query', 'http://jabber.org/protocol/disco#items')
        packet.addCallback(disco_result_handler_a, t, s, p, grep)
        reactor.callFromThread(packet.send, p)
    else: reply(t, s, u'и?')

def disco_result_handler_a(t, s, p, grep, x):
    if x['type'] == 'result':
        query = element2dict(x)['query']
        query = [i.attributes for i in query.children if i.__class__==domish.Element]
        if p.count('conference.') or p.count('chat.') or p.count('muc.'):
            if p.count('@'):
                r = [i.get('name') for i in query]
                r.sort()
            else:
                r = []
                for i in query:
                    try: g = re.search('^(.+)\(([0-9]+)\)$', i['name']).groups()
                    except: g = (i['name'], '0')
                    if int(g[1]) < 99: r.append((g[0], i['jid'], g[1]))
                r.sort(lambda x, y: cmp(int(y[2]), int(x[2])))
                r = ['%s - %s (%s)' % i for i in r]
                ###r = r[:100]
        else:
            r = [i['jid'] for i in query]
            r.sort()
        if r: reply(t, s, u'Надискаверил:\n'+show_list(r, grep))
        else: reply(t, s, u'Пустое диско!')
    elif x['type'] == 'error':
        code, add = [], ''
        ERROR={'400':u'Плохой запрос','401':u'Не авторизирован','402':u'Требуется оплата','403':u'Запрещено','404':u'Не найдено','405':u'Не разрешено','406':u'Не приемлемый','407':u'Требуется регистация','408':u'Время ожидания ответа вышло','409':u'Конфликт','500':u'Внутренняя ошибка сервера','501':u'Не реализовано','503':u'Сервис недоступен','504':u'Сервер удалил запрос по тайм-ауту'}
        try: code = [c['code'] for c in x.children if (c.name=='error')]
        except: pass
        if ''.join(code) in ERROR: add=ERROR[' '.join(code)]
        reply(t, s, u'Не дискаверится. '+' '.join(code)+' '+add)
        return

def show_list(seq, grep=None, empty='[empty list]'):
 if len(seq) == 1: return seq[0]
 else:
  r = ''
  for i in range(len(seq)):
   r += '%s) %s\n' % (i+1, seq[i])
  if grep: r = '\n'.join([i for i in r.split('\n') if i.lower().count(grep.lower())])
  if not r: r = empty
  return r

USER_PING = {}

def join_user_ping(g, n, r, a, cljid):
    global USER_PING
    if not g in USER_PING or not g in GROUPCHATS or get_bot_nick(g)==n:
        return
    if 'timel' in USER_PING[g] and 'limit' in USER_PING[g] and 'now' in USER_PING[g]:
        if time.time() - USER_PING[g]['timel']<60:
            USER_PING[g]['now']+=1
            USER_PING[g]['timel'] = time.time()
            if USER_PING[g]['now']>USER_PING[g]['limit']:
                if a in ['participant']:
                    room_access(cljid, g, 'role', 'visitor', 'nick', n)
                return
        USER_PING[g]['timel'] = time.time()
        if USER_PING[g]['now']!=0: USER_PING[g]['now'] = 0
    jid=g+'/'+n
    if a in ['participant','visitor']:
        if a==u'participant':
            room_access(cljid, g, 'role', 'visitor', 'nick', n)
        packet = IQ(CLIENTS[cljid], 'get')
        packet.addElement('query', 'jabber:iq:version')
        packet.addCallback(user_ping_result, g, n, cljid)
        reactor.callFromThread(packet.send, jid)

def user_ping_result(g, n, cljid, x):
    if x['type'] == 'result':
        if g in USER_PING:
            t = USER_PING[g].get('timer',3)
            time.sleep(t)
        room_access(cljid, g, 'role', 'participant', 'nick', n)

def user_ping_init(cljid):
    try: db = eval(read_file(USER_PING_FILE))
    except:
        write_file(USER_PING_FILE, '{}')
        db = {}
    global USER_PING
    USER_PING = db.copy()

def hnd_user_ping(t, s, p):
    if not s[1] in GROUPCHATS: return
    if not p:
        reply(t, s, u'Читай помощь по команде!')
        return
    if p=='0':
        if not s[1] in USER_PING:
            reply(t, s, u'уже отключено!')
            return
        del USER_PING[s[1]]
        write_file(USER_PING_FILE, str(USER_PING))
        reply(t, s, u'Отключил!')
        return
    if p=='1':
        if s[1] in USER_PING:
            reply(t, s, u'уже работает!')
            return
        USER_PING[s[1]]={'limit':0,'now':0,'timel':time.time()}
        write_file(USER_PING_FILE, str(USER_PING))
        reply(t, s, u'Теперь включено!')
        return
    if p.split() and p.split()[0] == u'лимит' and p.split()[1].isdigit():
        USER_PING[s[1]]={'limit':int(p.split()[1]),'now':0,'timel':time.time()}
        write_file(USER_PING_FILE, str(USER_PING))
        reply(t, s, u'Установлен лимит на выдачу войса '+p.split()[1]+u' юзеров в минуту!')
    if p.split() and p.split()[0] == u'таймер' and p.split()[1].isdigit():
        if not s[1] in USER_PING:
            USER_PING[s[1]]={}
        USER_PING[s[1]]['timer']=int(p.split()[1])
        write_file(USER_PING_FILE, str(USER_PING))
        reply(t, s, u'ok!')

register_join_handler(join_user_ping)
register_stage0_init(user_ping_init)
register_command_handler(urnxmpptime, 'time', ['все'], 0, 'Показывает время юзая XEP-0202 (urn:xmpp:time)', 'time ник', ['time вася'])
register_command_handler(hnd_user_ping, 'юзер_пинг', ['все'], 20, 'Пингует вошедшего юзера, и только после ответа клиента выдает голос. Команда может использоваться против примитивных спам-ботов. Для установки лимита на количество выдачи голосов за минут используем ключ команды <лимит> <число>; Для установки таймера выдачи голоса вошедшим после ответа их клиента используем ключ <таймер> <секунды>', 'юзер_пинг <0|1|лимит>', ['юзер_пинг 1','юзер_пинг лимит 1'])
register_command_handler(disco_handler, 'диско', ['все'], 0, 'Дискаверит конференцию или сервер.', 'диско чат', ['диско cool@conference.talkonaut.com'])
register_command_handler(time_handler, 'часики', ['все'], 0, 'часики', 'часики ник', ['часики вася'])
register_command_handler(hnd_turboping, 'пинг', ['все'], 0, 'пинг', 'пинг', ['пинг'])
