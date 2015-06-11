#===istalismanplugin===
# -*- coding: utf-8 -*-


AUTO_MUC = {}

AUTO_MUC_FILE = 'dynamic/auto.txt'

db_file(AUTO_MUC_FILE, dict)

AUTO_MUC = eval(read_file(AUTO_MUC_FILE))


def auto_moderator(type, source, p):
    global AUTO_MUC_FILE
    global AUTO_MUC

    if not source[1] in GROUPCHATS:
        return
    
    try: db = eval(read_file(AUTO_MUC_FILE))
    except:
        reply(type,source,u'Ошибка в файле \"dynamic/auto.txt\"!')
        return
    
    if p:
        t = p.lower()
        
        if t.count(u'дел')>0 and t.count('-')>0:
            numb = p.split('-')
            if len(numb[1].strip())>3 or len(numb[1].strip())==0:
                return
            if not source[1] in db.keys():
                reply(type, source, u'Пустой список!')
                return
            try:
                list = db[source[1]][2].keys()
                if len(list)<int(numb[1].strip()):
                    relpy(type, source, u'Неверный ввод!')
                    return
                who = list[int(numb[1].strip())]
                del db[source[1]][2][db[source[1]][2].keys()[int(numb[1].strip())]]
                write_file(AUTO_MUC_FILE, str(db))
                reply(type,source, who+u' удалeн!')
                AUTO_MUC = db.copy()
                return
            except:
                reply(type, source, u'Произошла ошибка!')
                return

            
        if not source[1] in db.keys():
            db[source[1]] = {}

        if not 2 in db[source[1]].keys():
            db[source[1]][2] = {}

        if not p in db[source[1]][2].keys():
            db[source[1]][2][p] = {}
            write_file(AUTO_MUC_FILE, str(db))
            auto_set_roles(source, p, 'moderator', 'amoderator')
            reply(type, source, u'Пользователь \"'+p+u'\" добавлен!')
            AUTO_MUC = db.copy()
            return
        else:
            del db[source[1]][2][p]
            write_file(AUTO_MUC_FILE, str(db))
            reply(type,source,u'Автомодер с \"'+p+u'\" снят!')
            auto_set_roles(source, p,'participant',u'command '+source[2])
            AUTO_MUC = db.copy()
            return
            
    else:
        try:
            list = [str(db[source[1]][2].keys().index(x))+') '+x for x in db[source[1]][2].keys()]
            if not list:
                reply(type, source, u'Список пуст!')
                return
            reply(type, source, '\n'.join(list))
        except:
            reply(type, source, u'Список пуст!')
            return

        
