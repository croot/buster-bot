#===istalismanplugin===
# -*- coding: utf-8 -*-


def handler_commoff(type,s,p):
	if not s[1] in GROUPCHATS:
		reply(type, s, u'это возможно только в конференции')
		return
	file='dynamic/'+s[1]+'/commoff.txt'
	get_commoff(s[1])
	na=[u'доступ',u'eval',u'логин',u'логаут',u'!stanza',u'unglobacc',u'свал',u'рестарт',u'globacc',u'команды',u'sh',u'exec',u'commoff',u'common']
	if p:
                if not p in COMMANDS:
                        reply(type, s, u'Нет такой команды!')
                        return
                if p in na:
                        reply(type, s, u'Эту команду отключить невозможно!')
                        return
                if p in COMMOFF[s[1]]:
                        reply(type, s, u'Эта команда уже отключена ранее!')
                        return
                db=eval(read_file(file))
                db[p]={}
                write_file(file, str(db))
                reply(type, s, u'Отключил '+p)
                get_commoff(s[1])
        else:
                reply(type, s, ', '.join(COMMOFF[s[1]].keys()))

def handler_common(type,s,p):
	if not s[1] in GROUPCHATS:
		reply(type, source, u'это возможно только в конференции')
		return
	file='dynamic/'+s[1]+'/commoff.txt'
	get_commoff(s[1])
	if p:
                if not p in COMMANDS:
                        reply(type, s, u'Нет такой команды!')
                        return
                if not p in COMMOFF[s[1]]:
                        reply(type, s, u'Эта команда не отключалась!')
                        return
                db=eval(read_file(file))
                if p in db:
                        del db[p]
                write_file(file, str(db))
                reply(type, s, u'Включил '+p)
                get_commoff(s[1])

def get_commoff(gch):
        global COMMOFF
        COMMOFF[gch]={}
        file='dynamic/'+gch+'/commoff.txt'
        check_file(gch, 'commoff.txt')
        db=eval(read_file(file))
        if db:
                COMMOFF[gch]=db


register_command_handler(handler_commoff, 'commoff', ['админ','мук','все'], 20, 'Отключает определённые команды для текущей конференции, без параметров показывает список уже отключенных команд.', 'commoff [команды]', ['commoff','commoff тык диско версия пинг'])
register_command_handler(handler_common, 'common', ['админ','мук','все'], 20, 'Включает определённые команды для текущей конференции.', 'common [команды]', ['common тык диско версия пинг'])

register_stage1_init(get_commoff)
