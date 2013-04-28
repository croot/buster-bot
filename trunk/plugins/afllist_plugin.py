#===istalismanplugin===
# -*- coding: utf-8 -*-

def handler_spisok_iq(type, source, parameters):
        if not source[1] in GROUPCHATS: return
        if not parameters:
                reply(type,source,u'Выберите ключ: \"овнеры, админы, мемберы, изгои\"!')
                return
        body=parameters.lower()
	nick = source[2]
	groupchat=source[1]
	afl=''
	if body.count(u'овнеры')>0:
                afl='owner'
        elif body.count(u'админы')>0:
                afl='admin'
        elif body.count(u'мемберы')>0:
                afl='member'
        elif body.count(u'изгои')>0:
                afl='outcast'
        if afl=='':
                return
        packet = IQ(CLIENTS[source[3]], 'get')
        packet['id'] = 'item'+str(random.randrange(1000, 9999))
        query = packet.addElement('query', 'http://jabber.org/protocol/muc#admin')
        i = query.addElement('item')
        i['affiliation'] = afl
        packet.addCallback(handler_sp_answ, type, source)
        reactor.callFromThread(packet.send, groupchat)


def handler_sp_answ(type, source, x):
        rep, n = '', 0
        if x['type']=='result':
                query = element2dict(x)['query']
                query = [i.attributes for i in query.children if i.__class__==domish.Element]
                if not query:
                        reply(type, source, u'Пусто!')
                        return
                for c in query:
                        n+=1
                        rep+=str(n)+') '+c['jid']+'\n'
        else:
                reply(type,source,u'облом!')
                return
        if type in ['chat','public']:
                reply(type, source, u'Смотри в привате! (всего '+str(n)+')')
	reply('private', source, u'Всего найдено в списке '+str(n)+':\n'+rep)
	
register_command_handler(handler_spisok_iq, 'список', ['админ','мук','все'], 20, 'Показывает в зависимости от выбранного ключа список админов,овнеров,мемберов или забаненных конфы.', 'список <ключ>', ['список овнеры','список изгои','список мемберы','список админы'])


def hnd_getold_list(type, source):
        if check_file(source[1],'banlist.txt'):
                file='dynamic/'+source[1]+'/banlist.txt'
                txt=eval(read_file(file))
                n=0
                if txt:
                        hnd_banl_packet(source, 'outcast', txt)
                        reply(type,source,u'Восстановленно банов: '+unicode(len(txt)))

def any_copy_banl(type,source,parameters):
        if len(parameters)>50:
                return
        if not parameters.count(' '):
                reply(type,source,u'укажите адрес чата для копирования!')
                return
        chat=parameters.split()[1]
        try:
                file='dynamic/'+chat+'/banlist.txt'
                txt=eval(read_file(file))
        except:
                reply(type,source,u'база '+chat+u' не найдена!')
                return
        if not txt:
                reply(type,source,u'база '+chat+u' пуста!')
                return
        n=0
        if txt:
                hnd_banl_packet(source, 'outcast', txt)
        reply(type,source,u'Bсего скопировано банов в банлист конференции: '+str(len(txt)))
                                
def hnd_banl(type, source, parameters):
        if source[1] not in GROUPCHATS:
                return
        body=parameters.lower()
	nick = source[2]
	groupchat=source[1]
        if body.count(u'вернуть'):
                hnd_getold_list(type,source)
                return
        if body.count(u'копировать'):
                any_copy_banl(type,source,parameters)
                return
        if body==u'бд':
                try:
                        fp = eval(read_file('dynamic/'+source[1]+'/banlist.txt'))
                        reply(type, source, u'В базе '+str(len(fp))+':\n'+'\n'.join(fp.keys()))
                except: reply(type, source, u'Базы не создано!')
                return
	afl='outcast'
	packet = IQ(CLIENTS[source[3]], 'get')
        packet['id'] = 'item'+str(random.randrange(1000, 9999))
        query = packet.addElement('query', 'http://jabber.org/protocol/muc#admin')
        i = query.addElement('item')
        i['affiliation'] = afl
        packet.addCallback(handler_banlist_answ, type, source, parameters)
        reactor.callFromThread(packet.send, groupchat)


def handler_banlist_answ(type, source, parameters, x):
        jid, serv = [], []
        if x['type']=='result':
                query = element2dict(x)['query']
                query = [i.attributes for i in query.children if i.__class__==domish.Element]
                jid = [i['jid'] for i in query if jid.count('@')]
                serv = [i['jid'] for i in query if not jid.count('@')]
                all = jid + serv
                if not all:
                        reply(type,source,u'Пусто!')
                        return
                if check_file(source[1],'banlist.txt'):
                        file='dynamic/'+source[1]+'/banlist.txt'
                        txt=eval(read_file(file))
                        if parameters.count(u'серв'):
                                if len(serv)>0:
                                        write_file(file, str(serv))
                                        reply(type,source,u'Всего сохраненено серверов: '+str(len(serv)))
                                        return
                                else:
                                        reply(type,source,u'Серверов не найдено в бан-листе!')
                                        return
                        elif parameters.count(u'унбан'):
                                if len(all)==0:
                                        reply(type, source, u'Нету банов!')
                                        return
                                hnd_banl_packet(source, 'none', all)
                                time.sleep(1)
                                reply(type,source,u'Снято банов: '+str(len(all)))
                                return
                        else:
                                if len(all)==0: return
                                write_file(file, str(all))
                                reply(type,source,u'Сохранены все баны: '+str(len(all)))
                                return

                        
                        
                else:
                        reply(type,source,u'Oблом!')
                        return
        else:
                reply(type,source,u'Oблом!')
                return
        


def hnd_banl_packet(s, afl, jid):
    packet = IQ(CLIENTS[s[3]], 'set')
    if isinstance(jid, dict):
            jid = jid.keys()
    query = packet.addElement('query', 'http://jabber.org/protocol/muc#admin')
    if len(jid)>51:
        a, b = 0, 50
        for x in range(len(jid)/50+1):
            print len(jid[a:b:])
            drj_afl(s, afl, jid[a:b:])
            a+= 50
            b+= 50
            time.sleep(3.5)
        return
    for x in jid:
        i = query.addElement('item')
        i['jid'] = x
        i['affiliation'] = afl
        if afl!='none':
            i.addElement('reason').addContent(get_bot_nick(s[1])+u': reserve copy')
        if sys.getsizeof(packet)>62000:
            break
    #d = Deferred()
    #packet.addCallback(d.callback)
    reactor.callFromThread(packet.send, s[1])
    #return d

	
register_command_handler(hnd_banl, '!банлист', ['все','админ'], 20, 'Работа с банлистом конференции.\nБез ключа просто сохранит все баны в базе бота.\nКлюч серв - сохранит в базе только серверы\nКлюч унбан - снимет все баны конференции.\nКлюч вернуть - вернет баны сохраненные в базе;\nкопировать - скопирует баны из базы указанной конференции;\nбд - просмотр базы.', '!банлист <ключ>', ['!банлист','!банлист серв','!банлист унбан','!банлист копировать cool@conference.jabber.ru'])
