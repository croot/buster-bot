# -*- coding: utf-8 -*-

def check_globals(p):
    for x in globals().keys():
        if p.count(x) and x not in ['re','msg','random','reply','time','timeElapsed','jid','user_level']: return x
    for x in ['for','while','print','def','class','**','import','eval','exec','execfile','global','write','read','open']:
        if p.count(x): return x
    return 0


ALIAS = {}
ALIAS_FILE = 'dynamic/alias.txt'
ALIAS_BUFFER = {'msg':{},'join':{}}
ALIAS_JOIN = {}


def alias_exec_add_join(t, s, p):
    if not s[1] in GROUPCHATS: return
    if not p:
        if not s[1] in ALIAS_JOIN.keys() or not ALIAS_JOIN[s[1]]:
            reply(t, s, u'Нет алиасов!')
            return
        reply(t, s, ';\n'.join([str(x)+') '+ALIAS_JOIN[s[1]][x] for x in ALIAS_JOIN[s[1]]]))
        return

    cnt = 0
    
    if p.isdigit() and s[1] in ALIAS_JOIN.keys():
        if int(p) in ALIAS_JOIN[s[1]].keys():
            del ALIAS_JOIN[s[1]][int(p)]
            reply(t, s, u'ok')
            db=eval(read_file(ALIAS_FILE))
            del db['join'][s[1]][int(p)]
            write_file(ALIAS_FILE, str(db))
            return
        else:
            reply(t, s, u'?')
            return
        
    ch = check_globals(p)
    
    if ch:
        reply(t, s, u'Выражение содержит имя запрещенной глобальной переменной '+ch+ ' !')
        return
    if not isinstance(p, basestring):
        reply(t, s, u'Фиг!')
        return

    c35 = p.count('#')
    
    if c35 > 2:
        reply(t, s, u'Больше двух команд нельзя!')
        return

    rp = {}
    org = p
    
    for x in COMMAND_HANDLERS:
        if p.count(' '+x+' ') or p.count('#'+x+' ') and len(x)>2:
            if not p.count('#'):
                reply(t, s, u'А где завершение параметров # ?')
                return

            cnt += 1
            
            real_access = COMMANDS[x]['access']
            if not has_access(s, real_access, s[1]):
                reply(t, s, u'Недостаточный доступ для команды '+x)
                return
            
            a = re.findall(x+'.*?#', p, re.DOTALL | re.IGNORECASE)[0]
            g = re.findall(x+'(.*?)#', p, re.DOTALL | re.IGNORECASE)[0]#p.split(x)[1]
            g = g.replace('{','\"""+random.choice([').replace('}','])+u\"""')
            g = g.replace('</','\"""+').replace('\>','+u\"""')
            
            m = ("""threading.Thread(None,COMMAND_HANDLERS[u'%s'],'command'+str(INFO['thr']),(t, s, u\"""%s\""",)).start();""") % (x, g.strip())

            rp[a] = m

    if cnt != c35:
        reply(t, s, u'Что-то сделано неверно! Число команд: '+str(cnt)+u', число завершений параматров #: '+str(c35))
        return

    for x in rp.keys():
        p = p.replace(x, rp[x])
        
    if int(user_level(s, s[1]))<100:
        n=random.randrange(20, 9999)
        if not s[1] in ALIAS_BUFFER['join']: ALIAS_BUFFER['join'][s[1]]={}
        ALIAS_BUFFER['join'][s[1]][n]={}
        ALIAS_BUFFER['join'][s[1]][n]=p
        reply(t, s, u'Ок! Алиас будет добавлен после дополнительной проверки админами!')
        for x in [x for x in GLOBACCESS.keys() if GLOBACCESS[x]==100]:
            time.sleep(1)
            msg(s[3], x, u'Новый алиас поступил на проверку от '+s[1]+'/'+s[2]+u', id '+str(n)+u'.\nДля активации напишите id алиаса!\n'+org)
        return
    else:
        if not s[1] in ALIAS_JOIN.keys(): ALIAS_JOIN[s[1]]={}
        n = len(ALIAS_JOIN[s[1]])+1
        ALIAS_JOIN[s[1]][n]={}
        ALIAS_JOIN[s[1]][n]=p
        alias_append(s[1], 'join', p, n)
        reply(t, s, u'ok!')
    