def auto_kick(type, source, p):
    global AUTO_MUC_FILE
    global AUTO_MUC

    if not source[1] in GROUPCHATS or p==get_bot_nick(source[1]):
        return
    
    db, rep = eval(read_file(AUTO_MUC_FILE)), ''

    if p:
        t = p.lower()
        s = p.split()

        if t.count(u'дел') and t.count('-'):
            numb = t.split('-')
            if len(numb[1].strip())>3 or len(numb[1].strip())==0:
                return
            if not source[1] in db.keys():
                reply(type, source, u'Пустой список!')
                return
            try:
                list = db[source[1]][1].keys()
                if len(list)<int(numb[1].strip()):
                    relpy(type, source, u'Неверный ввод!')
                    return
                who = list[int(numb[1].strip())]
                del db[source[1]][1][db[source[1]][1].keys()[int(numb[1].strip())]]
                write_file(AUTO_MUC_FILE, str(db))
                reply(type,source, who+u' удалeн!')
                AUTO_MUC = db.copy()
                return
            except Exception, err:
                reply(type, source, u'Произошла ошибка!')

            
        if not source[1] in db.keys():
            db[source[1]] = {}

        if not 1 in db[source[1]].keys():
            db[source[1]][1]={}
            
        if t.count(' ') and t.count('.count') and t.count('*')>0:
            dd = p.split('*')
            db[source[1]][1] = '*'+dd[1].strip()
            write_file(AUTO_MUC_FILE, str(db))
            reply(type, source, u'В акик добавлены все ники содержащие \"'+dd[1].strip()+'\"!')
            AUTO_MUC = db.copy()
            return
        
        if not p in db[source[1]][1].keys():
            db[source[1]][1][p] = {}
            write_file(AUTO_MUC_FILE ,str(db))
            reply(type, source, p+u' добавлено!')
            AUTO_MUC = db.copy()
            if p in GROUPCHATS[source[1]]:
                auto_set_roles(source, p,'none',u'Autokick!')
        else:
            del db[source[1]][1][p]
            write_file(AUTO_MUC_FILE, str(db))
            reply(type,source, p+u' удален!')
            AUTO_MUC = db.copy()
    else:
        try:
            list = [str(db[source[1]][1].keys().index(x))+') '+x for x in db[source[1]][1].keys()]
            if not list:
                reply(type, source, u'Список пуст!')
                return
            reply(type, source, '\n'.join(list))
        except:
            reply(type, source, u'Список пуст!')
            return


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def auto_visitor(type, source, p):
    global AUTO_MUC_FILE
    global AUTO_MUC

    if not source[1] in GROUPCHATS: return
    
    db = eval(read_file(AUTO_MUC_FILE))

    tm = 0

    jid = ''

    if p:
        t = p.lower()
        
        if t.count(u'дел')>0 and t.count('-')>0:
            numb = p.split('-')
            if len(numb[1].strip())>3 or len(numb[1].strip())==0:
                return
            if not source[1] in db.keys():
                reply(type, source, u'Пустой список!')
                return
            try:
                list = db[source[1]][3].keys()
                if len(list)<int(numb[1].strip()):
                    relpy(type, source, u'Неверный ввод!')
                    return
                who = list[numb[1].strip()]
                del db[source[1]][3][db[source[1]][3].keys()[int(numb[1].strip())]]
                write_file(AUTO_MUC_FILE, str(db))
                reply(type,source, who+u' удалeн!')
                AUTO_MUC = db.copy()
                return
            except:
                reply(type, source, u'Произошла ошибка!')
                return
            
        if not source[1] in db.keys():
            db[source[1]] = {}

        if not 3 in db[source[1]].keys():
            db[source[1]][3] = {}
        
        if not p in db[source[1]][3].keys():
            if not p in GROUPCHATS[source[1]]:
                if p.count(' ') and is_number(p.split()[-1:][0]):
                    tm = time.time()+float(p.split()[-1:][0])*3600
                    p = ' '.join(p.split()[:-1])
            if p in GROUPCHATS[source[1]]:
                jid = get_true_jid(GROUPCHATS[source[1]][p]['jid'])
            db[source[1]][3][(jid if jid else p)] = ({} if not tm else tm)
            write_file(AUTO_MUC_FILE ,str(db))
            reply(type, source, p+u' добавлено!'+('' if not tm else u'(девойс на время)'))
            AUTO_MUC = db.copy()
            if p in GROUPCHATS[source[1]]:
                auto_set_roles(source, p,'visitor',u'Autovisitor')
        else:
            del db[source[1]][3][p]
            write_file(AUTO_MUC_FILE, str(db))
            reply(type,source, p+u' удален!')
            AUTO_MUC = db.copy()
    else:
        try:
            list = [str(db[source[1]][3].keys().index(x))+') '+x for x in db[source[1]][3].keys()]
            if not list:
                reply(type, source, u'Список пуст!')
                return
            reply(type, source, '\n'.join(list))
        except:
            reply(type, source, u'Список пуст!')
            return


def autoroles_hh_msg(r, t, s, p):
    if not s[1] in GROUPCHATS: return
    if not s[1] in AUTO_MUC.keys(): return
    for x in AUTO_MUC[s[1]].get(3, []):
        if isinstance(AUTO_MUC[s[1]][3][x],int) or isinstance(AUTO_MUC[s[1]][3][x],float):
            if time.time() - AUTO_MUC[s[1]][3][x]>0:
                try:
                    auto_set_roles(s, [c for c in GROUPCHATS[s[1]].keys() if get_true_jid(GROUPCHATS[s[1]][c]['jid'])==x][0],'participant','Time visitor is up!')
                    del AUTO_MUC[s[1]][3][x]
                    write_file(AUTO_MUC_FILE, str(AUTO_MUC))
                except: pass

