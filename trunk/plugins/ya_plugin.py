#===istalismanplugin===
# -*- coding: utf-8 -*-

WEATHER_CACHE = 'dynamic/weather_cache.txt'
db_file(WEATHER_CACHE, dict)

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


import xml.etree.ElementTree as etree


def yanew_getid(city):
    #c = urllib.urlopen('http://weather.yandex.ru/static/cities.xml').read()
    #d = xmldict.xml_to_dict(c)['cities']['country']
    #for x in d:
    #    for i in x.get('city',[]):
    #        if isinstance(i,dict):
    #            if i.get('#text','').lower()==city.lower():
    #                return i.get('@id','0')
    #return 0
    import xml.etree.ElementTree
    c = xml.etree.ElementTree.fromstring(urllib.urlopen('http://weather.yandex.ru/static/cities.xml').read())
    for i in c:
        for x in i:
            #print x
            if hasattr(x, 'text'):
                ct = x.text.lower()
                if ct==city.lower() or ct.count(city.lower()):
                    return x.get('id')
    return 0




def yanew_getweath(t, s, p):
    jid = get_true_jid(s)
    if not p:
        p = yaw_getcity(jid)
        if not p:
            reply(t, s, u'И какой город мне показывать?')
            return
    else:
        yaw_getcity(jid, p)
        #reply(t, s, u'Запомнил!')
        #time.sleep(2)
    
    def fdd(x, key):
        res = 'None'
        if hasattr(x, 'find'):
            res = x.find(key)
            if hasattr(res, 'text'):
                return res.text
        return res
    wind = {'n':u'север','e':u'восток','w':u'запад','s':u'юг','c':u'затишье'}
    a = '{http://weather.yandex.ru/forecast}'
    d = {0:a+'forecast',1:a+'day',2:a+'fact',3:a+'day_part',4:a+'temperature_from',5:a+'temperature_to',6:a+'weather_type',7:a+'weather_type_short',8:a+'wind_speed',9:a+'humidity',10:a+'temperature',11:a+'sunrise',12:a+'sunset'}
    word = {d[11]:u'Рассвет',d[12]:u'Закат',d[4]:u'от',d[5]:u'до',u'morning':u'Утром',u'day':u'Днем',u'evening':u'Вечером',u'night':u'Ночью'}
    id = yanew_getid(p)
    if not id:
        reply(t, s, u'Город не найден!')
        return
    c = etree.parse(urllib.urlopen('http://export.yandex.ru/weather-ng/forecasts/'+id+'.xml')).getroot()
    listday = [x for x in c._children if x.tag == d[1]]
    fact = [x for x in c._children if x.tag == d[2]]
    if fact: fact = fact[0]
    rep = u'Погодa для '+c.get('city')+', '+c.get('country')+'\n'
    rep+= u'Сейчас: '+fdd(fact, d[10])+u'°C, '+fdd(fact, d[7])+', '+fdd(fact, d[8])+u'м/с\n'
    l = ''
    for x in listday:
        date = x.attrib.get('date','0')
        rep+='\n   '+date+'\n'
        l = u'  Свет. день: '+x.find(d[11]).text+u'-'+x.find(d[12]).text+'\n'
        for i in [m for m in x.iter('{http://weather.yandex.ru/forecast}day_part')]:
            if not i.attrib['type'] in word:
                continue
            
            rep+=word[i.attrib['type']]+':\n'
            
            try: rep+=i.find(d[4]).text+' ... '+i.find(d[5]).text+', '+i.find(d[7]).text+'\n'
            except: rep+=i.find(d[10]).text+', '+i.find(d[7]).text+'\n'
            finally: pass
        rep+=l
    
    reply(t, s, rep)
    

    
register_command_handler(ya_week, 'week', ['все'], 0, 'Погода предоставлена сайтом http://yandex.ru ', 'week <city>', ['week киев'])
register_command_handler(yanew_getweath, 'ya', ['все'], 0, 'Погода предоставлена сайтом http://yandex.ru \nАвтоматически запоминает последний указанный город, в дальнейшем можно использовать без параметров.', 'ya <city>', ['ya киев'])