def alias_exec_add_msg(t, s, p):
    if not s[1] in GROUPCHATS: return
    cnt = 0
    if not p:
        if not s[1] in ALIAS.keys() or not ALIAS[s[1]]:
            reply(t, s, u'Нет алиасов!')
            return
        reply(t, s, ';\n'.join([str(x)+') '+ALIAS[s[1]][x] for x in ALIAS[s[1]]]))
        return
    if p.isdigit() and s[1] in ALIAS.keys():
        if int(p) in ALIAS[s[1]].keys():
            del ALIAS[s[1]][int(p)]
            reply(t, s, u'ok')
            db=eval(read_file(ALIAS_FILE))
            del db['msg'][s[1]][int(p)]
            write_file(ALIAS_FILE, str(db))
            return
        else:
            reply(t, s, u'?')
            return
        
    ch = check_globals(p)
    
    if ch:
        reply(t, s, u'Выражение содержит имя запрещенной глобальной переменной '+ch+ ' !')
        return
    if not isinstance(p, basestring):
        reply(t, s, u'Фиг!')
        return

    c35 = p.count('#')

    if c35>2:
        reply(t, s, u'Больше двух команд нельзя!')
        return
    
    rp = {}
    org = p
    
    for x in COMMAND_HANDLERS.keys():
        if p.count(' '+x+' ') or p.count('#'+x+' ') and len(x)>=2:
            if p.count('#')<1:
                reply(t, s, u'А где завершение параметров # ?')
                return

            cnt += 1
            
            real_access = COMMANDS[x]['access']
            if not has_access(s, real_access, s[1]):
                reply(t, s, u'Недостаточный доступ для команды '+x)
                return
            
            a = re.findall(x+'.*?#', p)[0]
            g = re.findall(x+'(.*?)#', p)[0]
            g = g.replace('{','\"""+random.choice([').replace('}','])+u\"""')
            g = g.replace('</','\"""+').replace('\>','+u\"""')
            
            m = """threading.Thread(None,COMMAND_HANDLERS[u'%s'],'command'+str(INFO['thr']),(t, s, u\"""%s\""",)).start(); """ % (x, g.strip())
            
            rp[a] = m

    if cnt != c35:
        reply(t, s, u'Что-то сделано неверно! Число команд: '+str(cnt)+u', число завершений параматров #: '+str(c35))
        return
            
    for x in rp:
        p=p.replace(x, rp[x])
    if int(user_level(s, s[1]))<100:
        n=random.randrange(20, 9999)
        if not s[1] in ALIAS_BUFFER['msg']: ALIAS_BUFFER['msg'][s[1]]={}
        ALIAS_BUFFER['msg'][s[1]][n]={}
        ALIAS_BUFFER['msg'][s[1]][n]=p
        reply(t, s, u'Ок! Алиас будет добавлен после проверки!')
        for x in [x for x in GLOBACCESS.keys() if GLOBACCESS[x]==100]:
            msg(s[3], x, u'Новый алиас поступил на проверку с комнаты '+s[1]+u', id '+str(n)+u'.\nДля активации напишите id алиаса!\n'+org)
        return
    else:
        if not s[1] in ALIAS.keys(): ALIAS[s[1]]={}
        n = len(ALIAS[s[1]])+1
        ALIAS[s[1]][n]={}
        ALIAS[s[1]][n]=p
        alias_append(s[1], 'msg', p, n)
        reply(t, s, u'ok!')

def alias_append(chat, tt, p, n):
    db=eval(read_file(ALIAS_FILE))
    if not chat in db[tt]: db[tt][chat] = {}
    if not n in db[tt][chat]: db[tt][chat][n] = {}
    db[tt][chat][n] = p
    write_file(ALIAS_FILE, str(db))
    

