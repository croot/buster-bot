#===istalismanplugin===
# -*- coding: utf-8 -*-

#http://feeds.feedburner.com/euronews/ru/home/
#http://podrobnosti.ua/rss/

def hnd_news_grab(type, source, parameters):
        try:
                rss = feedparser.parse('http://feeds.newsru.com/com/www/section/world')
                list = [(x.title,x.summary) for x in rss.entries]
                if parameters.isdigit() and len(list)>=int(parameters):
                        reply(type, source, list[int(parameters)-1][0]+'\n'+universal_html_parser(list[int(parameters)-1][1]))
                        return
                rep = str()
                for x in list:
                        rep+=str(list.index(x)+1)+'. '+x[0]+'\n'
                reply(type, source, rep+u'\nДетальнее - новости <номер>\nИсточник newsru.com')
        except: reply(type, source, u'Что-то сломалось!')

register_command_handler(hnd_news_grab, 'новости', ['все'], 0, u'Новости предоставленные http://newsru.com , для более детальной информации пишем в качестве параметра команды номер новости в списке, например новости 1', 'новости', ['новости'])

def hnd_news_grab2(type, source, parameters):
        try:
                rss = feedparser.parse('http://podrobnosti.ua/rss/')
                list = [(x.title,x.summary) for x in rss.entries]
                if parameters.isdigit() and len(list)>=int(parameters):
                        reply(type, source, list[int(parameters)-1][0]+'\n'+universal_html_parser(list[int(parameters)-1][1]))
                        return
                rep = str()
                for x in list:
                        rep+=str(list.index(x)+1)+'. '+x[0]+'\n'
                reply(type, source, rep+u'\nДетальнее - новости <номер>\nИсточник podrobnosti.ua')
        except: reply(type, source, u'Что-то сломалось!')

register_command_handler(hnd_news_grab2, 'новости+', ['все'], 0, u'Новости предоставленные http://podrobnosti.ua , для более детальной информации пишем в качестве параметра команды номер новости в списке, например новости+ 1', 'новости+', ['новости+'])
