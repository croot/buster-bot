#===istalismanplugin===
# -*- coding: utf-8 -*-

#by 40tman

COLOR = [u'манго',u'пурпурный',u'пепельный',u'бронзовый',u'красный',u'зеленый',u'черный',u'синий',u'белый',u'желтый',u'салатовый',u'оранжевый',u'фиолетовый']

BOOMB_USER = {}
BOOMB_CONT = {}

def bomb_send(type, source, parameters):
        global BOOMB_USER
        global COLOR

        random.shuffle(COLOR)

        jid = get_true_jid(source)

        chat = False

        if source[1] in GROUPCHATS:
                chat = True
                if not parameters:
                        reply(type, source, u'Кому?')
                        return
                if type in ['private','chat']:
                        reply(type,source,u'Разрешено только в общем чате!')
                        return
                if not parameters in GROUPCHATS[source[1]]:
                        reply(type,source,u'а он тут?')
                        return
                if parameters == get_bot_nick(source[1]):
                        reply(type, source, u'фига!')
                        return
                jid = get_true_jid(source[1]+'/'+parameters)
                if jid in BOOMB_USER:
                        reply(type, source, u'Пока нельзя!')
                        return
        if not parameters:
                parameters = source[2]

        if jid in BOOMB_CONT and time.time()-BOOMB_CONT[jid]<300:
                reply(type, source, (u'У вас контузия на 5 минут!' if not chat else u'У него контузия на 5 минут!'))

        BOOMB_CONT[jid] = time.time()

        tim, part1 = random.randrange(20, 45), u'Вам вручена бомба, на ней '
        number = random.randrange(2, 6)
        
        list = COLOR[:number]
        
        BOOMB_USER[jid] = {'adr':source[1], 'chat':chat, 'wires':list, 'true': random.choice(list)}

        rep = part1+str(len(list))+u' провода: '+', '.join(list)+u'.\n Вам нужно выбрать цвет провода который нужно перерезать, на таймере '+str(tim)+u' с.'
        if chat:
                msg(source[3], source[1], u'/me '+parameters+u': '+rep)
        else:
                reply(type, source, rep)

        
        bomb_start(source[3], source[1], parameters, tim, jid)

def kick_bomb(cljid, groupchat, nick, reason=''):
        room_access(cljid, groupchat, 'role', 'none', 'nick', nick)
	try:
                if groupchat in order_stats and jid in order_stats[groupchat]:
                        order_stats[groupchat][jid]['kicks']=0
        except:
                pass

def bomb_start(cljid, groupchat, nick, tim, jid):
        time.sleep(tim)
        if jid in BOOMB_USER:
                if BOOMB_USER[jid]['chat']:
                        kick_bomb(cljid, groupchat, nick, u'птыдыщь!')
                        msg(cljid, groupchat, u'/me '+nick+u' улетел к ебеням!')
                else:
                        msg(cljid, jid, u'Время вышло! Вы труп!')
                del BOOMB_USER[jid]
                
def bomb_msg(raw, type, s, p):
        jid = get_true_jid(s)

        if not jid in BOOMB_USER: return
        
        if s[1] in GROUPCHATS and BOOMB_USER[jid]['chat']:
                for x in [get_bot_nick(s[1])+x for x in [':',',','>']]:
                        p = p.replace(x,'')
                        p = p.strip()
                if BOOMB_USER[jid]['adr'] == s[1]:
                        if p.lower()==BOOMB_USER[jid]['true']:
                                reply(type, s, u'Бомба обезврежена!')
                                del BOOMB_USER[jid]
                                return
                        else:
                                if p.lower() in BOOMB_USER[jid]['wires']:
                                        kick_bomb(s[3], s[1], s[2], u'птыдыщь!')
                                        msg(s[3], s[1], u'Нужный провод был: '+BOOMB_USER[jid]['true'])
                                        del BOOMB_USER[jid]
                                        return
        else:
                if p.lower()==BOOMB_USER[jid]['true']:
                        reply(type, s, u'Бомба обезврежена!')
                        del BOOMB_USER[jid]
                        return
                else:
                        if p.lower() in BOOMB_USER[jid]['wires']:
                                msg(s[3], s[1], u'Нужный провод был: '+BOOMB_USER[jid]['true'])
                                del BOOMB_USER[jid]
                                return
                        

def bomb_leave(groupchat, nick, pr, prr, cljid):
        jid = get_true_jid(source)
        if not jid in BOOMB_USER: return
        if BOOMB_USER[jid]['adr'] == groupchat:
                del BOOMB_USER[jid]
                msg(cljid, groupchat, u'Бомба не обезврежена, '+nick+u' зассал!')
                
                
register_leave_handler(bomb_leave)                    
register_message_handler(bomb_msg)
register_command_handler(bomb_send, 'бомба', ['мук','все'], 15, 'Вручает учасникам бомбу),если перерезать не той провод будет кик, время 15 секунд', 'бомба <nick>', ['бомба abyba'])
