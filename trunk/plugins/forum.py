# -*- coding: utf-8 -*-

if not 'DIGIT_MENU' in globals().keys():
        DIGIT_MENU = {}

        
FORUM = {}
FORUM_NICK = {}
USER_FORUM = {}
GENERAL_FORUM = 'dynamic/forum.txt'
COPY_FORUM = 'dynamic/copy_forum.txt'
db_file(GENERAL_FORUM, dict)
db_file(COPY_FORUM, dict)

FORUM_PLUS = {}

FORUM_WHEREI = {}

#FORUM = {(u'Тема пра зоебись',u'User'):{(u'User',u'Text',time.time()):{}}}

#sorted([(u'User',u'Text',u'Time'),(u'User',u'Text',u'Time')], key=lambda x: x[2])

def frmt(t):
    return datetime.datetime.fromtimestamp(t).strftime('%H:%M:%S %m/%d')


def subject_last_activ(subject, all=0):
    #all = 3 время первого сообщения|создания темы
    #all = 0 время последнего поста в теме
    #all = 1 список постов
    if not subject in FORUM:
        return None
    list = sorted(FORUM[subject].keys(), key=lambda x: x[2])
    if all==3:
        return datetime.datetime.fromtimestamp(list[0][2]).strftime('%H:%M:%S %m/%d')
    list.reverse()
    return (list[0][2] if not all else list)


def show_frm_subject():
    d = {}
    for x in FORUM.keys():
        d[x]=subject_last_activ(x)
    list = sorted(d.items(), key = lambda x: x[1])
    list.reverse()
    return list


def hnd_make_forum(t, s, p):
    if len(p)>1 and p[:1]==u'#':
        reply(t, s, u'# - запрещенный символ в начале!')
        return
    c = p.split('#')
    jid = get_true_jid(s)
    nick = FORUM_NICK.get(jid, jid.split('@')[0])
    if not p or len(c)<2:
        reply(t, s, u'Введите параметры: тема # сообщение. прим. Привет # всем куку, идемте бухать')
        return
    sub = c[0]
    if len(sub)<3:
        reply(t, s, u' Название темы может содержать не менее трех символов!')
        return
    if len(sub)>100:
        reply(t, s, u' Название темы может содержать максимум 100 символов!')
        return
    if len(c[1])>500:
        reply(t, s, u' Сообщение не более 500 символов!')
        return
    for x in FORUM.keys():
        if x[0].lower() == sub.lower():
            reply(t, s, u'Такая тема уже есть!')
            return
    FORUM[(sub, nick)]={}
    FORUM[(sub, nick)][(nick, c[1], time.time())] = {}
    reply(t, s, u'Тема успешно создана!')
    write_file(GENERAL_FORUM, str(FORUM))
        
register_command_handler(hnd_make_forum, 'f+', ['все','jabber'], 0, 'Создает тему в виртуальном форуме бота', 'f+ Тема # сообщение', ['f+ Васе срочно! # Вася идем бухать!'])


def hnd_forum_msg(t, s, p):
    if not p or p.isspace():
        return
    jid = get_true_jid(s)
    c = str()
    global FORUM_WHEREI
    global FORUM_NICK
    nick = FORUM_NICK.get(jid, jid.split('@')[0])
    if not jid in FORUM_WHEREI:
        reply(t, s, u'Чтобы написать войдите в тему форума, просмотр тем - f')
        return
    sub = FORUM_WHEREI[jid]
    if not sub in FORUM.keys():
        reply(t, s, u'Тема не найдена!')
        return
    
    if jid in GLOBACCESS.keys() and GLOBACCESS[jid]>30 and p.lower() in [u'close',u'open',u'del',u'all']:
        if p.lower() == u'close':
            c = FORUM[sub]
            FORUM[('#'+sub[0], sub[1])]={}
            for m in c:
                FORUM[('#'+sub[0], sub[1])][m]={}
            del FORUM[sub]
            reply(t, s, u'Тема закрыта!')
        if p.lower() == u'del':
            del FORUM[FORUM_WHEREI[jid]]
            reply(t, s, u'Тема удалена!')
        if p.lower() == u'all':
            for x in FORUM.keys():
                if FORUM[x][1]==FORUM[sub][1]:
                    del FORUM[x]
            reply(t, s, u'Все темы пользователя удалены!')
        write_file(GENERAL_FORUM, str(FORUM))
        return
    if sub[0][:1]==u'#':
        reply(t, s, u'Тема закрыта!')
        return
    if p==u'test123':
        for x in range(23):
            FORUM[sub][(nick, str(x), time.time())] = {}
    FORUM[sub][(nick, p, time.time())] = {}
    write_file(GENERAL_FORUM, str(FORUM))
    reply(t, s, u'Сообщение добавлено!')
    del FORUM_WHEREI[jid]
        
