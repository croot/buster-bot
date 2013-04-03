#===istalismanplugin===
# -*- coding: utf-8 -*-

DICT_FOR_TIMER = {}

MEMORY_SELFAFLOOD = 'dynamic/selfaflood.txt'

db_file(MEMORY_SELFAFLOOD, dict)

def selfaflood_msg(r, t, s, p):
    if not s[1] in GROUPCHATS.keys() or not t in ['public', 'groupchat']:
        return
    if s[1] in PERSONAL_CMD.keys():
        return
    if not s[2] or s[2]==get_bot_nick(s[1]):
        return
    if not p:
        return
    if p.split()[0].lower() in COMMANDS.keys():
        DICT_FOR_TIMER[s[2]]=time.time()
    if len(p)>=2 and p.split()[0][:-1] in DICT_FOR_TIMER.keys():
        if time.time()-DICT_FOR_TIMER[p.split()[0][:-1]]<1:
            time.sleep(2)
            msg(s[3], s[1], u'В вашей конференции зафиксирован бот с аналогичной командой,\nчтобы не засорять чат перехожу в тихий режим - \nвыполнение команд возможно только по обращению на ник!')
            PERSONAL_CMD[s[1]]={}
            write_file(MEMORY_SELFAFLOOD, str(PERSONAL_CMD))

def selfaflood_load(*arg):
    global PERSONAL_CMD
    global MEMORY_SELFAFLOOD
    if not PERSONAL_CMD:
        db=eval(read_file(MEMORY_SELFAFLOOD))
        PERSONAL_CMD = db.copy()

register_stage0_init(selfaflood_load)

register_message_handler(selfaflood_msg)
