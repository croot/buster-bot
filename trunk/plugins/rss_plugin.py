#===istalismanplugin===
# -*- coding: utf-8 -*-


RSS_GLOB = {}

RSS_CONFIG = {}

RSS_THREAD = 0

RSS_CACHE_FILE = 'dynamic/rss_cache.txt'

RSS_CONFIG_FILE = 'dynamic/rss_config.txt'

RSS_HASH_FILE = 'dynamic/rss_hash.txt'

db_file(RSS_CACHE_FILE, dict)
db_file(RSS_CONFIG_FILE, dict)
db_file(RSS_HASH_FILE, list)

#channel-url : { 'sub':{jid1:cljid, jid2:cljid, ..}, 'last': rss.feed['updated']}

try: from rss import feedparser
except: print "NO Module rss"
import HTMLParser

import hashlib

def rss_sender(user, parse):
        pass

def rss_md5(string):
        """string to md5 convertor"""
        if not isinstance(string, basestring):
                try: string = string.decode('utf8','replace')
                except: pass
        md5 = hashlib.md5()
        md5.update(string.encode('utf8'))
        return md5.hexdigest()

def rss_reader():
        global RSS_HASH_FILE
        hm = eval(read_file(RSS_HASH_FILE))
        DPC = dpc(RSS_GLOB)
        def ufnsc(page):
                h = HTMLParser.HTMLParser()
                page = h.unescape(page)
                page = page.replace('<br />','\n').replace('<br/>','\n')
                return universal_html_parser(page)
        page, bjid = '', ''
        while RSS_THREAD:
                time.sleep(120)
                list = [x for x in DPC.keys() if DPC[x]['sub']]
                for x in list:
                        try: c = feedparser.parse(x)
                        except: continue
                        try:
                                if c['status']!=200:
                                        continue
                        except: continue
                        time.sleep(2.5)
                        j = c.entries
                        random.shuffle(j)
                        for i in j:
                                tit = rss_md5(i.get('title','-'))
                                if not tit in hm:#DPC[x]['ids']:
                                        if len(hm)>65:
                                                hm = hm[-15:]
                                        hm.append(tit)
                                        for user in DPC[x]['sub']:
                                                bjid = DPC[x]['sub'][user]
                                                if user.count('@con') | user.count('@chat') | user.count('@muc'):
                                                        if not user in GROUPCHATS:
                                                                del DPC[x]['sub'][user]
                                                                write_file(RSS_CACHE_FILE, str(DPC))
                                                                continue
                                                        else:
                                                                if GROUPCHATS[user][get_bot_nick(user)]['ismoder']:
                                                                        bjid = GROUPCHATS[user][get_bot_nick(user)]['jid']
                                                                        bjid = bjid.split('/')[0]
                                                if c['encoding'] not in ['UTF-8','utf8','utf-8','ascii']:
                                                        try:
                                                                page = '\n'.join([c.feed['title'],i.title, i.summary, i.link])
                                                                page = page.encode(c['encoding'])
                                                                page = page.decode(c['encoding'],'replace')
                                                                page = 'RSS '+page
                                                        except:
                                                                continue
                                                        msg(bjid, user, ufnsc(page))
                                                else:
                                                        page = '\n'.join(['RSS '+c.feed['title'],i.title, i.summary, i.link])
                                                        msg(bjid, user, ufnsc(page))
                                        break
                
                write_file(RSS_HASH_FILE, str(hm))
                RSS_GLOB.update(DPC)


def rss_lists(t, s, p):
        rep, n, jid, sub = str(), 0, get_true_jid(s), str()
        if not RSS_GLOB:
                reply(t, s, u'У вас в списке не добавлено пока ни одного канала!')
                return
        sub = str()
        rep+=u'№ | (url)Addres | Заголовок | Подписка (JID или чат) | Кол-во подписчиков\n'
        for x in RSS_GLOB.keys():
                sub = ''
                n+=1
                if jid in RSS_GLOB[x]['sub']:
                        sub='JID '
                if s[1] in GROUPCHATS and s[1] in RSS_GLOB[x]['sub']:
                        sub+=u'Чат '
                if not sub:
                        sub = u'нет'
                rep+=str(n)+') '+x+' '+RSS_GLOB[x].get('title','None')+u' '+sub+' ('+str(len(RSS_GLOB[x]['sub']))+')\n'
        reply(t, s, u'Всего каналов '+str(n)+':\n'+rep)


