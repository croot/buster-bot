#===istalismanplugin===
# -*- coding: utf-8 -*-

MF_WHO_JOIN = {}

MAF_ADMINS = [u'tengiz@mafiozo.in',u'cool@mafiozo.in',u'40tman@qip.ru',u'apostol@xmpp.ru',u'krasotylya@jabber.ru',u'progmaster90@xmpp.kz']

MAF_TEMP_BAN = {'f':[],'t':{},'new':0,'mail':1}

BAN_MEMB_FILE = 'dynamic/ban_memb_mf.txt'
MODEM_FILE = 'dynamic/modemf.txt'

db_file(BAN_MEMB_FILE, dict)
db_file(MODEM_FILE, dict)

try:
    M_MODE = eval(read_file(MODEM_FILE))
except:
    pass

TMAIL_LIST = {}

import operator

db_file('dynamic/mfcntspeak.txt', dict)

GLOB_CANTSPEAKM = eval(read_file('dynamic/mfcntspeak.txt'))

def mafia_can_speak(jid):
    global GLOB_CANTSPEAKM
    if jid in GLOB_CANTSPEAKM.keys():
        if GLOB_CANTSPEAKM[jid]>time.time():
            return (False, u'Вы сможете писать в чат через:'+timeElapsed(GLOB_CANTSPEAKM[jid]-time.time()))
    return (True, str())

