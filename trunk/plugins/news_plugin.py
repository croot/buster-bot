#===istalismanplugin===
# -*- coding: utf-8 -*-

NEWS_GRAB = []

def hnd_news_grab(t, s, p):
    global NEWS_GRAB
    if p:
        if p.isdigit() and int(p)<len(NEWS_GRAB):
            page = urllib.urlopen('http://news.domochat.ru/?r=2&t='+NEWS_GRAB[int(p)-1]+'&s=').read()
            src = re.findall('<h1>(.*?)<a href', page, re.DOTALL | re.IGNORECASE)
            reply(t, s, decode(''.join(src)))
        return
    page = urllib.urlopen('http://news.domochat.ru/?r=2&s=').read()
    url = re.findall('<a href=\'?(.*?)&s=\'>', page, re.DOTALL | re.IGNORECASE)
    url = [x for x in url if x.count('=2&t=')]
    if url:
        NEWS_GRAB = url
    src = re.findall('<p>(.*?)</p>', page, re.DOTALL | re.IGNORECASE)
    rep = [str(src.index(x)+1)+') '+x+'\n' for x in src]
    rep = decode(''.join(rep))
    reply(t, s, rep)

register_command_handler(hnd_news_grab, 'новости', ['все'], 0, u'Новости предоставленные http://news.domochat.ru/, для более детальной информации пишем в качестве параметра команды номер новости в списке, например новости 1', 'новости', ['новости'])