def alias_msg(r, t, s, p):
    if not s[1] in ALIAS.keys(): return
    if s[2] == get_bot_nick(s[1]): return
    if p.count(' ') and p.split()[0].lower() in COMMANDS.keys(): return
    userjid = get_true_jid(s)
    serv, lastmsg, p0, p1 = '', 0, p.lower(), ''
    try: lastmsg = time.time()-GROUPCHATS[s[1]][s[2]]['idle']
    except: pass
    try: serv = userjid.split('@')[1]
    except: pass
    if p.count(' '):
        sp=p.split()
        p0=sp[0]
        p1=sp[1]
    nick = s[2]
    chat = s[1]
    for x in ALIAS[s[1]].keys():
        i=ALIAS[s[1]][x].replace('$p0',p0).replace('$p1',p1).replace('$lastmsg',str(lastmsg)).replace('$nick',nick).replace('$chat',chat).replace('$userjid',userjid).replace('$serv',serv).replace('$p',p)
        try: exec i
        except Exception as err:
            try: msg(s[3], s[1], u'Исключение при выполнении алиаса '+ALIAS[s[1]][x]+u':\n'+str(err.message))
            except: pass
            del ALIAS[s[1]][x]
            write_file(ALIAS_FILE, str(ALIAS))

def alias_join(chat, nick, role, aff, cljid):
    t='public'
    s=[chat+'/'+nick,chat,nick,cljid]
    if not chat in GROUPCHATS: return
    if not chat in ALIAS_JOIN: return
    if nick == get_bot_nick(chat): return
    userjid = get_true_jid(chat+'/'+nick)
    serv, timej = '', 0
    try: serv = userjid.split('@')[1]
    except: pass
    try: timej = time.time()-GROUPCHATS[chat][nick]['joined']
    except: pass
    for x in ALIAS_JOIN[chat].keys():
        i=ALIAS_JOIN[chat][x].replace('$role',role).replace('$aff',aff).replace('$timej', str(timej)).replace('$nick',nick).replace('$chat',chat).replace('$userjid',userjid).replace('$serv',serv)
        try: exec i
        except Exception, err:
            try: msg(cljid, chat, u'Зарегестрировано исключение при выполнении '+ALIAS_JOIN[chat][x]+':\n'+err)
            except: pass
            del ALIAS_JOIN[chat][x]

def alias_adm_check(r, t, s, p):
    global ALIAS
    global ALIAS_MSG
    global ALIAS_BUFFER
    jid = get_true_jid(s)
    al, ak, chat = '', 0, ''
    if jid in [x for x in GLOBACCESS.keys() if GLOBACCESS[x]==100] and p.isdigit() and int(p)>19:
        for x in ALIAS_BUFFER['join'].keys():
            for c in ALIAS_BUFFER['join'][x]:
                if c == int(p):
                    al = ALIAS_BUFFER['join'][x][int(p)]
                    del ALIAS_BUFFER['join'][x][int(p)]
                    chat = x
                    break
        for x in ALIAS_BUFFER['msg'].keys():
            for c in ALIAS_BUFFER['msg'][x]:
                if c == int(p):
                    al = ALIAS_BUFFER['msg'][x][int(p)]
                    del ALIAS_BUFFER['msg'][x][int(p)]
                    chat = x
                    ak = 1
                    break
        if not al: return

        reply(t, s, u'Вы активировали алиас:\n'+al)
        
        if ak:
            if not chat in ALIAS.keys(): ALIAS[chat] = {}
            
            n = len(ALIAS[chat])+1
            
            if n in ALIAS[chat].keys(): n = random.randrange(99, 9999)
                
            ALIAS[chat][n] = {}
            ALIAS[chat][n] = al
            alias_append(chat, 'msg', al, n)
            return
        
        if not chat in ALIAS_JOIN.keys(): ALIAS_JOIN[chat]={}

        n = len(ALIAS_JOIN[chat])+1
        
        if n in ALIAS_JOIN[chat].keys(): n = random.randrange(99, 9999)
        
        ALIAS_JOIN[chat][n]={}
        ALIAS_JOIN[chat][n]=al
        alias_append(chat, 'join', al, n)

