# -*- coding: utf-8 -*-


MUC_FILT = {'fool':{},'onlymemb':{},'newbie':{}}

MUC_FCON = {'member':{},'t1':0}

MFILT = 'dynamic/mucfilt.txt'

MFILT_WHITE = 'dynamic/mucfilt_members.txt'

db_file(MFILT, dict)
db_file(MFILT_WHITE, dict)

MCFILT_FOOL = [u'люблю сосать хуи',u'я сегодня на помойке почти новый вебратор нашол',u'пойду ща есть какашки',u'люблю обмазывать себя какашками',u'пук']

MCF_NS = 'http://jabber.ru/muc-filter'



def iq_muc(xs, cljid):
    
    if xs['type']!='set': return
    
    for query in xs.elements(): xmlns = query.uri
    
    if xmlns != MCF_NS: return

    #global z

    xmlns, type, body, traf, jid, m = None, None, None, 0, None, None

    try: traf = sys.getsizeof(xs.toXml())
    except: pass

    #print 'IN+'
    #print xs.toXml()
    
    iq = IQ(CLIENTS[cljid], 'result')
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
    ik = ''
    if type in ['chat','groupchat','normal']:
        for x in m.elements():
            if x.name == "body": body = x.__str__()
            
        if not MUC_FILT.has_key(chat): MUC_FILT[chat] = {}

        if not MUC_FILT[chat].has_key('traf'): MUC_FILT[chat]['traf'] = traf
        else: MUC_FILT[chat]['traf'] += traf
            
        jid = m['from']
        #print m['from'],'G+'
        try:
            if 'MAFIA' in globals().keys() and 'MAFIA_CHATS' in globals().keys():
                if chat in MAFIA_CHATS and get_true_jid(jid) in MAFIA:
                    if not MAFIA[get_true_jid(jid)]['voice']:
                        i=msg_403(m, 'You are die!')
                        query.addRawXml(i.toXml())
                        reactor.callFromThread(iq.send, xs['from'])
                        return
                    
                    if type==u'groupchat' and not body.split()[0].lower() in COMMANDS.keys():
                        ik = [MAFIA[x]['nick'] for x in MAFIA.keys() if x==jid]
                        if not ik:
                            ik = [x for x in GROUPCHATS[chat].keys() if GROUPCHATS[chat][x]['jid']==jid]
                        if ik:
                            mafia_msg(m, 'public', [chat+'/'+ik[0], chat, ik[0], cljid], body)
                            return
                    
                    if MAFIA_SES['hod']>=1 and m['type']=='chat' and m['to']!=chat+'/'+get_bot_nick(chat):
                        i=msg_403(m, 'Private message has been locked!')
                        query.addRawXml(i.toXml())
                        reactor.callFromThread(iq.send, xs['from'])
                        return

                    
                    
                    


            if chat=='mafia_online@conference.jabber.ru' and 'MAFC' in globals().keys():
                if MAFC_SYS['hod']>=1 and m['type']=='chat' and m['to']!='mafia_online@conference.jabber.ru/'+get_bot_nick(chat):
                    i=msg_403(m, 'Private message has been locked!')
                    query.addRawXml(i.toXml())
                    reactor.callFromThread(iq.send, xs['from'])
                    return
                for x in GROUPCHATS[chat]:
                    if GROUPCHATS[chat][x]['jid']==jid:
                        if x in MAFC.keys() and MAFC[x]['voice']==0:
                            i=msg_403(m, 'You are die!')
                            query.addRawXml(i.toXml())
                            reactor.callFromThread(iq.send, xs['from'])
                            return
                nnn=[x for x in GROUPCHATS[chat] if GROUPCHATS[chat][x]['jid']==jid]
                if body.isdigit() and nnn:
                    dd={'chat':'private','groupchat':'public'}
                    tt=m['type']
                    if tt in dd:
                        tt=dd[tt]
                    mfc_message(None, tt, [chat+'/'+nnn[0], chat, nnn[0], cljid], body)
                    return

        except: pass
        #jid = unicode(jid)
        if hasattr(jid, 'count'):
            if jid.count('/'): jid = jid.split('/')[0]

        if not jid in MUC_FILT[chat]: MUC_FILT[chat][jid]={'t':time.time(), 'm':body}
        else:
            if time.time() - MUC_FILT[chat][jid]['t']<1.8:
                i=msg_403(m, 'Too fast you send! limit 1.8 sec.')
                query.addRawXml(i.toXml())
                reactor.callFromThread(iq.send, xs['from'])
                return
            if MUC_FILT[chat][jid]['m']==body and not body.split()[0].lower() in COMMANDS.keys():
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
        if isinstance(body, basestring):
            if len(body)>500:
                i=msg_403(m, 'Very long Message!limit 500 symbols')
                query.addRawXml(i.toXml())
                reactor.callFromThread(dd, xs['from'],)
                return
    elif type in ['available', None]:
        #print m['from']
        
        if not chat in MUC_FCON['member']: MUC_FCON['member'][chat]={}
        try:
            pz = m['to']
            pz = pz.split('/')[1]
            if [x for x in pz if unicodedata.category(x)=='Lo'] or len(pz)>21:
                i = xs_403(m)
                query.addRawXml(i.toXml())
                reactor.callFromThread(iq.send, xs['from'])
                return
        except: pass
        if chat in MUC_FILT.get('newbie',{}) and not jid in MUC_FCON['member'][chat]:
            if time.time()-MUC_FILT['newbie'][chat]['t']<1800 and MUC_FILT['newbie'][chat]['n']>5:
                i = xs_403(m)
                query.addRawXml(i.toXml())
                reactor.callFromThread(iq.send, xs['from'])
                return
            MUC_FILT['newbie'][chat]['n']+=1
            MUC_FILT['newbie'][chat]['t']=time.time()
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
        rep=u'Конфигурация muc-filter:\n-сообщения >500 символов - блокировать,\n- сообщения чаще 1.8 сек. - блокировать,\n- одинаковые сообщения  - блокировать,\nдлинные ники и ники на китайском - блокировать.'
        try: rep+=u'\nТраффик конференции по muc-filter :'+str(MUC_FILT[s[1]]['traf']//1024)+u' Кб.'
        except: pass
        reply(t, s, rep)
        return
    if p.count(' '):
        i=p.split()
        if i[0] == 'fool':
            if not s[1] in MUC_FILT['fool']: MUC_FILT['fool'][s[1]] = {}
            if not i[1] in MUC_FILT['fool'][s[1]] or i[1]==u'1':
                MUC_FILT['fool'][s[1]][i[1]]={}
                write_file(MFILT, str(MUC_FILT))
                reply(t, s, u'ok!')
            else:
                del MUC_FILT['fool'][s[1]][i[1]]
                write_file(MFILT, str(MUC_FILT))
                reply(t, s, u'Удалил!')
        if i[0] == 'white':
            if not s[1] in MUC_FILT['onlymemb'] or i[1]==u'1':
                MUC_FILT['onlymemb'][s[1]] = {}
                write_file(MFILT, str(MUC_FILT))
                reply(t, s, u'ok!')
            else:
                del MUC_FILT['onlymemb'][s[1]]
                write_file(MFILT, str(MUC_FILT))
                reply(t, s, u'Отключил вход по белому списку!')
        if i[0] == 'newbie':
            if not 'newbie' in MUC_FILT:
                MUC_FILT['newbie']={}
            if not s[1] in MUC_FILT['newbie'] or i[1]==u'1':
                MUC_FILT['newbie'][s[1]] = {'n':0,'t':0}
                write_file(MFILT, str(MUC_FILT))
                reply(t, s, u'ok!')
            else:
                del MUC_FILT['newbie'][s[1]]
                write_file(MFILT, str(MUC_FILT))
                reply(t, s, u'Отключил лимит новичков!')
    else:
        reply(t, s, u'Неверный синтаксис!\nПример: mfilt white 1')


def load_mfilt_members(cljid):
    global MUC_FCON
    db=eval(read_file(MFILT_WHITE))
    MUC_FCON['member']=db.copy()

def load_mfilt_config(cljid):
    global MUC_FILT
    db=eval(read_file(MFILT))
    if not db:
        db=MUC_FILT.copy()
        write_file(MFILT, str(db))
    else: MUC_FILT=db.copy()


register_command_handler(mfilt_config, 'mfilt', ['все'], 20, 'Юзает специальное расширение http://jabber.ru/muc-filter, позволяющее фильтровать все сообщения и презенсы конференции через бота, до попадания их в public. Используются ключи: newbie - лимит новичков, не более 5-ти за пол часа, white - разрешает вход гостям только если они уже были в чате ранее, fool - добавление/удаление юзера в черный список, сообщения от него бот будет коверкать на свой лад. Команда без параметров выведет статистику.', 'mfilt', ['mfilt','mfilt white 1'])
register_stage0_init(load_mfilt_members)
register_stage0_init(load_mfilt_config)
register_iq_handler(iq_muc)
