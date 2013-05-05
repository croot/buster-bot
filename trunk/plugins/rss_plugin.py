#===istalismanplugin===
# -*- coding: utf-8 -*-


RSS_GLOB = {}

RSS_THREAD = 0

RSS_CACHE_FILE = 'dynamic/rss_cache.txt'

db_file(RSS_CACHE_FILE, dict)

#channel-url : { 'sub':{jid1:cljid, jid2:cljid, ..}, 'last': rss.feed['updated']}

try: from rss import feedparser
except: print "NO Module rss"
import HTMLParser

def rss_reader():
        def ufnsc(page):
                h = HTMLParser.HTMLParser()
                return h.unescape(page)
        page = ''
        while RSS_THREAD:
                time.sleep(120)
                list = [x for x in RSS_GLOB.keys() if RSS_GLOB[x]['sub']]
                for x in list:
                        try: c = feedparser.parse(x)
                        except: continue
                        if c['status']!=200:
                                continue
                        time.sleep(2.5)
                        for i in random.shuffle(c.entries):
                                if not i.get('id','1') in RSS_GLOB[x]['ids']:
                                        RSS_GLOB[x]['ids'].append(i.get('id','1'))
                                        for user in RSS_GLOB[x]['sub']:
                                                if user.count('@con') | user.count('@chat') | user.count('@muc'):
                                                        if not user in GROUPCHATS:
                                                                del RSS_GLOB[x]['sub'][user]
                                                                write_file(RSS_CACHE_FILE, str(RSS_GLOB))
                                                                continue
                                                if c['encoding'] not in ['UTF-8','utf8','utf-8','ascii']:
                                                        try:
                                                                page = '\n'.join([c.feed['title'],i.title, i.summary, i.link])
                                                                page = page.encode(c['encoding'])
                                                                page = page.decode(c['encoding'],'replace')
                                                                page = 'RSS '+page
                                                        except:
                                                                continue
                                                        msg(RSS_GLOB[x]['sub'][user], user, ufnsc(page))
                                                else:
                                                        page = '\n'.join(['RSS '+c.feed['title'],i.title, i.summary, i.link])
                                                        msg(RSS_GLOB[x]['sub'][user], user, ufnsc(page))
                                        break


def rss_lists(t, s, p):
        rep, n, jid, sub = str(), 0, get_true_jid(s), str()
        if not RSS_GLOB:
                reply(t, s, u'У вас в списке недобавлено пока ни одного канала!')
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

        title = ('' if not d.feed.get('title','') else '('+d.feed['title']+')')

        RSS_GLOB[p] = {'sub':{}, 'ids':[], 'title':title, 'show':0, 'cljid':s[3]}
        write_file(RSS_CACHE_FILE, str(RSS_GLOB))
        reply(t, s, u'Источник " '+p+u' " '+title+u' успешно добавлен!')


def rss_manager(t, s, p):
        global RSS_THREAD
        if not p:
                rss_lists(t, s, p)
                return
        jid = get_true_jid(s)
        if p.isdigit() and p!='0':
                if not len(RSS_GLOB)>=int(p):
                        reply(t, s, u'Канала с таким номером не найдено!')
                        return
                if s[1] in GROUPCHATS:
                        jid = s[1]
                if not jid in RSS_GLOB[RSS_GLOB.keys()[int(p)-1]]['sub']:
                        RSS_GLOB[RSS_GLOB.keys()[int(p)-1]]['sub'][jid]=s[3]
                        reply(t, s, jid+u' успешно подписан на '+RSS_GLOB.keys()[int(p)-1])
                        if not RSS_THREAD:
                                RSS_THREAD = 1
                                threading.Thread(None, rss_reader, 'rss_reader'+str(INFO['thr'])).start()
                else:
                        del RSS_GLOB[RSS_GLOB.keys()[int(p)-1]]['sub'][jid]
                        reply(t, s, jid+u' удален из рассылки '+RSS_GLOB.keys()[int(p)-1])
                write_file(RSS_CACHE_FILE, str(RSS_GLOB))

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
register_command_handler(rss_manager, '!rss', ['rss','инфо','все'], 0, 'Работа с лентами новостей (RSS).\n Без параметров выводит список доступных каналов для подписки.\nДля подписки/отказа нужно указать номер канала в списке.\nЕсли вы хотите сделать подписку для конференции то просто выполните команду в этой конференции.', '!rsslist', ['!rsslist'])
register_command_handler(rss_add_channel, '!rss+', ['rss','инфо','все'], 40, 'Добавить RSS-канал в список достуных для подписки.', '!rss+ <url>', ['!rss+ http://gogi.net/news.rss'])
register_command_handler(rss_del_channel, '!rss-', ['rss','инфо','все'], 40, 'Удалить RSS-канал из списока достуных для подписки. Для удаления используется номер канала в списке. Список каналов доступен по команде !rss', '!rss- <number>', ['!rss- 1'])

