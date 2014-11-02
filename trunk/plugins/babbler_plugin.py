# -*- coding: utf-8 -*-

BABBLER_FILE = 'dynamic/babbler.txt'

check_file(file='babbler.txt')

BABBLER = {}

BABBLER_MSG = {}

BABBLER_NN = {}

def babbler_msg(r, t, s, p):
    if not s[1] in GROUPCHATS or not p or not t in ['groupchat','public']:
        return
    if len(p)>250: return
    if p.split()[0].lower() in COMMANDS:
        return
    if not p.count(' '):
        return
    
    nick = p.split()[0]
    nick = nick[:-1]
    nc = True
    
    if not nick in GROUPCHATS[s[1]]:
        nc = False

    if len(p)==len(nick): return
    
    db = eval(read_file(BABBLER_FILE))

    bn = get_bot_nick(s[1])
    if nick == bn or s[2] == bn: return
    
    if not s[1] in BABBLER:
        BABBLER[s[1]]={}

    p = (' '.join(p.split()[1:]) if nc else p)
    if not nc and not p.count(': '):
        if not s[1] in BABBLER_NN:
            BABBLER_NN[s[1]]={}
            
        
        list = [ x for x in BABBLER_NN[s[1]].keys() if BABBLER_NN[s[1]][x]['nick']!=s[2] and time.time() - BABBLER_NN[s[1]][x]['time']>5 and time.time() - BABBLER_NN[s[1]][x]['time']<120 and not BABBLER_NN[s[1]][x]['answ']]
        if not list:
            BABBLER_NN[s[1]][p] = {'time':time.time(),'answ':'','nick':s[2]}
            return
        list = list[0]
        if not list in db.keys():
            db[list] = []
        db[list].append(p)
        write_file(BABBLER_FILE, str(db))
        try:
            del BABBLER_NN[s[1]][list]
        except: pass
        return
                               
    if s[2] in BABBLER[s[1]] and nick==BABBLER[s[1]][s[2]]['from']:
        if time.time() - BABBLER[s[1]][s[2]]['time']<10:
            del BABBLER[s[1]][s[2]]
            return
        if not BABBLER[s[1]][s[2]]['body'] in db:
            db[BABBLER[s[1]][s[2]]['body']]=[]
        db[BABBLER[s[1]][s[2]]['body']].append(p)
        write_file(BABBLER_FILE, str(db))
        try: del BABBLER[s[1]][s[2]]
        except: pass
        return
    BABBLER[s[1]][nick]={'time':time.time(),'body':p,'from':s[2]}
    for x in BABBLER[s[1]].keys():
        if time.time()-BABBLER[s[1]][x]['time']>180:
            del BABBLER[s[1]][x]

def db_base_trash(t, s, p):
    emp = 0
    nk = 0
    rep = ''
    for x in BABBLER_MSG.keys():
        if x.isspace():
            emp += 1
            del BABBLER_MSG[x]
        else:
            for c in BABBLER_MSG[x]:
                if c.count(': '):
                    BABBLER_MSG[x].remove(c)
                    nk+=1
                    rep+=c+'\n'
    if BABBLER_MSG:
        write_file(BABBLER_FILE, str(BABBLER_MSG))
    reply(t, s, u'Удалено '+str(nk)+u' объектов содержащих ники\n'+rep)

def db_babbler(t, s, p):
    rep = ''
    txt = eval(read_file(BABBLER_FILE))
    rd = random.choice(txt.keys())
    cnt = (False if len(p)<3 or p[-1:]!='*' else True)
    if cnt:
        p = p[:-1]

    if p == 'del':
        db_base_trash(t, s, p)
        return
    if p == 'random':
        reply(t, s, rd+' -> '+' | '.join(txt[rd])+';\n')
        return
    for x in txt:
        if cnt and p and not x.count(p):
                continue
        if not cnt and p and not x.lower()==p:
            continue
        try: rep+=x+' = '+'; '.join(txt[x])+';\n'
        except: pass
    reply(t, s, str(len(txt))+':\n '+rep)

def babbler_init(cljid):
    global BABBLER_MSG
    txt = eval(read_file(BABBLER_FILE))
    BABBLER_MSG = txt.copy()

BABBLER_MEM = {}

BABBLER_REP = {}

def babbler_answ(r, t, s, p):
    global BABBLER_MSG
    global BABBLER_REP
    if not p or p=='[no text]': return
    if time.time()-INFO['start']<120:
        return
    if s[1] in GROUPCHATS:
        if not s[2] or s[2].isspace():
            return
        if p.split()>1:
            if p.split()[0][:-1] in GROUPCHATS[s[1]] and p.split()[0][:-1]!=get_bot_nick(s[1]): return
    if p.split()[0].lower() in COMMANDS: return
    n = random.randrange(0, 13)
    if n != 1: return
    try:
        if get_true_jid(s) in MAFIA.keys(): return
    except: pass
    p = p.replace(get_bot_nick(s[1]),'')
    p = p.strip()
    m = ''
    if p in BABBLER_MSG.keys():
        m=random.choice(BABBLER_MSG[p])
    if not s[1] in BABBLER_REP:
        BABBLER_REP[s[1]] = {'t':time.time(),'m':m}
    else:
        if BABBLER_REP[s[1]]['m']==m: return
        if time.time() - BABBLER_REP[s[1]]['t']<120: return
    BABBLER_REP[s[1]]['m'] = m
    BABBLER_REP[s[1]]['t'] = time.time()
    if m:
        tm=random.randrange(7, 17)
        time.sleep(tm)
        reply(t, s, m)
    
register_command_handler(db_babbler, 'db', ['все'], 0, 'Команда для поиска по базе болтуна.\n Символ * в коце параметров - ищет строгое соответствие ключевой фразе,\n без * ищет предложения содержащие параметерт.\nКлюч del - очищает базу от мусора.', 'db', ['db','db привет','db random','db привет*'])        
register_message_handler(babbler_msg)
register_message_handler(babbler_answ)
register_stage0_init(babbler_init)

