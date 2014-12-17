# -*- coding: utf-8 -*-

def hnd_test_film(t, s, p):
    if not p:
        return
    if p.count(' ')>4:
        return
    p = p.replace(' ','+')
    url = 'http://www.kinokopilka.tv/search?search_mode=movies&q='+p.encode('utf8')
    page = TV.open(url, timeout=5).read()
    f = re.findall('<a href=[\"]\/movies\/(.*?)[\"]', page)
    tit =  re.findall('<span class=["]title["]>(.*?)</span>', page)
    if not f:
        reply(t, s, u'По вашему запросу ничего не найдено!')
        return
    page = TV.open('http://www.kinokopilka.tv/movies/'+f[0], timeout=5).read()
    desc = re.findall('<meta name=["]description["] content=["](.*?)["]', page)
    page = re.findall('<p>(.*?)</p>', page)
    if not page:
        reply(t, s, u'Ошибка парсера!')
        return
    page = page[0]
    reply(t, s, (desc[0] if desc else '')+'\n'+page)

FILM_TEMP = {}

def hnd_film(t, s, p):
    global FILM_TEMP
    jid = get_true_jid(s)
    n = 0
    if not jid in FILM_TEMP.keys():
        FILM_TEMP[jid]={}
    if p in FILM_TEMP[jid]:
        page = urllib.urlopen('http://wap.sasisa.ru/film/film.php?id='+FILM_TEMP[jid][p][0]).read()
        page = universal_html_parser(page)
        reply(t, s, page)
        return
    p = p.replace(' ','+')
    rep = ''
    url = 'http://wap.sasisa.ru/film/search.php?title='+p.encode('utf8')
    page = urllib.urlopen(url).read()
    films = re.findall('<a href=[\"]film.php\?id=(.*?)[\"]>(.*?)</a>', page, re.DOTALL|re.IGNORECASE)
    if not films:
        reply(t, s, u'Ничего не найденно!')
        return
    if len(films) == 1:
        try:
            page = urllib.urlopen('http://wap.sasisa.ru/film/film.php?id='+films[0][0]).read()
        except:
            reply(t, s, u'Ошибка открытия страницы!')
            return
        pag = re.findall('Жанр:(.*?)Комментарии', page)
        if pag:
            page = pag[0]
        
        page = universal_html_parser(page)
        page = page.replace(', ,','')
        reply(t, s, page)
    else:
        n = 0
        for x in films:
            n+=1
            rep+=str(n)+') '+films[n-1][1]+'\n'
            FILM_TEMP[jid][str(n)] = x
        reply(t, s, rep)


register_command_handler(hnd_test_film, 'фильм', ['все'], 0, 'Поиск информации о фильме на www.kinokopilka.tv', 'фильм название', ['фильм ворон'])
