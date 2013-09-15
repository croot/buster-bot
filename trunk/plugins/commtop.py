# -*- coding: utf-8 -*-

COMMTOP = {}

COMMTOP_CALC = 0

COMMTOP_FILE = 'dynamic/commtop.txt'

db_file(COMMTOP_FILE, dict)

from operator import itemgetter

def msg_commtop(r, t, s, p):
    global COMMTOP
    global COMMTOP_CALC
    if not p or not len(p)>0:
        return
    bot_nick = ''
    if s[1] in GROUPCHATS:
        bot_nick = get_bot_nick(s[1])
        for x in [bot_nick+x for x in [':',',','>']]:
            p = p.replace(x,'')
    ss = p.split()
    cmd = ss[0].lower()
    cmd = cmd.strip()
    if cmd in COMMANDS:
        COMMTOP_CALC += 1
        if cmd in COMMTOP:
            COMMTOP[cmd]+=1
        else:
            COMMTOP[cmd] = 1
        if COMMTOP_CALC>=10:
            COMMTOP_CALC = 0
            write_file(COMMTOP_FILE, str(COMMTOP))

register_message_handler(msg_commtop)

def commtop_init(*n):
    global COMMTOP
    global COMMTOP_FILE
    if not COMMTOP:
        COMMTOP = eval(read_file(COMMTOP_FILE))

register_stage0_init(commtop_init)

def hnd_commtop(t, s, p):
    rep = u'\n№ | Kоманда  | Cколько раз использовалась\n'
    sor = sorted(COMMTOP.iteritems(), key=itemgetter(1))
    sor.reverse()
    for x in sor:
        rep+=str(sor.index(x)+1)+') '+ x[0]+' - '+str(x[1])+'\n'
        if p.isdigit() and (sor.index(x)+1)==int(p):
            break
    reply(t, s, rep)


MEMCMD_GLOB = {}

MEMCMD_CALC = 0

MEMCMD_FILE = 'dynamic/memcmd.txt'

db_file(MEMCMD_FILE, dict)


def memo_cmd_set(t, s, p):
    if not p:
        reply(t, s, '\n'.join([x+' - '+MEMCMD_GLOB[x]['msg'] for x in MEMCMD_GLOB.keys()]))
        return
    ss = p.split()
    if ss[0].lower() in COMMANDS.keys():
        if len(ss)==1:
            if ss[0].lower() in MEMCMD_GLOB.keys():
                del MEMCMD_GLOB[ss[0].lower()]
                reply(t, s, u'Удалил!')
                write_file(MEMCMD_FILE, str(MEMCMD_GLOB))
                return
        else:
            MEMCMD_GLOB[ss[0].lower()] = {'list':[], 'msg':' '.join(ss[1:])}
            write_file(MEMCMD_FILE, str(MEMCMD_GLOB))
            reply(t, s, u'Добавил!')

def memo_msg_reg(r, t, s, p):
    global MEMCMD_GLOB
    global MEMCMD_CALC
    if not p or not len(p)>0:
        return
    bot_nick = ''
    if s[1] in GROUPCHATS:
        bot_nick = get_bot_nick(s[1])
        for x in [bot_nick+x for x in [':',',','>']]:
            p = p.replace(x,'')
    ss = p.split()
    cmd = ss[0].lower()
    cmd = cmd.strip()
    jid = get_true_jid(s)
    if cmd in MEMCMD_GLOB and not jid in MEMCMD_GLOB[cmd]['list']:
        MEMCMD_CALC += 1
        MEMCMD_GLOB[cmd]['list'].append(jid)
        time.sleep(3)
        reply(t, s, MEMCMD_GLOB[cmd]['msg'])
        if MEMCMD_CALC>=10:
            write_file(MEMCMD_FILE, str(MEMCMD_GLOB))
            MEMCMD_CALC = 0

register_message_handler(memo_msg_reg)
    
def cmdmem_init(*n):
    global MEMCMD_GLOB
    global MEMCMD_FILE
    if not MEMCMD_GLOB:
        MEMCMD_GLOB = eval(read_file(MEMCMD_FILE))

register_stage0_init(cmdmem_init)

register_command_handler(memo_cmd_set, 'компамятка', ['все'], 40, 'Добавляет определенное сообщение после использования юзером указанной команды.', 'комтпамятка <команда> <текст>', ['компамятка пинг Более детальный пинг по команде - турбопинг'])
register_command_handler(hnd_commtop, 'комтоп', ['все'], 0, 'Выводит топ команд', 'комтоп', ['комтоп'])
        
