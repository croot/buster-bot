#===istalismanplugin===
# -*- coding: utf-8 -*-

def ya_weather(t, s, p):
    if not p:
        return
    p = urllib.quote(p.encode('utf8'))
    page = urllib.urlopen('http://pogoda.yandex.ua/'+p+'/details/').read()
    page = re.findall('сейчас.*?пункта', page, re.DOTALL | re.IGNORECASE)
    if not page:
        reply(t, s, u'Нет погоды для '+p)
        return
    page = page[0]
    page=page.replace('</div>',' ').replace('  ','').replace('В','\nВ').replace('Д','\nД').replace('сейчас','Сейчас:').replace('днем','Днем:').replace('ночью','Ночью:').replace('вечером','Вечером:')
    page = re.compile(r'<[^<>]*>').sub('', page)
    page = page.replace('<img alt="','')
    reply(t, s, unicode(page,'UTF-8'))

def ya_week(t, s, p):
    if not p:
        return
    p = urllib.quote(p.encode('utf8'))
    #data = urllib.urlencode({'c':p})
    page = urllib.urlopen('http://pogoda.yandex.ua/'+p)
    page = page.read()
    try: city = re.findall('<title>(.*)</title>', page)[0]
    except: city = ''
    page = re.findall('климат.*?Розыгрыш погоды', page, re.DOTALL | re.IGNORECASE)
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
    rep=city+u'\nДата | Погода днем | ночью\n'.encode('utf8')
    n=0
    try:
        for x in DICT[0]:
            k=htmlp(x)
            if k.isspace() or not re.findall('[0-9]+',k):
                continue
            rep+=k+' - '+htmlp(DICT[1][n])+' '+htmlp(DICT[2][n])+' '+htmlp(DICT[3][n])+'\n'
            n+=1
    except: pass
    reply(t, s, unicode(rep,'UTF-8'))    
    

def htmlp(data):
    data=re.compile(r'<[^<>]*>').sub('', data)
    return data
    
register_command_handler(ya_week, 'week', ['все'], 0, 'Погода предоставлена сайтом http://yandex.ua ', 'week <city>', ['week киев'])
register_command_handler(ya_weather, 'ya', ['все'], 0, 'Погода предоставлена сайтом http://yandex.ua ', 'ya <city>', ['ya киев'])