def alias_init(cljid):
    global ALIAS
    global ALIAS_JOIN
    if 'db_file' in globals().keys():
        db_file(ALIAS_FILE)
    else:
        check_file(file=ALIAS_FILE)
    db=eval(read_file(ALIAS_FILE))
    if not 'msg' in db.keys():
        db['msg']={}
        write_file(ALIAS_FILE, str(db))
    if not 'join' in db.keys():
        db['join']={}
        write_file(ALIAS_FILE, str(db))
    ALIAS = db['msg'].copy()
    ALIAS_JOIN = db['join'].copy()

ALS_HELP = """Для более простого восприятия питон кода в алиасе,
в частности человеку далекому от программирования
можно отдельно рассмотреть типичные инструкции,
начнем с типичного оператора if (если).
Условно, для более общего представления, конструкцию кода с условием
можно описать следующим образом:
if <если истинно>: то делай это
А теперь рассмотрим логические операторы:
and (и)
or (или)
not (отрицание)
а так же сравнения:
== (равно)
!- (не равно)
> (больше)
=> (больше либо равно)
и не забудем об операторе in - который проверяет наличие чего либо в
списках и не только. 

А теперь конкретные примеры:

if 1+1==2 and not 4+4==5: сказать пример удался!#
Если 1+1 равно 2 - условие верно, и верно отрицание того что 4+4 равно 5 - выполняется код после двух точек.

if nick in [u'петя',u'мотя'] and serv in ['jabbrik.ru']: time.sleep(5); сказать $nick : привет!#
Если переменная ник есть в списке [1] и переменная сервера есть в списке [2]: условие верно, идет ожидание 5 секунд, и выполняется нужная нам команда!
"""

def als_help(t, s, p):
    reply(t, s, ALS_HELP)
    
            
register_command_handler(als_help, 'alias_help', ['все'], 20, 'Помощь по алиасам', 'alias_help', ['alias_help'])        
register_command_handler(alias_exec_add_msg, 'alias_msg', ['все'], 20, 'Добавление алиаса с использованием кода питон. Без параметров выводит список всех алиасов. Активируется при сообщении. см. также alias_help .Есть несколько переменных $nick-ник написавшего, $p0 - первое слово до пробела, $p1 - второе слово, $userjid-жид, $serv - сервер, $chat-конфа ,$p - текст который написал юзер, $p0 - первое слово до пробела, $p1 - второе слово до пробела.', 'alias_msg <условие> <вызов команды и параметры> # или alias_msg <номер алиаса> чтобы удалить алиас', ['alias_msg if p==u\'конец света\': сказать конец света через </str(random.randrange(10,99999))\> дней!#','alias_msg if len(p)>1000: кик $nick#','alias_msg if p.count(u\'привет\'): time.sleep(10); сказать $nick: {u\'здарова!\',u\'выручи на рубас?\'}#','alias_msg if nick.count(u\'вася\'): time.sleep(5); сказать привет, $nick!#','alias_msg if p==u\'Что такое пук?\': сказать $nick: Звук, издаваемый при выходе газов из кишечника. Громкий пук.#'])        
register_command_handler(alias_exec_add_join, 'alias_join', ['все'], 20, 'Добавление алиаса с использованием кода питон. Без параметров выводит список всех алиасов. Активируется на презенс. см. также alias_help .Есть несколько переменных $nick-ник написавшего, $userjid-жид, $serv - сервер, $chat-конфа', 'alias_join <условие> <вызов команды и параметры> #', ['alias_join if len(nick)>19: бан $nick#','alias_join if nick.count(u\'вася\'): time.sleep(5); сказать {u\'привет\',u\'хобуна\'}#','alias_join if not serv in [\'jabber.ru\',\'talkonaut.com\']: бан $serv#'])        
register_message_handler(alias_msg)
register_join_handler(alias_join)
register_message_handler(alias_adm_check)
register_stage0_init(alias_init)

    
