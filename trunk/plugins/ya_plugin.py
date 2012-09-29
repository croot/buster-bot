#===istalismanplugin===
# -*- coding: utf-8 -*-

def ya_weather(t, s, p):
    if not p:
        return
    p = urllib.quote(p.encode('utf8'))
    req = urllib2.Request('http://pogoda.yandex.ua/'+p+'/details/')
    req.add_header('User-Agent','Mozilla/5.0 (Linux; U; Android 2.2.1; sv-se; HTC Wildfire Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1')
    page = urllib2.urlopen(req).read()
    page = re.findall('зараз.*?вчора', page, re.DOTALL | re.IGNORECASE)
    if not page:
        page = re.findall('сейчас.*?вчера', page, re.DOTALL | re.IGNORECASE)
        if not page:
            reply(t, s, u'Нет погоды для '+p)
            return
    page = page[0]
    page=page.replace('</div>',' ').replace('  ','').replace('В','\nВ').replace('Д','\nД').replace('сейчас','Сейчас:').replace('днем','Днем:').replace('ночью','Ночью:').replace('вечером','Вечером:')
    page = re.compile(r'<[^<>]*>').sub('', page)
    page = page.replace('<img alt="','')
    reply(t, s, unicode(page,'UTF-8'))

gh = ''

def ya_week(t, s, p):
    global gh
    if not p:
        return
    p = urllib.quote(p.encode('utf8'))
    #data = urllib.urlencode({'c':p})
    page = urllib.urlopen('http://pogoda.yandex.ua/'+p)
    page = page.read()
    gh = page
    try: city = re.findall('<title>(.*)</title>', page)[0]
    except: city = ''
    page = re.findall('клімат.*?Розіграш погоди', page, re.DOTALL | re.IGNORECASE)
    if not page:
        reply(t, s, u'Нет погоды для '+p)
        return
    page = page[0]
    m = re.findall('<tr>.*?</tr>',page, re.DOTALL | re.IGNORECASE)
    if not m:
        reply(t, s, u'Произошла ошибка!')
        return
    DICT = {}
    for x in m:
        l=x.split('</div>')
        if m.index(x)==0:
            l=x.split('</div></div>')
        DICT[m.index(x)]=l
    rep=city+u'\nDay | t° min | t° max\n'.encode('utf8')
    n=0
    try:
        for x in DICT[0]:
            k=htmlp(x)
            if k.isspace() or not re.findall('[0-9]+',k):
                continue
            rep+=k+' - '+htmlp(DICT[1][n])+' '+htmlp(DICT[2][n])+' '+htmlp(DICT[3][n])+'\n'
            n+=1
    except: pass
    reply(t, s, unicode(rep.replace('завтра','завтра '),'UTF-8'))   
    

def htmlp(data):
    data=re.compile(r'<[^<>]*>').sub(' ', data)
    return data
    
register_command_handler(ya_week, 'week', ['все'], 0, 'Погода предоставлена сайтом http://yandex.ua ', 'week <city>', ['week киев'])
register_command_handler(ya_weather, 'ya', ['все'], 0, 'Погода предоставлена сайтом http://yandex.ua ', 'ya <city>', ['ya киев'])
