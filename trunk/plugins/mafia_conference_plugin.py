#===istalismanplugin===
# -*- coding: utf-8 -*-

MAFC = {}

MAFC_SYS = {'start':0, 'hod':0, 'd':0, 'voice':{}, 'novoice':0, 'lim':[]}

MAFC_ROLES = {1:u'Мирный житель',2:u'Коммисар',3:u'Мафиози',4:u'Маньяк'}

def mfc_random(n):
    global MAFC
    list = range(n+1)
    while 1:
        id = random.choice(list)
        if not id in [MAFC[x]['id'] for x in MAFC.keys()]:
            break
    return id
    

def mafia_conference_start(t, s, p):
    global MAFC_SYS
    if not s[1] in GROUPCHATS or s[1]!='mafia_online@conference.jabber.ru':
        return
    if MAFC_SYS['start']:
        reply(t, s, u'На данный момент в мафию уже кто-то играет!')
        return
    list = [x for x in GROUPCHATS[s[1]].keys() if GROUPCHATS[s[1]][x]['ishere'] and x!=get_bot_nick(s[1])]
    if len(list)<6:
        reply(t, s, u'Необходимое количество игроков для начала игры: 6,\nВ чате: '+str(len(list)))
        return
    reply(t, s, u'Игра началась!!!Идет распределение ролей!!!')
    MAFC_SYS['start'] = 1
    mfc_roles(list, s)

def mfc_roles(list, s):
    random.shuffle(list)
    for x in list:
        time.sleep(1.8)
        id = mfc_random(len(list))
        if list.index(x)==0:
            MAFC[x]={'who':2, 'id':id, 'voice':1}
            msg(s[3], s[1]+'/'+x, u'Вы - Коммисар! Вы победите если посадите всех мафиози!\nПишите ночью мне в приват id игрока которого хотите проверить!')
        else:
            if list.index(x) in [1, 2]:
                MAFC[x]={'who':3, 'id':id, 'voice':1}
                msg(s[3], s[1]+'/'+x, u'Вы - Мафиози! Вы победите избавившись от мирных жителей!\nНочью вместе с напарником пишите мне в приват id игрока которого хотите убить! Для того чтобы увидеть напарника и получить список игроков используем ?? в привате!')
            else:
                if list.index(x)==len(list) and random.randrange(1,11) == 1:
                    MAFC[x]={'who':4, 'id':id, 'voice':1}
                    msg(s[3], s[1]+'/'+x, u'Вы - Маньяк! Вы победите казних всех жителей до одного!\nДля убийства пишем мне id жертвы ночью в приват!')
                else:
                    MAFC[x]={'who':1, 'id':id, 'voice':1}
                    msg(s[3], s[1]+'/'+x, u'Вы - Мирный житель! Вы победите казнив всех мафиози!\nДнем голосуйте вместе со всеми отправив id подозрительного по вашему мнению игрока в чат! Для того чтобы получить список игроков используем ??')
    time.sleep(1.5)
    msg(s[3], s[1], u'В игре участвуют: \n'+'\n'.join([unicode(x)+' [id='+str(MAFC[x]['id'])+']' for x in MAFC.keys()])+u'\nНаступила ночь! Дадим мафии познакомится друг с другом! Приват открыт!')
    mfc_cycle(s)

def mfc_calc_kill():
    mf = len([x for x in MAFC.keys() if MAFC[x]['who']==3 and MAFC[x]['voice']])
    if len(MAFC_SYS['voice'])==1:
        i=MAFC_SYS['voice'].keys()[0]
        if MAFC_SYS['voice'][i]==mf:
            return i
    return 0

def mfc_calc():
    mf = len([x for x in MAFC.keys() if MAFC[x]['who']==3 and MAFC[x]['voice']])
    if MAFC_SYS['voice']:
        l=list(MAFC_SYS['voice'].items())
        l.sort()
        if len(l)==1:
            if l[0][1]>1:
                return l[0][0]
            else: return
        if len(l)>1 and l[0][1]==l[1][1]:
            return 0
        return l[0][0]
    return 0

def mfc_scan(s):
    maf = [x for x in MAFC.keys() if MAFC[x]['who']==3 and MAFC[x]['voice']]
    mir = [x for x in MAFC.keys() if MAFC[x]['who']!=3 and MAFC[x]['voice']]
    live = [x for x in MAFC.keys() if MAFC[x]['voice']]
    if len(maf)==0:
        time.sleep(1.5)
        if len(live)==1 and MAFC[live[0]]['who']==4:
            msg(s[3], s[1], u'Победил Маньяк!!!')
            MAFC_SYS['start']=0
        else:
            msg(s[3], s[1], u'Поздравляем честных с победой!!!')
            MAFC_SYS['start']=0
    if len(maf)>=len(mir):
        time.sleep(1.5)
        msg(s[3], s[1], u'Победила мафия!!!')
        MAFC_SYS['start']=0
   
    