def rss_add_channel(t, s, p):
        DPC=None
        global RSS_GLOB
        global RSS_CACHE_FILE
        
        if not p:
                reply(t, s, u'Укажите url-адрес нового канала!')
                return
        
        d = feedparser.parse(p)
        if d['status']!=200:
                reply(t, s, u'Указанный адрес не может быть прочитан. Статус '+str(d['status']))
                return

        i = [x.lower() for x in RSS_GLOB.keys()]
        if p.lower() in i:
                reply(t, s, u'Такой url уже есть в списке!')
                return

        level = int(user_level(s[1]+'/'+s[2], s[1]))
        if level<40:
                reply(t, s, u'Заявка на добавление вашего канала отправлена админам бота!')
                for x in [x for x in GLOBACCESS.keys() if GLOBACCESS[x]==100]:
                        msg(s[3], x, u'Заявка на добавление RSS-канала от пользователя '+s[1]+'/'+s[2]+u'\n Наберите !rss+ '+p+u' для добавления!')
                return

        DPC = dpc(RSS_GLOB)

        title = ('' if not d.feed.get('title','') else '('+d.feed['title']+')')

        DPC[p] = {'sub':{}, 'ids':[], 'title':title, 'show':0, 'cljid':s[3]}
        
        write_file(RSS_CACHE_FILE, str(DPC))
        reply(t, s, u'Источник " '+p+u' " '+title+u' успешно добавлен!')
        RSS_GLOB.update(DPC)


def rss_manager(t, s, p):
        DPC=dpc(RSS_GLOB)
        global RSS_THREAD
        if not p:
                rss_lists(t, s, p)
                return
        if p.split()>1 and p.split()[0].lower()=='?' and p.split()[1].isdigit():
                if not len(DPC)>=int(p.split()[1]):
                        reply(t, s, u'Канала с таким номером не найдено!')
                        return
                rss = feedparser.parse(DPC.keys()[int(p.split()[1])-1])
                if rss.entries:
                        rss = '\n- '.join([x.get('title','-') for x in rss.entries])
                        reply(t, s, '- '+rss)
                return
        jid = get_true_jid(s)
        if p.isdigit() and p!='0':
                if not len(DPC)>=int(p):
                        reply(t, s, u'Канала с таким номером не найдено!')
                        return
                if s[1] in GROUPCHATS:
                        level = int(user_level(s[1]+'/'+s[2], s[1]))
                        if level<20:
                                reply(t, s, u'Для подписки в чат у вас должен быть доступ админа(20)!')
                                return
                        jid = s[1]
                if not jid in DPC[DPC.keys()[int(p)-1]]['sub']:
                        DPC[DPC.keys()[int(p)-1]]['sub'][jid]=s[3]
                        reply(t, s, jid+u' успешно подписан на '+DPC.keys()[int(p)-1])
                        if not RSS_THREAD:
                                RSS_THREAD = 1
                                threading.Thread(None, rss_reader, 'rss_reader'+str(INFO['thr'])).start()
                else:
                        del DPC[DPC.keys()[int(p)-1]]['sub'][jid]
                        reply(t, s, jid+u' удален из рассылки '+DPC.keys()[int(p)-1])
                write_file(RSS_CACHE_FILE, str(DPC))
                RSS_GLOB.update(DPC)

def rss_init(*n):
        global RSS_GLOB
        global RSS_CACHE_FILE
        global RSS_THREAD
        
        if RSS_GLOB:
                return
        RSS_GLOB = eval(read_file(RSS_CACHE_FILE))
        for x in RSS_GLOB:
                if RSS_GLOB[x]['sub']:
                        RSS_THREAD = 1
                        threading.Thread(None, rss_reader, 'rss_reader'+str(INFO['thr'])).start()
                        break

def rss_del_channel(t, s, p):
        if not p:
                return
        if not p.isdigit():
                reply(t, s, u'Вы должны указать номер канала в списке!')
                return
        if not len(RSS_GLOB)>=int(p):
                reply(t, s, u'Нет такого канала!')
                return
        del RSS_GLOB[RSS_GLOB.keys()[int(p)-1]]
        write_file(RSS_CACHE_FILE, str(RSS_GLOB))
        reply(t, s, 'ok')

register_stage0_init(rss_init)
register_command_handler(rss_manager, '!rss', ['rss','инфо','все'], 0, 'Работа с лентами новостей (RSS).\n Без параметров выводит список доступных каналов для подписки.\nДля подписки/отказа нужно указать номер канала в списке.\nЕсли вы хотите сделать подписку для конференции то просто выполните команду в этой конференции.\nКлюч ? n - выведет заголовки канала с номером n.', '!rss', ['!rss','!rss 1','!rss ? 1'])
register_command_handler(rss_add_channel, '!rss+', ['rss','инфо','все'], 0, 'Добавить RSS-канал в список достуных для подписки.', '!rss+ <url>', ['!rss+ http://gogi.net/news.rss'])
register_command_handler(rss_del_channel, '!rss-', ['rss','инфо','все'], 40, 'Удалить RSS-канал из списока достуных для подписки. Для удаления используется номер канала в списке. Список каналов доступен по команде !rss', '!rss- <number>', ['!rss- 1'])

