#===istalismanplugin===
# -*- coding: utf-8 -*-

def ya_weather(t, s, p):
    if not p:
        return
    n=1
    if p.count(' '):
        p=p.split()[0]
        n=2
    p = urllib.quote(p.encode('utf8'))
    page = urllib.urlopen('http://pogoda.yandex.ua/'+p+'/details/').read()
    page = page.split('</th></tr>')
    if len(page)==0:
        reply(t, s, u'Погода сломалась')
        return
    page = page[n]
    page = page.replace('<td class="t"><strong>','\n  - ')
    page = re.compile(r'<[^<>]*>').sub(' ', page)
    page = page.replace('        ','\n').replace('     ','\n').replace('мм','').replace('м/с','').replace('ст.','').replace('рт.','')
    reply(t, s, unicode(page,'UTF-8'))

def ya_week(t, s, p):
    pass
    

register_command_handler(ya_weather, 'погода2', ['все'], 0, 'Погода предоставлена сайтом http://yandex.ua ', 'погода2 <city>', ['погода2 киев','погода2 киев завтра'])
