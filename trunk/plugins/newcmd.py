#===istalismanplugin===
# -*- coding: utf-8 -*-

CMD_HELP_MEM = {}

HASHCMD_FILE = 'dynamic/hashcmd.txt'

db_file(HASHCMD_FILE, dict)


UPDATED_AND_NEW = {}


def hnd_priv_cmd(t, s, p):
    if not s[1] in GROUPCHATS:
        return
    if t in ['private','chat']:
        return
    if not p or p.isspace():
        return
    ss = p.split()
    cmd = p.lower()
    pr = str()
    
    if len(ss)>1:
        cmd = ss[0].lower()
        pr = ' '.join(ss[1:])
    if COMMAND_HANDLERS.has_key(cmd):
        if s[1] in COMMOFF and cmd in COMMOFF[s[1]]:
            return
        call_command_handlers(cmd, 'private', s, pr)

register_command_handler(hnd_priv_cmd, 'приват', ['все'], 0, 'Выполняет указанную команду с возвратом результатов в приват.', 'приват команда параметры', ['приват gis киев'])


def cmdhash(cmd):
    import inspect
    import hashlib
    hsh = None
    md5 = hashlib.md5()
    try:
        hsh = inspect.getsource(COMMAND_HANDLERS[cmd])
        md5.update(hsh)
        hsh = md5.hexdigest()
    except: pass
    return hsh

REPEAT_DICT = {}

def repeat_cmd_msg(r,t,s,p):
    jid = get_true_jid(s)
    if p.lower() in COMMANDS.keys() and p!='_':
        REPEAT_DICT[jid]=p.lower()

register_message_handler(repeat_cmd_msg)
    

def hnd_repeat_cmd(t, s, p):
    global REPEAT_DICT
    jid = get_true_jid(s)
    if not jid in REPEAT_DICT.keys():
        reply(t, s, u'Последняя команда не определена!\nПовтор последней команды работает только для команд без параметров, например: <анек>,<бор>;\n бот помнит последнюю команду до рестарта бота!')
        return
    call_command_handlers(REPEAT_DICT[jid], t, s, str())

register_command_handler(hnd_repeat_cmd, '_', ['все'], 0, 'Повтор последней команды.\nРаботает только для команд без параметров, например цитники типа бор, анекдот и тд.', '_', ['_'])

def updated_and_new(t, s, p):
    
    def dtbycmd(cmd):
        rep = ''
        try: f=inspect.getsourcefile(COMMAND_HANDLERS[cmd])
        except: pass
        tt=os.path.getmtime(f)
        rep = datetime.datetime.fromtimestamp(tt).strftime('%Y-%m-%d')#[%H:%M:%S]')
        return rep
    def gtlist():
        D = {}
        f = 0
        for x in COMMAND_HANDLERS.keys():
            try: f=inspect.getsourcefile(COMMAND_HANDLERS[x])
            except: pass
            D[x] = os.path.getmtime(f)
        return sorted(D.iteritems(), key=lambda x: x[1], reverse=True)
    
    db=eval(read_file(HASHCMD_FILE))
    rep=''
    mk=os.path.getctime(HASHCMD_FILE)
    n=0
    
    for x in gtlist():#COMMAND_HANDLERS.keys():
        x=x[0]
        if not x in db.keys():
            db[x]={'h':cmdhash(x),'t':time.time()}
            n+=1
            rep+=x+' - '+dtbycmd(x)+' (NEW) \n'#dtbycmd(x)+') '+x+' (NEW) \n'
        else:
            if cmdhash(x)!=db[x]['h']:
                db[x]={'h':cmdhash(x),'t':time.time()}
                n+=1
                rep+=x+' - '+dtbycmd(x)+u' (обновлено) \n'
    #if db[db.keys()[0]]['t']!=db[db.keys()[len(db)-1]]['t']:
    #    list = sorted(db, key = lambda key: db[key].get('t',0))
    #    list.reverse()
    #    if len(list)>20:
    #        list=list[:20]
    #    for x in list:
    #        n+=1
    #        rep+=dtbycmd(x)+') '+x+' '+dtbycmd(x)+'\n'
    if not rep or rep.isspace():
        reply(t, s, u'пока нету')
        return
    reply(t, s, rep)


register_command_handler(updated_and_new, 'новые команды', ['все'], 0, 'Показывает список новых и последних обновленных команд', 'новые команды', ['новые команды'])


