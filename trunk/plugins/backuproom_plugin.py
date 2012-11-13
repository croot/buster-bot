#===istalismanplugin===
# /* coding: utf8 */

DEV_BACKUP_ROOMF = 'dynamic/backup_roomf.txt'

BACKUP_MUC = {}

db_file(DEV_BACKUP_ROOMF, dict)


def making_backup_muc_quest(c, muc, afl):
        packet = IQ(CLIENTS[c], 'get')
        packet['id'] = 'item'+str(random.randrange(1000, 9999))
        query = packet.addElement('query', 'http://jabber.org/protocol/muc#admin')
        i = query.addElement('item')
        i['affiliation'] = afl
        packet.addCallback(backup_muc_res, c, muc, afl)
        reactor.callFromThread(packet.send, muc)

def backup_muc_res(c, muc, afl, x):
        if x['type']=='result':
                query = element2dict(x)['query']
                query = [i.attributes for i in query.children if i.__class__==domish.Element]
                if not query: return
                db=eval(read_file(DEV_BACKUP_ROOMF))
                if not muc in db.keys():
                        db[muc]={'subject':'','info':'','outcast':[],'member':[],'admin':[],'owner':[],'last':time.time()}
                db[muc][afl].extend([x['jid'] for x in query])
                write_file(DEV_BACKUP_ROOMF, str(db))


def self_join_for_owner(g, n, a, b, c):
        if a==u'owner' and n==get_bot_nick(g):
                packet = IQ(CLIENTS[c], 'get')
                packet['id'] = 'item'+str(random.randrange(1000, 9999))
                query = packet.addElement('query', 'http://jabber.org/protocol/muc#admin')
                i = query.addElement('item')
                i['affiliation'] = 'owner'
                packet.addCallback(backup_muc_answ, c, g)
                reactor.callFromThread(packet.send, g)
        else:
                if time.time()-INFO['start']<300: return
                if g in GROUPCHATS and get_bot_nick(g) in GROUPCHATS[g] and GROUPCHATS[g][get_bot_nick(g)]['ismoder']:
                        if g in BACKUP_MUC.keys() and time.time()-BACKUP_MUC[g]<(86400*3):
                                return
                        else:
                                db=eval(read_file(DEV_BACKUP_ROOMF))
                                if not g in BACKUP_MUC.keys() and not g in db.keys():
                                        db[g]={'subject':'','info':'','outcast':[],'member':[],'admin':[],'owner':[],'last':time.time()}
                                        write_file(DEV_BACKUP_ROOMF, str(db))
                                else:
                                        try: db[g]['last']=time.time()
                                        except: db[g]={'subject':'','info':'','outcast':[],'member':[],'admin':[],'owner':[],'last':time.time()}
                                        write_file(DEV_BACKUP_ROOMF, str(db))
                                BACKUP_MUC[g]=time.time()
                                for x in ['owner','admin','member','outcast']:
                                        making_backup_muc_quest(c, g, x)
                                packet = IQ(CLIENTS[c], 'get')
                                packet.addElement('query', 'http://jabber.org/protocol/disco#info')
                                packet.addCallback(back_up_info_res, g)
                                reactor.callFromThread(packet.send, g)
                                        
def back_up_info_res(g, x):
        if x['type']=='result':
                db=eval(read_file(DEV_BACKUP_ROOMF))
                query = element2dict(x)['query']
                if query.children:
                        for x in query.children:
                                if x.uri == 'jabber:x:data':
                                        try:
                                                db[g]['info'] = unicode(getTag(x.children[1],'value'))
                                                write_file(DEV_BACKUP_ROOMF, str(db))
                                        except: pass


