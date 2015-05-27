#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  turn_plugin.py

#  Initial Copyright © 2008 dimichxp <dimichxp@gmail.com>
#  Idea © 2008 Als <Als@exploit.in>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

global_en2ru_table = dict(zip(u"qwertyuiop[]asdfghjkl;'zxcvbnm,./`йцукенгшщзхъфывапролджэячсмитьбю.ёQWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>?~ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё", u"йцукенгшщзхъфывапролджэячсмитьбю.ёqwertyuiop[]asdfghjkl;'zxcvbnm,./`ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,ЁQWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>?~"))

turn_msgs={}

_eng_chars = u"~!@#$%^&qwertyuiop[]asdfghjkl;'zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:\"|ZXCVBNM<>?"
_rus_chars = u"ё!\"№;%:?йцукенгшщзхъфывапролджэячсмитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭ/ЯЧСМИТЬБЮ,"
_trans_table = dict(zip(_eng_chars, _rus_chars))
 
def fix_layout(s):
    return u''.join([_trans_table.get(c, c) for c in s])

def handler_turn_last(type, source, parameters):
	nick=source[2]
	groupchat=source[1]
	jid=get_true_jid(groupchat+'/'+nick)
	nc=''
	if parameters:
		reply(type,source,fix_layout(parameters))
	else:
		if turn_msgs[groupchat][jid] is None:
			reply(type,source,u'а ты ещё ничего не говорил')
			return
		if turn_msgs[groupchat][jid] == u'turn':
			reply(type,source,u'ага, щаззз')
			return
		tmsg=turn_msgs[groupchat][jid]
		try:
                    kk = tmsg.split()
                    if kk[0][:-1] in GROUPCHATS[source[1]]:
                        tmsg = ' '.join(kk[1:])
                        nc = kk[0]
                except: pass
		reply(type,source,nc+fix_layout(tmsg))

def handler_turn_save_msg(raw, type, source, body):
	time.sleep(1)
	nick=source[2]
	groupchat=source[1]
	jid=get_true_jid(groupchat+'/'+nick)
	if not groupchat in turn_msgs and groupchat in GROUPCHATS:
                turn_msgs[groupchat]={}
                turn_msgs[groupchat][jid]=None
	if groupchat in turn_msgs.keys():
		if jid in turn_msgs[groupchat].keys() and jid != groupchat and jid != JID:
			turn_msgs[groupchat][jid]=body

def handler_turn_join(groupchat, nick, aff, role, cljid):
	jid=get_true_jid(groupchat+'/'+nick)
	if not groupchat in turn_msgs.keys():
		turn_msgs[groupchat] = {}
	if not jid in turn_msgs[groupchat].keys():# and jid != JID:
		turn_msgs[groupchat][jid]=None


register_message_handler(handler_turn_save_msg)
register_join_handler(handler_turn_join)
register_command_handler(handler_turn_last, 'turn', ['мук','все'], 10, 'Переключает раскладку для последнего сообщения от юзера вызвавшего команду.', 'turn', ['turn'])
