# -*- coding: utf-8 -*-


import base64

def ibb_request(t, s, tojid, sid, name, size, about, fp, fz):
    iq = IQ(CLIENTS[s[3]], 'set')
    iq['to'] = tojid
    iq['id'] = str(random.randrange(100,999))
    si = iq.addElement('si', 'http://jabber.org/protocol/si')
    si['profile'] = 'http://jabber.org/protocol/si/profile/file-transfer'
    si['id'] = sid
    si['mime-type'] = 'text/plain'
    file = si.addElement('file', 'http://jabber.org/protocol/si/profile/file-transfer')
    file['name'] = name
    file['size'] = str(size)
    file.addElement('desc',  content = about)
    file.addElement('range')
    feature = si.addElement('feature', 'http://jabber.org/protocol/feature-neg')
    x = feature.addElement('x', 'jabber:x:data')
    x['type'] = 'form'
    field = x.addElement('field')
    field['var'] = 'stream-method'
    field['type'] = 'list-single'
    field.addRawXml('<option><value>http://jabber.org/protocol/ibb</value></option>')
    #print iq.toXml()
    iq.addCallback(ibb_result_handler, t, s, tojid, sid, fp, fz)
    reactor.callFromThread(iq.send, tojid)

def hnd_ibb(t, s, p):
    groupchat=s[1]
    nick = s[2]
    tojid, fz = '', 'message'
    if not GROUPCHATS.has_key(groupchat):
        reply(type, source, u'Эта команда может быть использована только в конференции!')
        return
    if p:
        if GROUPCHATS[groupchat].has_key(nick):
            tojid = GROUPCHATS[groupchat][nick]['jid']
	if not tojid:
            reply(t, s, u'Внутреняя ошибка, невозможно выполнить операцию!')
	    return
	sid = 'file'+str(random.randrange(10000000, 99999999))
	if p.count(' '):
            p=p.split()[0]
            fz='iq'
	if p in [u'log']:
            try: p = os.path.join(PUBLIC_LOG_DIR, s[1], str(time.localtime()[0]),str(time.localtime()[1]),str(time.localtime()[2])+'.html')
            except:
                reply(t, s, u'Файла несуществует!')
                return
		

	if not os.path.exists(p):
            reply(t, s, u'Файла несуществует!')
            return
        size = os.path.getsize(p)
        try: fp = open(p,'rb')
	except:
            reply(t, s, u'Невозможно открыть этот файл!')
	    return
	ibb_request(t, s, tojid, sid, p, size, p, fp, fz)
    else:
        reply(t, s, u'И какой мне файл передавать?')
    

def ibb_result_handler(t, s, tojid, sid, fp, fz, x):
    if x['type']=='result':
        reply(t, s, u'Передача файла начата!')
        ibb_open(tojid, sid, fz, s[3])
        seq = 0
        while 1:
            dat = fp.read(4096)
            if dat=='':
                break
            iq = domish.Element(('jabber:client', fz))
            iq['to'] = tojid
            iq['id'] = str(random.randrange(100,999))
            data = iq.addElement('data', 'http://jabber.org/protocol/ibb')
            data['sid'] = sid
            data['seq'] = str(seq)
            data.addContent(base64.encodestring(dat))
            reactor.callFromThread(dd, iq)
            seq+=1
        time.sleep(0.5)
        iq = domish.Element(('jabber:client', 'iq'))
        iq['to'] = tojid
        iq['type'] = 'set'
        iq['id'] = str(random.randrange(100,999))
        opn = iq.addElement('close', 'http://jabber.org/protocol/ibb')
        opn['sid'] = sid
        reactor.callFromThread(dd, iq)
        reply(t, s, u'Файл передан!')
        fp.close()
    else:
        reply(t, s, u'Передача файла невозможна!')

def ibb_open(tojid, sid, fz, cljid):
    iq = domish.Element(('jabber:client', 'iq'))
    iq['type'] = 'set'
    iq['to'] = tojid
    opn = iq.addElement('open', 'http://jabber.org/protocol/ibb')
    opn['sid'] = sid
    opn['block-size'] = '4096'
    opn['stanza'] = fz
    reactor.callFromThread(dd, iq, CLIENTS[cljid])

register_command_handler(hnd_ibb, 'get_file', ['все'], 100, 'Получение файлов через бота посредством IBB In-band. Доп. ключи команды - log, передаст файл логов текущей конференции за этот день.', 'get_file file', ['get_file err.html'])

