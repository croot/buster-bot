#===istalismanplugin===
# -*- coding: utf-8 -*-

DICT_FOR_TIMER = {}

selfaflood_tim = {}

MEMORY_SELFAFLOOD = 'dynamic/selfaflood.txt'

db_file(MEMORY_SELFAFLOOD, dict)

#SELFAFLOOD_DENY = 'dynamic/selfaflooddeny.txt'

#db_file(SELFAFLOOD_DENY, dict)

def selfaflood_msg_(r, t, s, p):
    global PERSONAL_CMD
    global selfaflood_tim
    if not s[1] in GROUPCHATS.keys() or not t in ['public', 'groupchat']:
        return
    if s[1] in PERSONAL_CMD.keys():
        return
    if s[2] == get_bot_nick(s[1]):
        return
    if not p:
        return
    if p.split()[0].lower() in COMMANDS.keys():
        DICT_FOR_TIMER[s[2]]=time.time()
    if len(p)>=2 and p.split()[0][:-1] in DICT_FOR_TIMER.keys() and p.split()[0][:-1]!=get_bot_nick(s[1]):
        if time.time()-DICT_FOR_TIMER[p.split()[0][:-1]]<1:
            time.sleep(2)
            if not s[1] in selfaflood_tim.keys():
                msg(s[3], s[1], u'В вашей конференции зафиксирован бот с аналогичной командой,\nчтобы не засорять чат перехожу в тихий режим - \nвыполнение команд возможно только по обращению на ник!')
            selfaflood_tim[s[1]] = time.time()
            PERSONAL_CMD[s[1]]={}
            write_file(MEMORY_SELFAFLOOD, str(PERSONAL_CMD))

def selfaflood_load(*arg):
    global PERSONAL_CMD
    global MEMORY_SELFAFLOOD
    if not PERSONAL_CMD:
        db=eval(read_file(MEMORY_SELFAFLOOD))
        PERSONAL_CMD = db.copy()

def selfaflood_cmd(t, s, p):
    if not s[1] in GROUPCHATS:
        return
    global PERSONAL_CMD
    if not s[1] in PERSONAL_CMD.keys():
        PERSONAL_CMD[s[1]]=True
    if not PERSONAL_CMD[s[1]]:
        
        PERSONAL_CMD[s[1]] = 1
        reply(t, s, u'Включил выполнение команд без обращения по нику!')
    else:
        PERSONAL_CMD[s[1]] = 0
        reply(t, s, u'Отключил выполнение команд без обращения по нику!')
    write_file(MEMORY_SELFAFLOOD, str(PERSONAL_CMD))

register_command_handler(selfaflood_cmd, 'sflood', ['админ','мук','все'], 20, 'Включает \октлючает выполнение команд в паблике без обращения по нику.', 'sflood', ['sflood'])

register_stage0_init(selfaflood_load)

register_message_handler(selfaflood_msg_)
