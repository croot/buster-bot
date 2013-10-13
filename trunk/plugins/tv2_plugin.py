#===istalismanplugin===
# -*- coding: utf-8 -*-


def dehtml(p):
    h = HTMLParser.HTMLParser()
    p = h.unescape(p)
    return p




def hnd_tv2(t, s, p):
    if p.isdigit():
        req = urllib2.Request('http://www.teleguide.info/kanal'+p+'.html')
        req.add_header('User-Agent', UserAgent().random)
        page = urllib2.urlopen(req).read().decode('utf8','ignore')
        try: page = '\n'.join(re.findall('(\d{2}:\d{2}.*?)</div>',page,re.DOTALL|re.IGNORECASE)[1:])
        except:
            reply(t, s, u'Ошибка парсера')
            return
        reply(t, s, dehtml(page))
        return
    req = urllib2.Request('http://www.teleguide.info/kanals.html')
    req.add_header('User-Agent', UserAgent().random)
    page = urllib2.urlopen(req).read().decode('utf8','ignore')
    page = re.findall('<a href="/kanal(\d{1,6}).html" title="(.*?)"',page,re.DOTALL|re.IGNORECASE)
    list=[]
    print len(page)
    for x in page:
        if x[1].lower().count(p.lower()) or x[1].lower()==p.lower():
            list.append(x)
    if not list:
        reply(t, s, u'Канал <'+p+u'> не найден!')
        return
    if len(list)==1:
        req = urllib2.Request('http://www.teleguide.info/kanal'+list[0][0]+'.html')
        req.add_header('User-Agent', UserAgent().random)
        page = urllib2.urlopen(req).read().decode('utf8','ignore')
        try: page = '\n'.join(re.findall('(\d{2}:\d{2}.*?)</div>',page,re.DOTALL|re.IGNORECASE)[1:])
        except: return
        reply(t, s, dehtml(page))
        return
    rep=''
    for x in list:
        rep+=x[0]+') '+x[1]+'\n'
    reply(t, s, rep)

register_command_handler(hnd_tv2, 'тв2', ['все','инфо'], 0, 'Телепрограмма на сегодня', 'тв2 <номер канала или название>', ['тв2 discovery'])
