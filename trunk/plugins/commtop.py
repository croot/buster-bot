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
    ss = p.split()
    cmd = ss[0].lower()
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

def hnd_commtop(t, s, p):
    rep = u'\n№ | Kоманда  | Cколько раз использовалась\n'
    sor = sorted(COMMTOP.iteritems(), key=itemgetter(1))
    sor.reverse()
    for x in sor:
        rep+=str(sor.index(x)+1)+') '+ x[0]+' - '+str(x[1])+'\n'
    reply(t, s, rep)


register_command_handler(hnd_commtop, 'комтоп', ['все'], 0, 'Выводит топ команд', 'комтоп', ['комтоп'])
        