def hnd_maf_admin(raw, type, source, parameters):
    global BAN_MEMB_FILE
    global MODEM_FILE
    one = 1
    def tell_all_mad(jid, msg):
        try:
            for x in MAF_ADMINS:
                if x!=jid:
                    msg(source[3], x, msg)
        except: pass
    jid = get_true_jid(source)
    rep = ''
    if jid in MAF_ADMINS:
        if parameters==u'#0':
            rep+=u'#1 - список пользователей в игре,\n'
            rep+=u'#2 - список пользователей посещавших игру за время работы бота,\n'
            rep+=u'#3 - остановка игры,\n'
            rep+=u'#4 - сообщение в игру,\n'
            rep+=u'#5 - предупреждение игроку: id текст,\n'
            rep+=u'#6 - бан игрока до рестарта бота: id причина,\n'
            rep+=u'#7 - кик игрока id,\n'
            rep+=u'#8 - временная блокировка игрока: id часы,\n'
            rep+=u'#9 - временный запрет входа юзеров не из базы,\n'
            rep+=u'#10 - вывод правил в общий чат,\n'
            rep+=u'#11 - изменить ник id ник,\n'
            rep+=u'#12 - запуск бастера,\n'
            rep+=u'#13 - достает из бана юзера по jid,\n'
            rep+=u'#14 - добавляет новость,\n'
            rep+=u'#15 - постоянный бан: id|JID|UIN\n'
            rep+=u'#16 - разрешает вход новому юзеру, используется номер из списка заявлений.\n'
            rep+=u'#17 - просмотр списка заявлений\n'
            rep+=u'#18 - запрет на сообщения игрока id часы причина, без указ.причины автоматически за ругань\n'
            rep+=u'#19 - достает из постоянного бана user\n'
            rep+=u'#20 - список постоянного бана\n'
            rep+=u'#21 - установка режима игры, ключи - f, 0 (f - новичек лишен права голоса, 0 - нормальный режим)\n'
            rep+=u'#22 - восстановление JID-а пользователя, со старого будет снят опыт, синтаксис: <старый JID> <новый JID>'
            #rep+=u'#18 - включает/отключает допуск MAil.ru'
            reply(type, source, rep)
            return
        if parameters==u'#10':
            pr=u"Следущие действия рассцениваються как нарушение правил игры:\n1.Сознательный подыгрыш или проигрыш другим персонажам в целях набора очков.\n2.Передача ценной игровой информации вне общего чата партии.\n3.Действия (бездействия), противоречащие логике партии и здравому смыслу, совершённые в силу неигровых мотивов (недовольство ролью, безразличное отношение к исходу партии и т.п.), которые послужили причиной ничьей или поражения своей стороны.\n4.Сообщение своей роли в общий чат, когда это сообщение не является одним из элементов тактики, что подтверждается разумным смыслом и логикой партии.\n5.Предвзятое и нескрываемое негативное отношение одного игрока/группы игроков к другому, ругань, оскорбления."
            mafia_bot(pr)
            reply(type, source, u'ok')
            return
        if parameters==u'#12':
            reply(type, source, u'ok')
            mf_buster()
            return
        if parameters==u'#1':
            if globals().has_key('MAFIA'):
                if len(MAFIA)==0:
                    reply(type, source, u'Никого нет в игре')
                    return
                rep=''
                for x in MAFIA:
                    chat=''
                    if MAFIA[x]['source'][1] in GROUPCHATS:
                        chat=MAFIA[x]['source'][1]
                    rep+=x+' '+unicode(MAFIA[x]['nick'])+' '+' '.join(MAFIA[x]['remote'])+' '+chat+';\n'
                reply(type, source, rep)
                return
        if parameters==u'#2':
            list = sorted(MF_WHO_JOIN.iteritems(), key=operator.itemgetter(1))
            list.reverse()
            rep=''
            for x in list:
                rep+=x[0]+' '+datetime.datetime.fromtimestamp(x[1]).strftime('%Y-%m-%d %H:%M:%S')+'\n'
            if not rep or rep.isspace():
                reply(type, source, u'статистики нет')
                return
            reply(type, source, rep)
            return
        if parameters==u'#9':
            rep=u'Включена'
            if MAF_TEMP_BAN['new']:
                MAF_TEMP_BAN['new']=0
                rep=u'Отключена'
            else:
                MAF_TEMP_BAN['new']=1
            reply(type, source, rep+u' временная блокировка юзеров не с базы!')
            mafia_bot(':: '+rep+u' временная блокировка юзеров не с базы!::')
            return
        if parameters==u'#3':
            mafia_bot(u':: Приносим свои извенения, партия остановлена адмистратором!::')
            MAFIA_SES['start']=0
            MAFIA.clear()
            for x in MAF_ADMINS:
                if x!=jid:
                    msg(source[3], x,u'Партия была остановлена '+jid)
            reply(type, source, u'сча остановим!')
            return
        if parameters==u'#20':
            reply(type, source, ', '.join(eval(read_file(BAN_MEMB_FILE)).keys()))
        if parameters==u'#17':
            i=str()
            for x in TMAIL_LIST.keys():
                i+=str(TMAIL_LIST.keys().index(x)+1)+') '+x+'\n'
            reply(type, source, (i if i else u'empty list'))
            return
        if parameters.count(' '):
            s=parameters.split()
            tim=0
            if s[0]==u'#22':
                if len(s)<3:
                    reply(type, source, u'В параметрах нужно указать старый и новый жид через пробел!')
                    return
                if s[1].lower() in [x.lower() for x in MAFIA_LEVEL.keys()]:
                    if s[1].lower() ==  s[2].lower():
                        reply(type, source, u'Ну и нагуя?')
                        return
                    if s[2].isdigit() or (s[2].count('@') and s[2].count('.')):
                        MAFIA_LEVEL[s[2]] =  MAFIA_LEVEL[s[1]].copy()
                        for x in MAFIA_LEVEL[s[1]]:
                            if x==u'all':
                                MAFIA_LEVEL[s[1]][x] = 10
                            else:
                                MAFIA_LEVEL[s[1]][x] = 0
                        write_file('dynamic/mafia_level.txt', str(MAFIA_LEVEL))
                        mafia_bot(u'* Пользователь '+s[1]+u' клонирован в '+s[2])
                        time.sleep(1.5)
                        reply(type, source, u'ok')
                        return
                else:
                    reply(type, source, s[1]+u' не найден в списке пользователей!')
                    return
            if s[0]==u'#18':
                if len(s)<2: return
                try:
                    reason = s[3]
                except:
                    reason = u'Ругань, оскорбления запрещены!'
                for x in MAFIA.keys():
                    if str(MAFIA[x]['id'])==s[1]:
                        tim=int(s[2])*3600
                        tim=time.time()+tim
                        GLOB_CANTSPEAKM[x]=tim
                        mafia_bot(u'* Игрок '+unicode(MAFIA[x]['nick'])+u' лишен права писать в общий чат на '+s[2]+u' часов : '+reason)
                        reply(type, source, u'ok')
                        write_file('dynamic/mfcntspeak.txt', str(GLOB_CANTSPEAKM))
                        return
            if s[0]==u'#21' and s[1] in ['f','0']:
                global M_MODE
                D = {'f':u'Пукающий новичок'}
                if s[1]=='0':
                    M_MODE = {}
                    reply(type, source, u'Установлен режим Norma')
                else:
                    M_MODE[s[1]] = {}
                    reply(type, source, u'Установлен режим '+D[s[1]])
                write_file(MODEM_FILE, str(M_MODE))
                return
            if s[0]==u'#16':
                if s[1].isgidit() and len(TMAIL_LIST)+1<=int(s[1]):
                    MAFIA_LEVEL[TMAIL_LIST.keys()[int(s[1])+1]]={}
                    try:
                        msg('mafia_bot@jabber.cz',TMAIL_LIST.keys()[int(s[1])+1],u'Вам открыт вход в игру мафия до рестарта бота!Заходите!')
                        del TMAIL_LIST[TMAIL_LIST.keys()[int(s[1])+1]]
                    except:
                        pass
                    reply(type, source, u'ok')
                    return
                else:
                    reply(type, source, u'Некорректные данные!')
                    return
            if s[0]==u'#14':
                parameters=parameters.replace('#14','')
                try: MAF_NEWS['body']==parameters
                except: pass
                reply(type, source, u'ok')
                return
            if s[0]==u'#4':
                parameters=parameters.replace('#4','')
                mafia_bot(u'Сообщение от Admin:\n'+parameters)
                return
            if s[0]==u'#5':
                i=''
                if len(s)>=3:
                    i=' '.join(s[2:])
                    for x in MAFIA.keys():
                        if str(MAFIA[x]['id'])==s[1]:
                            mafia_bot(u'* Игрок '+unicode(MAFIA[x]['nick'])+u' предупрежден, причина '+i)
                            reply(type, source, u'ok')
                            return
            if s[0]==u'#19':
                db = eval(read_file(BAN_MEMB_FILE))
                if s[1] in db.keys():
                    del db[s[1]]
                    write_file(BAN_MEMB_FILE, str(db))
                    reply(type, source, u'ok')
                    try: MAF_TEMP_BAN['f'].remove(s[1])
                    except: pass
                    DBMFBAN_EVAL = db
                    try: mafia_bot(s[1][:5]+u'.. был разбанен!')
                    except: pass
                else:
                    reply(type, source, u'Таких нет в бане!')
                    return
            if s[0]==u'#15':
                
                db = eval(read_file(BAN_MEMB_FILE))
                if s[1].isdigit() and len(s[1])<3:
                    for x in MAFIA.keys():
                        if str(MAFIA[x]['id'])==s[1]:
                            db[x]={}
                            write_file(BAN_MEMB_FILE, str(db))
                            reply(type, source, u'ok')
                            mafia_bot(u'* Игрок '+unicode(MAFIA[x]['nick'])+u' забанен вовеки')
                            MAF_TEMP_BAN['f'].append(x)
                            tell_all_mad(jid, x+u' забанен '+jid)
                            del MAFIA[x]
                            
                else:
                    db[s[1]]={}
                    write_file(BAN_MEMB_FILE, str(db))
                    MAF_TEMP_BAN['f'].append(s[1])
                    reply(type, source, u'ok')
                    if s[1] in MAFIA.keys():
                        del MAFIA[s[1]]
                    tell_all_mad(jid, s[1]+u' забанен '+jid)
                    return
                    
            if s[0]==u'#6':
                i=''
                if len(s)>=3:
                    i=' '.join(s[2:])
                    for x in MAFIA.keys():
                        if str(MAFIA[x]['id'])==s[1]:
                            mafia_bot(u'* Игрок '+unicode(MAFIA[x]['nick'])+u' забанен, причина '+i)
                            MAF_TEMP_BAN['f'].append(x)
                            for c in MAF_ADMINS:
                                if c!=jid:
                                    msg(source[3],c,x+u' был забанен '+jid)
                            del MAFIA[x]
                            reply(type, source, u'ok')
                            return
            if s[0]==u'#7':
                i=''
                if len(s)==2:
                    #i=' '.join(s[2:])
                    for x in MAFIA.keys():
                        if str(MAFIA[x]['id'])==s[1]:
                            mafia_bot(u'* Игрок '+unicode(MAFIA[x]['nick'])+u' был выкинут из партии ')
                            del MAFIA[x]
                            reply(type, source, u'ok')
                            return
            if s[0]==u'#8':
                tim=0
                if len(s)==3:
                    if not s[2].isdigit():
                        return
                    tim=int(s[2])*3600
                    tim=time.time()+tim
                    for x in MAFIA.keys():
                        if str(MAFIA[x]['id'])==s[1]:
                            mafia_bot(u'* Игрок '+unicode(MAFIA[x]['nick'])+u' лишен права заходить в игру на '+s[2]+u' часов.')
                            MAF_TEMP_BAN['t'][x]={}
                            MAF_TEMP_BAN['t'][x]=tim
                            del MAFIA[x]
                            for c in MAF_ADMINS:
                                if c!=jid:
                                    msg(source[3],c,x+u' был забанен '+jid)
                            reply(type, source, u'ok')
                            return
            if s[0]==u'#13':
                n=0
                if s[1] in MAF_TEMP_BAN['t']:
                    n=1
                    del MAF_TEMP_BAN['t'][s[1]]
                if s[1] in MAF_TEMP_BAN['f']:
                    MAF_TEMP_BAN['f'].remove(s[1])
                    n=1
                if not n:
                    reply(type, source, u'нет такого!')
                else:
                    reply(type, source, u'ок')
            if s[0]==u'#11':
                i=''
                if len(s)>=3:
                    i=' '.join(s[2:])
                    for x in MAFIA.keys():
                        if str(MAFIA[x]['id'])==s[1]:
                            try: mafia_bot(u'* '+unicode(MAFIA[x]['nick'])+u' теперь известен как '+i)
                            except: pass
                            MF_REPLACE[x]=i
                            db=eval(read_file('dynamic/mf_replace.txt'))
                            db[x]={}
                            db[x]=i
                            write_file('dynamic/mf_replace.txt',str(db))
                            MAFIA[x]['nick']=i
                            reply(type, source, u'ok')
                            return

