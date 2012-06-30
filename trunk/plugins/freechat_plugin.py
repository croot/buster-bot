# -*- coding: utf-8 -*-

CMD_AFLOOD = {}

def msg_twice_cmd(r, t, s, p):
    global CMD_AFLOOD
    if not s[1] in GROUPCHATS or not t in ['public','groupchat']: return
    if not p: return
    if not p.split()[0].lower() in COMMANDS: return
    if not s[1] in CMD_AFLOOD:
        CMD_AFLOOD[s[1]]={}
    if not p.split()[0].lower() in CMD_AFLOOD[s[1]]:
        CMD_AFLOOD[s[1]][s[2]]={'t':time.time(),'cmd':p.split()[0].lower()}

def msg_catch_twice(r, t, s, p):
    global CMD_AFLOOD
    if not s[1] in GROUPCHATS or not t in ['public','groupchat']: return
    if not p or not s[1] in CMD_AFLOOD: return
    if s[2]==get_bot_nick(s[1]): return
    nick=''
    if p.split()>1:
        nick=p.split()[0]
        nick=nick[:-1]
    if nick in CMD_AFLOOD[s[1]]:
        if time.time() - CMD_AFLOOD[s[1]][nick]['t']<0.8:
            print 'GOGI!!!\n'

register_message_handler(msg_twice_cmd)
register_message_handler(msg_catch_twice)

#register_command_handler(hnd_freechat, '!чат', ['все'], 0, 'Сервис чатов', '!чат', ['!чат'])
#register_command_handler(hnd_freechat, '!chat', ['все'], 0, 'Сервис чатов', '!chat', ['!chat'])