def mfc_cycle(s):
    global MAFC_SYS
    global MAFC
    global MAFC_ROLES
    n = 0
    while MAFC_SYS['start']:
        mfc_scan(s)
        if not MAFC_SYS['start']:
            break
        tim = random.randrange(90, 160)
        time.sleep(tim)
        MAFC_SYS['hod']+=1
        if MAFC_SYS['d']==1:
            ii = mfc_calc()
            MAFC_SYS['lim']=[]
            if ii!=0 or n==2:
                n = 0
                if ii in MAFC.keys():
                    time.sleep(2)
                    MAFC[ii]['voice']=0
                    msg(s[3], s[1], unicode(MAFC_ROLES[MAFC[ii]['who']])+u' '+unicode(ii)+u' отправлен на гильотину!')
                    time.sleep(1.5)
                MAFC_SYS['d'] = 0
                MAFC_SYS['voice'].clear()
                msg(s[3], s[1], u'Наступила ночь!!! Ход мафии!!!')
            else:
                n+=1
                MAFC_SYS['voice'].clear()
                msg(s[3], s[1], u'Поскольку честные не могут определиться дадим им еще один шанс!!!')
                
        else:
            ii = mfc_calc_kill()
            MAFC_SYS['lim']=[]
            if ii!=0:
                MAFC[ii]['voice']=0
                time.sleep(2)
                msg(s[3], s[1], unicode(MAFC_ROLES[MAFC[ii]['who']])+u' '+unicode(ii)+u' был убит ночью!')
                time.sleep(1.5)
                mfc_scan(s)
            MAFC_SYS['d']=1
            MAFC_SYS['voice'].clear()
            msg(s[3], s[1], u'Наступил день!!! Ищем и убиваем мафию!!!')
    time.sleep(1.8)
    msg(s[3], s[1], '\n'.join([unicode(x)+' - '+unicode(MAFC_ROLES[MAFC[x]['who']]) for x in MAFC.keys()]))
    time.sleep(1.5)
    msg(s[3], s[1], u'Игра окончена!!!')
    MAFC_SYS['voice'].clear()
    MAFC_SYS['hod']=0
    MAFC_SYS['d']=0
    MAFC_SYS['lim']=[]
    MAFC.clear()
                
def mfc_message(r, t, s, p):
    if not s[1] in GROUPCHATS:
        return
    if s[1]!='mafia_online@conference.jabber.ru':
        return
    if not s[2] in MAFC.keys():
        return
    if not MAFC[s[2]]['voice']:
        return
    if p=='??':
        rep='\n'.join([unicode(x)+' [id'+str(MAFC[x]['id'])+']' for x in MAFC.keys() if MAFC[x]['voice']])
        if MAFC[s[2]]['who']==3 and t in ['private','chat']:
            rep+=u'\nМафия :\n'+', '.join([unicode(x)+' [id='+str(MAFC[x]['id'])+']' for x in MAFC.keys() if MAFC[x]['who']==3 and MAFC[x]['voice']])
        reply(t, s, rep)
        return
    if MAFC_SYS['d']==1:
        if t not in ['groupchat','public']:
            reply(t, s, u'Днем голосуют только в чате!')
            return
    if p.isdigit() and int(p) in [MAFC[x]['id'] for x in MAFC.keys() if MAFC[x]['voice']]:
        if not s[2] in MAFC_SYS['lim']:
            MAFC_SYS['lim'].append(s[2])
        else:
            time.sleep(1.8)
            reply(t, s, u'Подожди следующего хода!!')
            return
        nick = [unicode(x) for x in MAFC.keys() if MAFC[x]['id']==int(p)][0]
        if MAFC_SYS['d']==0 and MAFC[s[2]]['who']==2:
            reply('private', s, nick+' '+MAFC_ROLES[MAFC[nick]['who']])
            return
        if MAFC_SYS['d']==0 and MAFC[s[2]]['who']==1:
            time.sleep(1.8)
            reply('private', s, u'Мирные ночью отдыхают!')
            return
        if nick in MAFC_SYS['voice'].keys():
            MAFC_SYS['voice'][nick]+=1
        else:
            MAFC_SYS['voice'][nick]={}
            MAFC_SYS['voice'][nick]=1
        if MAFC_SYS['d']==1:
            time.sleep(1.8)
            msg(s[3], s[1], s[2]+' [id'+str(MAFC[s[2]]['id'])+u'] хочет посадить '+unicode(nick)+' [id'+str(MAFC[nick]['id'])+']')
        else:
            time.sleep(1.8)
            reply('private', s, u'ok')
        


register_message_handler(mfc_message)
register_command_handler(mafia_conference_start, 'mafia', ['все','игры'], 0, 'Игра мафия.', 'mafia', ['mafia'])