register_command_handler(hnd_forum_msg, 'm+', ['все'], 0, 'Используется чтобы написать в виртуальном форуме бота', 'm+ <сообщение>', ['m+ Ахуеть дайте две!'])
   

def frm_top(th):
    if topic:
        pass
    
def hnd_forum(t, s, p, n=0):
    global FORUM
    global GENERAL_FORUM
    global USER_FORUM
    global FORUM_WHEREI
    global FORUM_PLUS
    
    jid = get_true_jid(s)
    fn = inspect.stack()[0][3]
    rep = ''
    rep2 = ''
    n = 0
    if p == '0' and jid in FORUM_PLUS.keys():
        reply(t, s, FORUM_PLUS[jid])
        return
    if not jid in USER_FORUM.keys() or not p:# or p==u'дальше':
        DIGIT_MENU[jid]=fn
        rep += u'Список тем:\n'
        USER_FORUM[jid]={}
        list = show_frm_subject()
        
        for x in list:
            x=x[0]
            n+=1
            USER_FORUM[jid][str(n)]=x
            if n>10:
                rep2+=str(n)+'. '+subject_last_activ(x, all=3)+' '+x[1]+'\n'+x[0]+' ('+str(len(FORUM[x]))+')\n'
            else:
                rep+=str(n)+'. '+subject_last_activ(x, all=3)+' '+x[1]+'\n'+x[0]+' ('+str(len(FORUM[x]))+')\n'
            
                
                
        if n>10:
            rep+=u'\n0 чтобы читать дальше (ноль)\n'
            FORUM_PLUS[jid]=rep2
                
        rep+=u'\nДля просмотра темы пишем ее номер, напр. 1\nЧтобы создать тему смотрим помощь f+'
        reply(t, s, (rep if len(FORUM.keys())>0 else u'На форуме нет тем! \nЧтобы создать смотрим помощь f+'))
        return
    if jid in USER_FORUM.keys() and p in USER_FORUM[jid]:
        FORUM_WHEREI[jid]=USER_FORUM[jid][p]
        rep += USER_FORUM[jid][p][0]+'\n'
        
        list = subject_last_activ(USER_FORUM[jid][p], all=1)
        
        for x in list:
            n+=1
            #(u'User',u'Text',u'Time')
            
            if n>10:
                rep2+='['+frmt(x[2])+'] '+x[0]+':\n'+x[1]+'\n'
            else:
                rep+='['+frmt(x[2])+'] '+x[0]+':\n'+x[1]+'\n'

        if n>10:
            rep+=u'\n0 чтобы читать дальше (ноль)\n'
            FORUM_PLUS[jid]=rep2
        rep+=u'\n чтобы написать используем m+ ваш текст'
        reply(t, s, rep)
        del USER_FORUM[jid]



register_command_handler(hnd_forum, 'f', ['все','jabber'], 0, 'Просмотр виртуального форума бота.', 'f', ['f'])



def forum_init(*a):
    global FORUM
    global GENERAL_FORUM
    if not FORUM:
        c = eval(read_file(GENERAL_FORUM))
        FORUM = c.copy()

register_stage0_init(forum_init)


    
