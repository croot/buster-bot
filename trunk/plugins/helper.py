# -*- coding: utf-8 -*-

HELPER_TIME = 0
HELPER_FILE = 'dynamic/helper.txt'
HELPER_GLOB = {}

db_file(HELPER_FILE, dict)

try: HELPER_GLOB = eval(read_file(HELPER_FILE))
except: HELPER_GLOB = {}

#HELPER_MSG = [u'Узнать мои команды можно написав команды все, получить помощь по команде - помощь и название команды!',u'Я бесплатный бот, завести меня можно дав команду зайти и ваш адрес чата!',u'Бесплатная игра мафия прямо с чата - пиши !мафия и зови друзей!',u'UIN бота в ICQ - 646210729']

def hnd_autohelper_work(t, s, p):
    global HELPER_FILE
    global HELPER_GLOB
    if not s[1] in GROUPCHATS.keys(): return
    db = eval(read_file(HELPER_FILE))
    if not s[1] in db.keys():
        reply(t, s, u'Помощь по командам в статусе Oтключена!')
        db[s[1]]={}
    else:
        reply(t, s, u'Помощь по командам в статусе Bключена!')
        del db[s[1]]
    HELPER_GLOB = db.copy()
    write_file(HELPER_FILE, str(db))
    
def hnd_autohelper(r, t, s, p):
    global HELPER_TIME
    global HELPER_GLOB
    f = 'dynamic/chatroom.list'
    if time.time()-HELPER_TIME>1800:
        HELPER_TIME = time.time()
        db = eval(read_file(f))
        list = [x for x in COMMANDS.keys() if COMMANDS[x]['access']<31 and len(COMMANDS[x]['desc'])>3]
        list = [x for x in list if not x in [u'пинг',u'тест',u'бан',u'кик',u'админ',u'никто',u'унбан']]
        for x in db.keys():
            for c in db[x].keys():
                if c in HELPER_GLOB.keys(): continue
                cmd = random.choice(list)
                p = domish.Element(('jabber:client', 'presence'))
                p['to'] = u'%s/%s' % (c, get_bot_nick(c))
                try: p.addElement('status').addContent(u'(Помощь по командам): '+cmd + ' - ' + COMMANDS[cmd]['desc'].decode('utf8','replace'))
                except: continue
                p.addElement('show').addContent('chat')
                p.addElement('x', 'http://jabber.org/protocol/muc').addElement('history').__setitem__('maxchars', '0')
                try: reactor.callFromThread(dd, p, CLIENTS[x])
                except: pass

register_message_handler(hnd_autohelper)
register_command_handler(hnd_autohelper_work, 'статусхелп', ['все'], 20, 'Включает/отключает автопомощь по командам в статусе', 'статусхелп', ['статусхелп'])

