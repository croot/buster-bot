#===istalismanplugin===
# -*- coding: utf-8 -*-

URL_DETECT_FILE = 'dynamic/url_detect.txt'

db_file(URL_DETECT_FILE, dict)

URL_DETECT_WORK = {}

try: URL_DETECT_WORK=eval(read_file(URL_DETECT_FILE))
except: pass

def hnd_url_detect_con(t, s, p):
        if not s[1] in GROUPCHATS.keys(): return
        global URL_DETECT_FILE
        global URL_DETECT_WORK
        db=eval(read_file(URL_DETECT_FILE))
        if s[1] in db.keys():
                del db[s[1]]
                reply(t, s, u'Отключил')
        else:
                db[s[1]]={}
                reply(t, s, u'Включил')
        URL_DETECT_WORK = db.copy()
        write_file(URL_DETECT_FILE, str(db))

register_command_handler(hnd_url_detect_con, 'юрлдетект', ['все'], 20, 'Включает/отключает автоинфу о ссылках в сообщениях', 'юрлдетект', ['юрлдетект'])                                                        

def url_detect_title(t, s, url):
        title = str()
        req = urllib2.Request(url)
        req = urllib2.urlopen(req, timeout=3)
        enc = req.headers.getparam('charset')
        head = req.info()['Content-Type']
        if head[:9]!='text/html':
                print 'rep'
                rep= u'Сведения о файле:\n'
                rep+= u'Тип файла: '+req.info().get('Content-Type','uknown')+'\n'
                rep+= u'Последние изменения: '+req.info().get('Last-Modified','uknown')+'\n'
                rep+= u'Размер(Байт): '+req.info().get('Content-Length','uknown')+'\n'
                reply(t, s, rep[:250])
                return
        if enc==None: return
        req = req.read().decode(enc, 'replace')
        try: title = re.findall('<title>(.*?)</title>', req, re.DOTALL | re.IGNORECASE)[0]
        except: pass
        reply(t, s, u'Заголовок: '+title[:250])

LAST_URL = {}

def hnd_url_detect(r, t, s, p):
        if not s[1] in GROUPCHATS or not p: return
        if not s[2]: return

        global LAST_URL
        global URL_DETECT_WORK

        if not s[1] in URL_DETECT_WORK.keys():
                return
        
        if s[2]==get_bot_nick(s[1]): return
        
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', p)
        if urls:
                try:
                        if not s[1] in LAST_URL.keys():
                                LAST_URL[s[1]]={'url':[],'time':time.time()}
                        else:
                                if time.time()-LAST_URL[s[1]]['time']<6:
                                        return
                                LAST_URL[s[1]]['time'] = time.time()

                        if urls[0] in LAST_URL[s[1]]['url']:
                                return
                        
                        try:
                                if len(LAST_URL[s[1]]['url'])>20:
                                        LAST_URL[s[1]]['url'].pop(0)
                        except: pass
                        
                        LAST_URL[s[1]]['url'].append(urls[0])
                        url_detect_title(t, s, urls[0])
                except: pass

register_message_handler(hnd_url_detect)

