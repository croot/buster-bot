# -*- coding: utf-8 -*-


MUC_FILT = {'fool':{},'onlymemb':{}}

MUC_FCON = {'member':{},'t1':0}

MFILT = 'dynamic/mucfilt.txt'

MFILT_WHITE = 'dynamic/mucfilt_members.txt'

db_file(MFILT, dict)
db_file(MFILT_WHITE, dict)

MCFILT_FOOL = [u'люблю сосать хуи',u'я сегодня на помойке почти новый вебратор нашол',u'пойду ща есть какашки',u'люблю обмазывать себя какашками',u'пук']

MCF_NS = 'http://jabber.ru/muc-filter'

def iq_muc(xs):
    if xs['type']!='set': return
    
    for query in xs.elements(): xmlns = query.uri
    
    if xmlns != MCF_NS: return

    #global z

    xmlns, type, body, traf, jid, m = None, None, None, 0, None, None

    try: traf = sys.getsizeof(xs)
    except: pass
    
    iq = IQ(JAB, 'result')
    iq['to'] = xs['from']
    iq['id'] = xs['id']
    query = iq.addElement('query', MCF_NS)

    if not xs.children or not xs.children[0].children: return

    for x in xs.children[0].children:
        m=x
        #z=x
    try: type = m['type']
    except: pass
    chat = xs['from']
    if type in ['chat','groupchat','normal']:
        for x in m.elements():
            if x.name == "body": body = x.__str__()
            
        if not MUC_FILT.has_key(chat): MUC_FILT[chat] = {}

        if not MUC_FILT[chat].has_key('traf'): MUC_FILT[chat]['traf'] = traf
        else: MUC_FILT[chat]['traf'] += traf
            
        jid = m['from']
        if hasattr(jid, 'count'):
            if jid.count('/'): jid = jid.split('/')[0]
        #jid = unicode(jid)

        if not jid in MUC_FILT[chat]: MUC_FILT[chat][jid]={'t':time.time(), 'm':body}
        else:
            if time.time() - MUC_FILT[chat][jid]['t']<1.8:
                i=msg_403(m, 'Too fast you send! limit 1.8 sec.')
                query.addRawXml(i.toXml())
                reactor.callFromThread(iq.send, xs['from'])
                return
            if MUC_FILT[chat][jid]['m']==body:
                i=msg_403(m, 'Your messages are very similar!')
                query.addRawXml(i.toXml())
                reactor.callFromThread(iq.send, xs['from'])
                return
            if body.isspace():
                i=msg_403(m, 'Your messages contains only spaces!')
                query.addRawXml(i.toXml())
                reactor.callFromThread(iq.send, xs['from'])
                return
            MUC_FILT[chat][jid]['m']=body
            MUC_FILT[chat][jid]['t']=time.time()
        if chat in MUC_FILT['fool'] and jid in MUC_FILT['fool'][chat]:
            i = xs_replace(m, random.choice(MCFILT_FOOL))
            query.addRawXml(i.toXml())
            reactor.callFromThread(iq.send, xs['from'])
            return
        if isinstance(body, unicode) or isinstance(body, str):
            if len(body)>500:
                i=msg_403(m, 'Very long Message!limit 500 symbols')
                query.addRawXml(i.toXml())
                reactor.callFromThread(iq.send, xs['from'])
                return
    elif type in ['available', None]:
        if not chat in MUC_FCON['member']: MUC_FCON['member'][chat]={}
        if chat in MUC_FILT['onlymemb'] and not jid in MUC_FCON['member'][chat]:
            i = xs_403(m)
            query.addRawXml(i.toXml())
            reactor.callFromThread(iq.send, xs['from'])
            return
        if not jid in MUC_FCON['member'][chat] and time.time() - MUC_FCON['t1']>60:
            MUC_FCON['member'][chat][jid]={}
            write_file(MFILT_WHITE, str(MUC_FCON['member']))
            MUC_FCON['t1']=time.time()
    query.addRawXml(m.toXml())
    #try: print iq.toXml()
    #except: pass
    reactor.callFromThread(iq.send, xs['from'])