def init_hash_cmd(*a):
    global UPDATED_AND_NEW
    db=eval(read_file(HASHCMD_FILE))
    if not db:
        t = time.time()
        
        for x in COMMAND_HANDLERS.keys():
            db[x]={'h': cmdhash(x),'t':t}
        write_file(HASHCMD_FILE, str(db))
        


register_stage0_init(init_hash_cmd)

def newcmd_msg(r, t, s, p):
    if not p:
        return
    if p.count(' ')>1:
        return
    if s[1] in GROUPCHATS and t in ['public','groupchat']:
        bn = get_bot_nick(s[1])
        if not p.count(bn):
            return
        for x in [bn+x for x in [':',',','>']]:
            p=p.replace(x,'')
        #if not p.split()[0].lower() if COMMANDS.keys() and not 
            
    ss = p.split()
    if not len(ss)>0:
        return
    if ss[0].lower() in COMMANDS:
        return
    try:
        if ' '.join(ss[:2]).lower() in COMMANDS: return
    except: pass
    if len(ss[0])<4 or len(ss[0])>30:
        return
    lenlike = [x for x in COMMANDS.keys() if len(ss[0])==len(x)]
    sp = []
    n = 0
    cmd = list(ss[0].lower())
    minlen = 2
    if len(cmd)<=5:
        minlen = 1
    for x in lenlike:
        a = list(x)
        notlike = 0
        ind = 0
        for c in a:
            if cmd[ind]==c:
                pass
            else:
                notlike+=1
            ind+=1
        if notlike!=0 and notlike <= minlen:
            sp.append(x)
    if not sp or len(sp)>1:
        return
    if sp[0].lower() in [u'свал',u'пшёл',u'рестарт']: return
    reply(t, s, u'Возможно, вы имели в виду -\n'+''.join(sp)+u' ?')
    time.sleep(1.5)
    rep = sp[0]
    c=''
    command=rep
    if len(ss)>1:
        c=ss[1]
    if s[1] in COMMOFF and command in COMMOFF[s[1]]:
        return
    else:
        call_command_handlers(command, t, s, unicode(c))
        INFO['cmd'] += 1
        


register_message_handler(newcmd_msg)

CMD_REPL={u' ':u' ',u'q':u'й',u'w':u'ц',u'e':u'у',u'r':u'к',u't':u'е',u'y':u'н',u'u':u'г',u'i':u'ш',u'o':u'щ',u'p':u'з',u'[':u'х',u']':u'ъ',u'a':u'ф',u's':u'ы',u'd':u'в',u'f':u'а',u'g':u'п',u'h':u'р',u'j':u'о',u'k':u'л',u'l':u'д',u';':u'ж',u'\'':u'э',u'z':u'я',u'x':u'ч',u'c':u'с',u'v':u'м',u'b':u'и',u'n':u'т',u'm':u'ь',u',':u'б',u'.':u'ю'}


def data_cmd_replace(data):
        global CMD_REPL
        rep=''
        for x in data:
                if x in CMD_REPL.keys():
                        rep+=CMD_REPL[x]
                else:
                        rep+=x
        return rep
                        
def cmd_repl(raw, type, source, parameters):
        try:
                if not parameters:
                        return
                if len(parameters)>50:
                        return
                parameters = parameters.lower()
                if parameters in COMMANDS.keys():
                        return
                if parameters.count(' '):
                        cmd=parameters.split()[0]
                        if cmd in COMMANDS.keys():
                                return
                if source[1] in GROUPCHATS:
                        if source[2]==get_bot_nick(source[1]):
                                return
                if source[2] and source[2]!=None:
                        cmd=data_cmd_replace(source[2])
                        if source[2].count(' '):
                                cmd=source[2].split()[0]
                                cmd=data_cmd_replace(cmd)
                        if cmd in COMMANDS.keys():
                                return
                rep=''
                c=''
                rep=data_cmd_replace(parameters)
                if not rep or rep.isspace():
                        return
                command=rep
                if rep.count(' '):
                        s=rep.split()
                        command=s[0]
                        c=' '.join(s[1:])
                if command in COMMANDS:
                        if source[1] in COMMOFF and command in COMMOFF[source[1]]:
                                return
                        else:
                                reply(type, source, u'Команду распознано как:\n'+rep)
                                time.sleep(1.5)
                                call_command_handlers(command, type, source, unicode(c))
                                INFO['cmd'] += 1

        except:
                pass

register_message_handler(cmd_repl)
    
