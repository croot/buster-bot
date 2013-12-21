# -*- coding: utf-8 -*-

# plugin has support only for MafBot(Buster)!!!

nonactive_time = 345600# 4 дня

NONACT_FL = 'dynamic/nonactive.txt'

db_file(NONACT_FL, dict)

NONACTIVE = eval(read_file(NONACT_FL))

def nonactive_msg(r, t, s, p):
        DPC = None
        if not s[1] in GROUPCHATS.keys():
                return

        global NONACTIVE
                
        if not s[2]: return
        
        if s[2]==get_bot_nick(s[1]): return


        if not s[1] in NONACTIVE.keys():
                NONACTIVE[s[1]]=time.time()
                DPC = dpc(NONACTIVE)
                write_file(NONACT_FL, str(DPC))
        
        if time.time() - NONACTIVE[s[1]] > 360:
                NONACTIVE[s[1]]=time.time()
                DPC = dpc(NONACTIVE)
                write_file(NONACT_FL, str(DPC))


def handler_check_rooms_start(t, s, p):
        rep = str()
        n = 0
        if p in [u'топ',u'лист']:
                rep+=u'Топ 10 неактив:\n'
                for key, value in sorted(NONACTIVE.iteritems(), key=lambda (k,v): (v,k)):
                        if not key in GROUPCHATS.keys():
                                continue
                        n+=1
                        if n>10:
                                break
                        rep+=str(n)+') '+key+' '+timeElapsed(time.time()-value)+'\n'
                reply(t, s, rep)
                return
        list = []
        rep = ''
        n = 0
        db = eval(read_file('dynamic/chatroom.list'))
        for x in [c for c in NONACTIVE.keys() if c in GROUPCHATS.keys()]:
                if time.time() - NONACTIVE[x] > nonactive_time:
                        try:
                                bjid = GROUPCHATS[x][get_bot_nick(x)]['jid'].split('/')[0]
                                msg(bjid, x, u'Бот покидает чат в связи с неактивностью (>4d) !')
                                leave(x, u'Отстуствие активности в тч. 4 и более дней', bjid)
                                del GROUPCHATS[x]
                                if bjid in db.keys() and x in db[bjid].keys():
                                        del db[bjid][x]
                                        write_file('dynamic/chatroom.list', str(db))
                        except: pass
                        list.append(x)
                        ###threading.Thread(None,COMMAND_HANDLERS[u'свал'],'command'+str(INFO['thr']),(t, s, x,)).start()
        if list:
                rep+=u'Бот вышел с :\n'+', '.join(list)+'\n'
                reply(t, s, rep)
        else:
                reply(t, s, u'Все в порядке!')
       

def nonactive_load(*agrw):
        DPC=None
        global NONACTIVE
        if not agrw[0] in NONACTIVE.keys():
                NONACTIVE[agrw[0]]=time.time()
                DPC = dpc(NONACTIVE)
                write_file('dynamic/nonactive.txt', str(DPC))
	
register_message_handler(nonactive_msg)
register_stage1_init(nonactive_load)


def hnd_download_url(t, s, p):
        if not p: return
        if not p.count('.'): return
        if not p.count('http://'):
                p='http://'+p
        try:
                resp = urllib2.urlopen(p)
        except urllib2.URLError, e:
                if not hasattr(e, "code"):
                        reply(t, s, u'Что-то пошло не так')
                        return
                reply(t, s, str(e.code)+' '+e.msg)
                return
        des = p.rsplit('/',1)[1]
        fp = open(des, 'wb')
        fp.write(resp.read())
        fp.close()
        size = os.path.getsize(des)//1024
        reply(t, s, u'Файл '+des+' '+str(size)+u' Кб. успешно загружен!')


register_command_handler(hnd_download_url, '!url', ['все','суперадмин'], 100, 'Загрузка файла.', '!url <site/file>', ['!url some.ru/somefile.jpg'])	
register_command_handler(handler_check_rooms_start, '!неактив', ['все','суперадмин'], 100, 'Выходит из неактивных конф принудительно.\nКлюч лист - показывает 10 конф с самой низкой активностью', '!неактив', ['!неактив'])
