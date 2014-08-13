#===istalismanplugin===
# -*- coding: utf-8 -*-

#http://feeds.feedburner.com/euronews/ru/home/
#http://podrobnosti.ua/rss/

import inspect

NEWS_TEMP = {}


if not 'DIGIT_MENU' in globals().keys():
        DIGIT_MENU = {}

def hnd_news_grab(type, source, parameters):
        global DIGIT_MENU
        global NEWS_TEMP

        jid = get_true_jid(source)
        fn = inspect.stack()[0][3]
        
        try:
                rss = feedparser.parse('http://feeds.newsru.com/com/www/section/world')
                list = [(x.title,x.summary,x.link) for x in rss.entries]
                if jid in NEWS_TEMP and NEWS_TEMP[jid]['f']==fn and time.time()-NEWS_TEMP[jid]['t']<600:
                        list = NEWS_TEMP[jid]['list']
                else:
                        NEWS_TEMP[jid]={'f':fn,'t':time.time(),'list': list}
                if parameters.isdigit() and len(list)>=int(parameters):
                        i = list[int(parameters)-1]
                        
                        
                        page = send_urlopen_q(i[2], False)
                        page = '\n'.join(re.findall('<p>(.[^<>]*?)</p>', page, re.DOTALL | re.IGNORECASE))
                        
                        page = universal_html_parser(page)
                        if page.isspace() or not page:
                                page = i[1]
                        reply(type, source, page)
                        return
                DIGIT_MENU[jid]=fn
                rep = str()
                for x in list:
                        rep+=str(list.index(x)+1)+'. '+x[0]+'\n'
                
                reply(type, source, rep+u'\nДетальнее - пиши <номер>, напр. 1\nИсточник newsru.com')
        except:
                reply(type, source, u'Что-то сломалось!')

register_command_handler(hnd_news_grab, 'новости', ['все'], 0, u'Новости предоставленные http://newsru.com , для более детальной информации пишем в качестве параметра команды номер новости в списке, например новости 1', 'новости', ['новости'])

def hnd_news_grab2(type, source, parameters):
        global NEWS_TEMP
        global DIGIT_MENU
        fn = inspect.stack()[0][3]
        
        jid = get_true_jid(source)
        try:
                rss = feedparser.parse('http://podrobnosti.ua/rss/')
                list = [(x.title,x.summary) for x in rss.entries]
                if jid in NEWS_TEMP and NEWS_TEMP[jid]['f']==fn and time.time()-NEWS_TEMP[jid]['t']<600:
                        list = NEWS_TEMP[jid]['list']
                else:
                        NEWS_TEMP[jid]={'f':fn,'t':time.time(),'list': list}
                if parameters.isdigit() and len(list)>=int(parameters):
                        reply(type, source, list[int(parameters)-1][0]+'\n'+universal_html_parser(list[int(parameters)-1][1]))
                        return
                rep = str()
                DIGIT_MENU[jid]=fn
                for x in list:
                        rep+=str(list.index(x)+1)+'. '+x[0]+'\n'
                reply(type, source, rep+u'\nДетальнее - пиши <номер>, напр. 2\nИсточник podrobnosti.ua')
        except: reply(type, source, u'Что-то сломалось!')

register_command_handler(hnd_news_grab2, 'новости+', ['все'], 0, u'Новости предоставленные http://podrobnosti.ua , для более детальной информации пишем в качестве параметра команды номер новости в списке, например новости+ 1', 'новости+', ['новости+'])
