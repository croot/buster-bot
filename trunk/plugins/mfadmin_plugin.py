#===istalismanplugin===
# -*- coding: utf-8 -*-

MF_WHO_JOIN = {}

MAF_ADMINS = [u'some_user@jabbrik.ru',u'apostol@xmpp.ru']

MAF_TEMP_BAN = {'f':[],'t':{},'new':0}

def hnd_maf_admin(raw, type, source, parameters):
    jid = get_true_jid(source)
    rep = ''
    if jid in MAF_ADMINS:
        if parameters==u'#0':
            rep+=u'#1 - список пользователей в игре,\n'
            rep+=u'#2 - список пользователей посещавших игру за время работы бота,\n'
            rep+=u'#3 - остановка игры,\n'
            rep+=u'#4 - сообщение в игру,\n'
            rep+=u'#5 - предупреждение игроку id текст,\n'
            rep+=u'#6 - блокировка игрока id причина,\n'
            rep+=u'#7 - кик игрока id,\n'
            rep+=u'#8 - временная блокировка игрока id часы,\n'
            rep+=u'#9 - временный запрет входа юзеров не из базы,\n'
            rep+=u'#10 - вывод правил в общий чат,\n'
            rep+=u'#11 - изменить ник id ник,\n'
            rep+=u'#12 - запуск бастера,\n'
            rep+=u'#13 - достает из бана юзера по jid'
            reply(type, source, rep)
            return
        if parameters==u'#10':
            pr=u"Следущие действия рассцениваються как нарушение правил игры:\n1.Сознательный подыгрыш или проигрыш другим персонажам в целях набора очков.\n2.Передача ценной игровой информации вне общего чата партии.\n3.Действия (бездействия), противоречащие логике партии и здравому смыслу, совершённые в силу неигровых мотивов (недовольство ролью, безразличное отношение к исходу партии и т.п.), которые послужили причиной ничьей или поражения своей стороны.\n4.Сообщение своей роли в общий чат, когда это сообщение не является одним из элементов тактики, что подтверждается разумным смыслом и логикой партии.\n5.Предвзятое и нескрываемое негативное отношение одного игрока/группы игроков к другому, что выражается в действиях, противоречащих логичному течению партии."
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
            rep=''
            for x in MF_WHO_JOIN:
                rep+=x+' '+MF_WHO_JOIN[x]+'\n'
            if not rep or rep.isspace():
                reply(type, source, u'статистики нет')
                return
            reply(type, source, rep)
            return
        if parameters==u'#9':
            rep=u'включена'
            if MAF_TEMP_BAN['new']:
                MAF_TEMP_BAN['new']=0
                rep=u'отключена'
            else:
                MAF_TEMP_BAN['new']=1
            reply(type, source, rep+u' врменная блокировка юзеров не с базы!')
            mafia_bot(rep+u' врменная блокировка юзеров не с базы!')
            return
        if parameters==u'#3':
            mafia_bot(u'Приносим свои извенения, партия остановлена адмистратором!')
            MAFIA_SES['start']=0
            MAFIA.clear()
            for x in MAF_ADMINS:
                if x!=jid:
                    msg(x,u'Партия была остановлена '+jid)
            reply(type, source, u'сча остановим!')
            return
        if parameters.count(' '):
            s=parameters.split()
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
                                    msg(c,x+u' был забанен '+jid)
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
                                    msg(c,x+u' был забанен '+jid)
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
                            MF_REPLACE[x]=i
                            db=eval(read_file('dynamic/mf_replace.txt'))
                            db[x]={}
                            db[x]=i
                            write_file('dynamic/mf_replace.txt',str(db))
                            MAFIA[x]['nick']=i
                            reply(type, source, u'ok')
                            return

def mafia_check(jid):
    MF_WHO_JOIN[jid]=time.ctime()
    if MAF_TEMP_BAN['new']:
        if not jid in MAFIA_LEVEL:
            return u'Доступ новчикам временно закрыт!'
    if jid in MAF_TEMP_BAN['f']:
        return u'Ваш аккаунт заблокирован!'
    if jid in MAF_TEMP_BAN['t']:
        if MAF_TEMP_BAN['t'][jid]>time.time():
            return u'До снятия бана осталось '+timeElapsed(MAF_TEMP_BAN['t'][jid]-time.time())
    return True

def mafia_admin_panel_init():
    pass
    
register_message_handler(hnd_maf_admin)