try: DBMFBAN_EVAL = eval(read_file(BAN_MEMB_FILE))
except: DBMFBAN_EVAL = {}


def mafia_check(jid):
    global TMAIL_LIST
    global DBMFBAN_EVAL
    MF_WHO_JOIN[jid]=time.time()
    if MAF_TEMP_BAN['mail']:
        if jid and jid.count('mrim') and len(re.findall('[0-9]',jid))>2:
            if not jid in MAFIA_LEVEL:
                if not jid in TMAIL_LIST.keys():
                    TMAIL_LIST[jid]={}
                    i=str()
                    for x in TMAIL_LIST.keys():
                        i+=str(TMAIL_LIST.keys().index(x)+1)+') '+x+'\n'
                    for x in MAF_ADMINS:
                        msg(random.choice(CLIENTS.keys()),x,u'Новая заявка на допуск в игру, список: \n'+i)
                return u'Доступ новым юзерам временно ограничен, решение о допуске будет принимать адмистрация, ваш E-mail добавлен в список.\n'
    if MAF_TEMP_BAN['new']:
        if not jid in MAFIA_LEVEL:
            return u'Доступ новчикам временно закрыт!\nОбращайтесь в Xmpp конференцию cool@conference.mafiozo.in'
    try:
        if jid in CLON_CATCH.keys():
            if CLON_CATCH[jid]['list'] and [x for x in MAFIA.keys() if x in CLON_CATCH[jid]['list']]:
                pass#return u'Зафиксирована не честная игра с нескольких учеток!'
    except: pass
    if jid in MAF_TEMP_BAN['f']:
        return u'Ваш аккаунт заблокирован!'
    if jid in DBMFBAN_EVAL.keys():
        return u'Вы забанены вовеки!'
    if jid in MAF_TEMP_BAN['t']:
        if MAF_TEMP_BAN['t'][jid]>time.time():
            return u'До снятия бана осталось '+timeElapsed(MAF_TEMP_BAN['t'][jid]-time.time())
    return True


def mafia_admin_panel_init(*n):
    pass
    
register_message_handler(hnd_maf_admin)

def maf_adm_login(t, s, p):
    global MAF_ADMINS
    jid = get_true_jid(s)
    if not p or p.isspace():
        if jid in MAF_ADMINS:
            MAF_ADMINS.remove(jid)
            reply(t, s, u'Снял админа!')
        return
    
    #if p==u'':
    #    MAF_ADMINS.append(jid)
    #    reply(t, s, u'Вы войшли как администратор!')
    #    return

register_command_handler(maf_adm_login, 'мафлогин', ['мафия','все'], 0, 'Команда для входа в админ панель игры по паролю, без параметров снимает админа', 'мафлогин <пароль>', ['мафлогин пук'])

