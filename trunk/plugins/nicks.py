# -*- coding: utf-8 -*-

import datetime


NICKS_TIMER = 0
NICKS_FILE = 'dynamic/nicks_.txt'

db_file(NICKS_FILE, dict)


NICKS = eval(read_file(NICKS_FILE))

def hnd_join_nicks(g, n, afl, role, cl):
        global NICKS
        global NICKS_TIMER
        global NICKS_FILE
        jid = get_true_jid(g+'/'+n)
        if not g in NICKS:
                NICKS[g]={}
        if not jid in NICKS[g]:
                NICKS[g][jid] = {'n':{},'t':time.time(),'m':0, 'last':0}
        if not n in NICKS[g][jid]['n']:
                NICKS[g][jid]['n'][n] = {}
        NICKS[g][jid]['last']=time.time()
        if time.time() - NICKS_TIMER > 1200:
                NICKS_TIMER = time.time()
                write_file(NICKS_FILE, str(NICKS))

register_join_handler(hnd_join_nicks)


def hnd_lev_nicks(g, n, reason, code, cl):
        global NICKS
        global NICKS_TIMER
        global NICKS_FILE
        jid = get_true_jid(g+'/'+n)
        if not g in NICKS:
                NICKS[g]={}
        try:
                if not 'all' in NICKS[g][jid]:
                        NICKS[g][jid]['all']=0
                NICKS[g][jid]['all']+=time.time()-NICKS[g][jid]['last']
        except:
                pass

register_leave_handler(hnd_lev_nicks)               
                

def hnd_msg_nicks(st, t, s, p):
        global NICKS
        jid = get_true_jid(s)
        try:
                if jid in NICKS[s[1]]:
                        NICKS[s[1]][jid]['m']+=1
        except:
                pass

register_message_handler(hnd_msg_nicks)


def hnd_nicks_inf(t, s, p):
        if not s[1] in GROUPCHATS:
                return
        if p.lower() == u'я':
                p = s[2]
        if p.lower() == u'ты':
                reply(t, s, u'Я бот Бастер')
                return
        ishere = False
        rep = ''
        #if not p in GROUPCHATS[s[1]]:
        #        pass
        n = 0
        for x in NICKS[s[1]]:
                ishere = False
                if x.count('@conference.'):
                        continue
                if p in NICKS[s[1]][x]['n']:
                        if p in GROUPCHATS[s[1]] and GROUPCHATS[s[1]][p]['jid']==x and GROUPCHATS[s[1]][p]['ishere']:
                                ishere = True
                        n+=1
                        rep+=(str(n)+') ' if n>1 else u'Информация о ')+p+u':\nНики - '+', '.join(NICKS[s[1]][x]['n'].keys())+u'\nВпервые увидел: '+datetime.datetime.fromtimestamp(NICKS[s[1]][x]['t']).strftime('%Y-%m-%d')
                        rep+=u'\nСообщений - '+str(NICKS[s[1]][x]['m'])+u'\nПоследний раз видел: '+(datetime.datetime.fromtimestamp(NICKS[s[1]][x]['last']).strftime('%m-%d %H:%M:%S') if not ishere else u'Онлайн прямо сейчас')+'\n'
                        rep+=u'Всего провел времени в конфе - '+timeElapsed(NICKS[s[1]][x].get('all',0))+'\n'

        if rep.isspace():
                return
        reply(t, s, (u'Совпадений в никах '+str(n)+'\n' if n>1 else '')+rep)

register_command_handler(hnd_nicks_inf, 'кто', ['все'], 0, 'Показывает информацию о нике.', 'кто <ник>', ['кто вася'])

	