register_message_handler(autoroles_hh_msg)
        
                    
def autoroles_join_rm(gch,nick,afl,role,cljid):
    global AUTO_MUC
    if not gch in GROUPCHATS or len(nick)>35: return
    s = [gch, gch, nick, cljid]

    jid = get_true_jid(gch+'/'+nick)

    if not gch in AUTO_MUC.keys(): return

    for x in AUTO_MUC[gch].get(3, []):
        if isinstance(AUTO_MUC[gch][3][x],int) or isinstance(AUTO_MUC[gch][3][x],float):
            if time.time() - AUTO_MUC[gch][3][x]>0:
                try: auto_set_roles(s, [c for c in GROUPCHATS[gch].keys() if get_true_jid(GROUPCHATS[gch][c]['jid'])==x][0],'participant','Time visitor is up!')
                except: pass

    if nick == get_bot_nick(gch): return

    if 1 in AUTO_MUC[gch]:
        for x in AUTO_MUC[gch][1].keys():
            if x[:1] == '*' and nick.count(unicode(x))>0:
                auto_set_roles(s, nick, 'none', u'Autokick!')
                
    if 2 in AUTO_MUC[gch].keys():
        if jid in AUTO_MUC[gch][2].keys() or nick in AUTO_MUC[gch][2].keys():
            auto_set_roles(s, nick,'moderator','Amoderator')

    if 1 in AUTO_MUC[gch].keys():
        if jid in AUTO_MUC[gch][1].keys() or nick in AUTO_MUC[gch][1].keys():
            auto_set_roles(s, nick, 'none', u'Autokick!')

    if 3 in AUTO_MUC[gch].keys():
        if jid in AUTO_MUC[gch][3].keys() or nick in AUTO_MUC[gch][3].keys():
            if isinstance(AUTO_MUC[gch][3][jid],int) or isinstance(AUTO_MUC[gch][3][jid],float):
                if time.time() - AUTO_MUC[gch][3][jid]>0:
                    del AUTO_MUC[gch][3][jid]
                    write_file(AUTO_MUC_FILE, str(AUTO_MUC))
                    return
            auto_set_roles(s, nick,'visitor','Read only!')
    
        
     
def auto_set_roles(s, nick, rol, reason):
    moderate(s, 'nick', nick, 'role', rol, reason)
#	iq = xmpp.Iq('set')
#	iq.setTo(groupchat)
#	iq.setID('kick'+str(random.randrange(1000, 9999)))
#	query = xmpp.Node('query')
#	query.setNamespace('http://jabber.org/protocol/muc#admin')
#	kick=query.addChild('item', {'nick':nick, 'role':rol})
#	kick.setTagData('reason', get_bot_nick(groupchat)+': '+reason)
#	iq.addChild(node=query)
#	JCON.send(iq)


register_join_handler(autoroles_join_rm)
register_command_handler(auto_moderator, 'амодератор', ['все'], 20, 'Добавляет ник юзера в автомодераторы.Без параметров показывает список.Чтобы удалить жид пользуемся ключом \"дел - номер\", после минуса вписываем номер в списке,например: амодератор дел -1', 'амодератор <ник>', ['амодератор Вася'])
register_command_handler(auto_kick, 'акик', ['все'], 20, 'Добавляет ник либо jid в автокик,без параметров покажет акик лист,дополнительные ключи команды:  .count *В - будет кикать все ники содержащие <В>; дел -1 - удалит из списка елемент с номером <1>', 'акик <ник>', ['акик Вася','акик .count *В'])
register_command_handler(auto_visitor, 'авизитор', ['все'], 20, 'Добавляет/удаляет ник либо jid в список пользователей без права голоса.Без параметров показывает список. \nПри необходимости после ника можно указывать параметр время в часах на которое юзер будет лишен голоса.', 'авизитор <ник>', ['авизитор Вася','авзитор Вася 1'])