def backup_muc_answ(c, g, x):
        if x['type']=='result':
                query = element2dict(x)['query']
                query = [i.attributes for i in query.children if i.__class__==domish.Element]
                if not query:
                        return
                if len(query)==1:
                        msg(c, g, u'Запущена программа восcтановления комнаты...\nПоиск резервной базы...')
                        time.sleep(2)
                else: return
                inf, enab = '', 1
                try: db=eval(read_file(DEV_BACKUP_ROOMF))
                except: db = {}
                if not g in db.keys():
                        enab = 0
                        msg(c, g, u'База не найдена! owner, admin, member, outcast листы не будут восставнолены!')
                        inf = 'BACKUP_BUSTER_ROOM'
                else:
                        inf = db[g]['info']
                        
                msg(c, g, u'Делаю комнату постоянной!')
                iq = IQ(CLIENTS[c], 'set')
                iq['to'] = g
                iq['id'] = str(random.randrange(0,1500))
                query = iq.addElement('query', 'http://jabber.org/protocol/muc#owner')
                x = query.addElement('x', 'jabber:x:data')
                x.__setitem__('type', 'submit')
                f = x.addElement('field')
                f.__setitem__('var', 'FORM_TYPE')
                f.addElement('value',content='http://jabber.org/protocol/muc#roomconfig')
                f2 = x.addElement('field')
                f2.__setitem__('var', 'muc#roomconfig_persistentroom')
                f2.addElement('value',content='1')
                f3 = x.addElement('field')
                f3.__setitem__('var', 'muc#roomconfig_roomdesc')
                f3.addElement('value',content=inf)
                #print iq.toXml()
                reactor.callFromThread(iq.send, g)
                clc = 0
                if enab:
                        sj = [None, g, None, c]
                        if 'owner' in db[g]:
                                for x in db[g]['owner']:
                                        clc+=1
                                        moderate(sj, 'jid', x, 'affiliation', 'owner')
                        if 'admin' in db[g]:
                                for x in db[g]['admin']:
                                        if x == c:
                                                continue
                                        clc+=1
                                        moderate(sj, 'jid', x, 'affiliation', 'admin')
                        if 'member' in db[g]:
                                for x in db[g]['member']:
                                        if x == c:
                                                continue
                                        clc+=1
                                        moderate(sj, 'jid', x, 'affiliations', 'memeber')
                        if 'outcast' in db[g]:
                                for x in db[g]['outcast']:
                                        if x == c:
                                                continue
                                        clc+=1
                                        moderate(sj, 'jid', x, 'affiliation', 'outcast')
                        if 'subject' in db[g] and len(db[g]['subject'])>2:
                                send_subject(c, g, db[g]['subject'])

                if clc:
                        msg(c, g, u'Восстановлено JID Affiliations '+str(clc))

register_join_handler(self_join_for_owner)


def msg_subject(r, t, s, p):
        if not s[2] and s[1] in GROUPCHATS:
                db = eval(read_file(DEV_BACKUP_ROOMF))
                if not s[1] in db.keys():
                        db[s[1]]={'subject':'','info':'','outcast':[],'member':[],'admin':[],'owner':[],'last':time.time()}
                try: db[s[1]]['subject'] = unicode(r.subject)
                except: return
                write_file(DEV_BACKUP_ROOMF, str(db))

register_message_handler(msg_subject)


def hnd_set_subject(t, s, p):
        if not p or not s[1] in GROUPCHATS: return
        send_subject(s[3], s[1], p)


def send_subject(c, muc, body):
        message = domish.Element(('jabber:client','message'))
        message["type"] = "groupchat"
        message["to"] = muc
        message.addElement("subject", "jabber:client", body)
        reactor.callFromThread(dd, message, CLIENTS[c])


def muc_backup_init(*something):
        global BACKUP_MUC
        global DEV_BACKUP_ROOMF
        if not BACKUP_MUC:
                db=eval(read_file(DEV_BACKUP_ROOMF))
                for x in db.keys():
                        if 'time' in db[x]:
                                BACKUP_MUC[x]=db[x]['time']

register_stage0_init(muc_backup_init)
                
def get_room_backup_status(t, s, p):
        if not p and s[1] in GROUPCHATS:
                p=s[1]
        else:
                reply(t, s, u'?')
                return
        rep, p = '', p.lower()
        db = eval(read_file(DEV_BACKUP_ROOMF))
        if not p in db.keys():
                reply(t, s, u'Бэкап комнаты отсутствует')
                return
        rep+=u'Бэкап комнаты создан '+timeElapsed(time.time()-db[p]['last'])+u' назад.\n'
        rep+=u'Топик '+db[p]['subject'][:20]+'... '+str(len(db[p]['subject']))+u' символов.\n'
        rep+=u'Информация о комнате '+db[p]['info']+'\n'
        rep+=u'Овнеры '+str(len(db[p]['owner']))+'\n'
        rep+=u'Админы '+str(len(db[p]['admin']))+'\n'
        rep+=u'Мемберы '+str(len(db[p]['member']))+'\n'
        rep+=u'Изгои '+str(len(db[p]['outcast']))+'\n'
        reply(t, s, rep)
        

register_command_handler(get_room_backup_status, 'backup_status', ['все'], 10, 'Выводит информацию по резервному копированию команты.', 'backup_status', ['backup_status'])        

