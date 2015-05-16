# -*- coding: utf-8 -*-

import datetime

NICKS = {}
NICKS_TIMER = 0
NICKS_FILE = 'dynamic/nicks_.txt'

#db_file(NICKS_FILE, dict)


def hnd_join_nicks(g, n, afl, role, cl):
        global NICKS
        global NICKS_TIMER
        global NICKS_FILE
        jid = get_true_jid(g+'/'+n)
        if not jid in NICKS:
                NICKS[jid] = {'n':{},'t':time.time(),'m':0, 'last':0}
        if not n in NICKS[jid]['n']:
                NICKS[jid]['n'][n] = {}
        NICKS[jid]['last']=time.time()
        if time.time() - NICKS_TIMER > 1200:
                NICKS_TIMER = time.time()
                write_file(NICKS_FILE, str(NICKS))

register_join_handler(hnd_join_nicks)

def hnd_msg_nicks(st, t, s, p):
        global NICKS
        jid = get_true_jid(s)
        if jid in NICKS:
                NICKS[jid]['m']+=1

register_message_handler(hnd_msg_nicks)


def hnd_nicks_inf(t, s, p):
        if not s[1] in GROUPCHATS:
                return
        if p.lower() == u'я':
                p = s[2]
        if p.lower() == u'ты':
                reply(t, s, u'Я бот Бастер')
                return
        rep = ''
        #if not p in GROUPCHATS[s[1]]:
        #        pass
        n = 0
        for x in NICKS:
                if p in NICKS[x]['n']:
                        n+=1
                        rep+=u'Информаци о '+p+u':\nНики - '+', '.join(NICKS[x]['n'].keys())+u'\nПервый раз увидел его в '+datetime.datetime.fromtimestamp(NICKS[x]['t']).strftime('%Y-%m-%d %H:%M:%S')
                        rep+=u'\nСообщений - '+str(NICKS[x]['m'])+u'\nПоследний раз видел в '+datetime.datetime.fromtimestamp(NICKS[x]['t']).strftime('%Y-%m-%d %H:%M:%S')+'\n'

        if rep.isspace():
                return
        reply(t, s, (u'Совпадений в никах '+str(n)+'\n' if n>1 else '')+rep)

register_command_handler(hnd_nicks_inf, 'кто', ['все'], 0, 'Показывает информацию о нике.', 'кто <ник>', ['кто вася'])

	
