#===istalismanplugin===
# -*- coding: utf-8 -*-

WEATHER_CACHE = 'dynamic/weather_cache.txt'
db_file(WEATHER_CACHE, dict)
#WEATHER_TEMP = {}

def yaw_getcity(jid, city=None):
    try: db=eval(read_file(WEATHER_CACHE))
    except: return None
    if city:
        db[jid]=city
        write_file(WEATHER_CACHE, str(db))
        return True
    else:
        if jid in db.keys():
            return db[jid]
    return None

def ya_weather(t, s, p):
    #global WEATHER_TEMP
    jid = get_true_jid(s)
    if not p:
        p = yaw_getcity(jid)
        if not p: return
    else:
        yaw_getcity(jid, p)

    city_first = p
    p = urllib.quote(p.encode('utf8'))
    req = urllib2.Request('http://pogoda.yandex.ua/'+p+'/details/')
    req.add_header('User-Agent','Mozilla/5.0 (Linux; U; Android 2.2.1; sv-se; HTC Wildfire Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1')
    page = urllib2.urlopen(req).read()
    try: city = re.findall('<title>(.*)</title>', page)[0]
    except: city = ''
    try: res = re.findall('зараз.*?вчора.*?\d*\d', page, re.DOTALL | re.IGNORECASE)
    except:
        reply(t, s, u'Нет погоды для <'+city_first+'>')
        return
    if not res:
        reply(t, s, u'Нет погоды для <'+city_first+'>')
        return
    a = page.split('клімат')
    if a and len(a)>1:
        a = a[1]
        b = a.split('вранці')
        if not b:
            reply(t, s, u'Город не найден!')
            return
        #WEATHER_TEMP = b
    
    part_a = res[0]
    part_a = part_a.replace('</div>',' ').replace('  ','')
    page = '\n'.join(['Сьогоднi:\n'+b[1][:-6],'Завтра:\n'+b[2].strip()])
    page = page.replace('</div>',' ').replace('вранці','\nвранці').replace('вдень','\nвдень').replace('увечері','\nувечері').replace('вночі','\nвночі')
    page = re.compile(r'<[^<>]*>').sub('', page)
    page = re.compile(r'\d\d\d.*?%').sub('', page)
    page = re.compile(r'\d\.\d.*?\n').sub('\n', page)
    page = re.compile(r'\nвранці$').sub('\n', page)
    if t in ['public','groupchat']:
        part_a+='\n>>> Детально в привате!'
        reply(t, s, unicode(city+'\n'+htmlp(part_a), 'UTF-8'))
        time.sleep(1.5)
        reply('private', s, unicode(city+'\n'+page, 'UTF-8'))
    else:
        reply(t, s, unicode(city+'\n'+htmlp(part_a)+'\n-== Детально ==-\n'+page,'UTF-8'))


def ya_week(t, s, p):
    if len(p)>35: return
    
    jid = get_true_jid(s)
    if not p:
        p = yaw_getcity(jid)
        if not p: return
    else:
        yaw_getcity(jid, p)
        
    p = urllib.quote(p.encode('utf8'))
    req = urllib2.Request('http://pogoda.yandex.ua/search/?request='+p)
    req.add_header('User-Agent','Mozilla/5.0 (Linux; U; Android 2.2.1; sv-se; HTC Wildfire Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1')
    page = urllib2.urlopen(req).read()
    gh = page
    write_file('pog.html', str(page))
    try: city = re.findall('<title>(.*)</title>', page)[0]
    except: city = ''
    page = re.findall('клімат|докладно(.*?)Розіграш погоди', page, re.DOTALL | re.IGNORECASE)
    if not page:
        if not page:
            reply(t, s, u'Нет погоды для '+p)
            return
    page = page[0]
    m = re.findall('<tr>.*?</tr>',page, re.DOTALL | re.IGNORECASE)
    if not m:
        reply(t, s, u'Произошла ошибка!')
        return
    try:
        if len(m)>=14: m = m[10:]
    except: pass
    DICT = {}
    for x in m:
        l=x.split('</div>')
        if m.index(x)==0:
            l=x.split('</div></div>')
        DICT[m.index(x)]=l
    rep=city+u'\nДень | t° max - t° min\n'.encode('utf8')
    n=0
    try:
        for x in DICT[0]:
            k=htmlp(x)
            if k.isspace() or not re.findall('[0-9]+',k,re.DOTALL | re.IGNORECASE):
                continue
            rep+=k+' - '+htmlp(DICT[1][n])+' '+htmlp(DICT[2][n])+' '+htmlp(DICT[3][n])+'\n'
            n+=1
    except: pass
    rep = rep.replace('    ',' ')
    reply(t, s, unicode(rep,'UTF-8'))  
    

def htmlp(data):
    data=re.compile(r'<[^<>]*>').sub('', data)
    return data
    
register_command_handler(ya_week, 'week', ['все'], 0, 'Погода предоставлена сайтом http://yandex.ua ', 'week <city>', ['week киев'])
register_command_handler(ya_weather, 'ya', ['все'], 0, 'Погода предоставлена сайтом http://yandex.ua ', 'ya <city>', ['ya киев'])
