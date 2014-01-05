#===istalismanplugin===
# -*- coding: utf-8 -*-


def dehtml(p):
    h = HTMLParser.HTMLParser()
    p = h.unescape(p)
    p = re.compile(r'<[^<>]*>').sub(' ', p)
    return p

cc=''


GLOBAL_TV2 = {}


def msg_tv2(r, t, s, p):
    jid=get_true_jid(s)
    if jid in GLOBAL_TV2.keys():
        if p in GLOBAL_TV2[jid]:
            hnd_tv2(t, s, GLOBAL_TV2[jid][p], sp=1)
            del GLOBAL_TV2[jid][p]

register_message_handler(msg_tv2)


def hnd_tv2(t, s, p, sp=0):
    global GLOBAL_TV2
    #if p.isdigit():
    #    req = urllib2.Request('http://www.teleguide.info/kanal'+p+'.html')
    #    req.add_header('User-Agent', UserAgent().random)
    #    page = urllib2.urlopen(req).read().decode('utf8','ignore')
    #    try: page = '\n'.join(re.findall('(\d{2}:\d{2}.*?)</div>',page,re.DOTALL|re.IGNORECASE)[1:])
    #    except:
    #        reply(t, s, u'Ошибка парсера')
    #        return
    #    reply(t, s, dehtml(page))
    #    return
    list = []
    chan = []
    title, day, a = '','',''
    if not p.isdigit() and not sp:
        req = urllib2.Request('http://www.teleguide.info/kanals.html')
        req.add_header('User-Agent', UserAgent().random)
        page = urllib2.urlopen(req).read().decode('utf8','ignore')
        page = re.findall('<a href="/kanal(\d{1,6}).html" title="(.*?)"',page,re.DOTALL|re.IGNORECASE)
        for x in page:
            if x[1].lower().count(p.lower()) or x[1].lower()==p.lower():
                list.append(x)
        if not list:
            reply(t, s, u'Канал <'+p+u'> не найден!')
            return
    if (list and len(list)==1) or sp or not list:
        
        if not list: a = p
        else: a = (list[0][0] if not sp else p)
        
        req = urllib2.Request('http://www.teleguide.info/kanal'+a+'.html')
        req.add_header('User-Agent', UserAgent().random)
        page = urllib2.urlopen(req).read().decode('utf8','ignore')
        try:
            title = re.findall('<title>(.*?)</title>', page, re.DOTALL | re.IGNORECASE)[0].split('-')[0]
            day = re.findall('<b>\d{1,2} .*?\,.*?</b>',page, re.DOTALL | re.IGNORECASE)#re.findall('<EM>(.*?)</SPAN>', page, re.DOTALL | re.IGNORECASE)[0]
            day = day[len(day)-1]
            if not sp: chan = re.findall('/kanal(\d{1,10}.*?)\.html', page, re.DOTALL | re.IGNORECASE)
        except: pass
        
        global cc
        cc=page
        
        try: #page = '\n'.join(re.findall('(\d{2}:\d{2}.*?(</b>|</a>))',page,re.DOTALL|re.IGNORECASE)[1:])#</div>
            page = '\n'.join([re.split('</b>|</a>',x)[0] for x in re.findall('(\d{2}:\d{2}.*?)</div>',cc,re.DOTALL|re.IGNORECASE)][1:])
        except: return
        page = title+'-'+day+'\n'+page
        if chan:
            jid = get_true_jid(s)
            try:
                GLOBAL_TV2[jid]={'-':chan[0],'+':chan[2]}
                page+=u'\nПиши \"-\",\"+\" для перемещения по дате'
            except: pass
        reply(t, s, dehtml(page))
        return
    rep=''
    for x in list:
        rep+=x[0]+') '+x[1]+'\n'
    reply(t, s, rep)

register_command_handler(hnd_tv2, 'тв2', ['все','инфо'], 0, 'Телепрограмма', 'тв2 <номер канала или название>', ['тв2 discovery'])