def xs_403(m):
    i = domish.Element(('jabber:client', 'presence'))
    i['type'] = 'error'
    i['to']= m['from']
    i['from']=m['to']
    i['xml:lang'] = 'ru'
    i.addElement('x', 'http://jabber.org/protocol/muc')
    err = i.addElement('error')
    err['code']= '403'
    err['type']='auth'
    err.addElement('forbidden','urn:ietf:params:xml:ns:xmpp-stanzas')
    err.addElement('text','urn:ietf:params:xml:ns:xmpp-stanzas').addContent('Your presence is denied by muc-filt policy!')
    return i

def msg_403(m, text):
    body = None
    for x in m.elements():
        if x.name == 'body':
            try: body = x.__str__()
            except: pass
    ms = domish.Element(('jabber:client','message'))
    ms['to'] = m['from']
    ms['from'] = m['to']
    ms['type'] = 'error'
    ms.addElement("body", "jabber:client", body)
    err = ms.addElement('error')
    err['code']= '403'
    err['type']='auth'
    err.addElement('forbidden','urn:ietf:params:xml:ns:xmpp-stanzas')
    err.addElement('text','urn:ietf:params:xml:ns:xmpp-stanzas').addContent(text)
    return ms

def xs_replace(m, text):
    ms = domish.Element(('jabber:client','message'))
    ms['to'] = m['to']
    ms['from'] = m['from']
    ms['type'] = m['type']
    ms.addElement("body", "jabber:client", text)
    return ms

def mfilt_config(t, s, p):
    if not s[1] in GROUPCHATS: return
    if not p:
        rep=u'Конфигурация muc-filter:\n-сообщения >500 символов - блокировать,\n- сообщения чаще 1.8 сек. - блокировать,\n- одинаковые сообщения  - блокировать.'
        try: rep+=u'\nТраффик конференции по muc-filter :'+str(MUC_FILT[s[1]]['traf']//1024)+u' Кб.'
        except: pass
        reply(t, s, rep)
        return
    if p.count(' '):
        i=p.split()
        if i[0] == 'fool':
            if not s[1] in MUC_FILT['fool']: MUC_FILT['fool'][s[1]] = {}
            if not i[1] in MUC_FILT['fool'][s[1]]:
                MUC_FILT['fool'][s[1]][i[1]]={}
                write_file(MFILT, str(MUC_FILT))
                reply(t, s, u'ok!')
            else:
                del MUC_FILT['fool'][s[1]][i[1]]
                write_file(MFILT, str(MUC_FILT))
                reply(t, s, u'Удалил!')
        if i[0] == 'white':
            if not s[1] in MUC_FILT['onlymemb']:
                MUC_FILT['onlymemb'][s[1]] = {}
                write_file(MFILT, str(MUC_FILT))
                reply(t, s, u'ok!')
            else:
                del MUC_FILT['onlymemb'][s[1]]
                write_file(MFILT, str(MUC_FILT))
                reply(t, s, u'Отключил вход по белому списку!')


def load_mfilt_members():
    global MUC_FCON
    db=eval(read_file(MFILT_WHITE))
    MUC_FCON['member']=db.copy()

def load_mfilt_config():
    global MUC_FILT
    db=eval(read_file(MFILT))
    if not db:
        db=MUC_FILT.copy()
        write_file(MFILT, str(db))
    else: MUC_FILT=db.copy()


register_command_handler(mfilt_config, 'mfilt', ['все'], 20, 'Юзает специальное расширение http://jabber.ru/muc-filter, позволяющее фильтровать все сообщения и презенсы конференции через бота, до попадания их в public. Используются ключи: white - разрешает вход гостям только если они уже были в чате ранее, fool - добавление/удаление юзера в черный список, сообщения от него бот будет коверкать на свой лад. Команда без параметров выведет статистику.', 'mfilt', ['mfilt'])
register_stage0_init(load_mfilt_members)
register_stage0_init(load_mfilt_config)
register_iq_handler(iq_muc)
