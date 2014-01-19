#===istalismanplugin===
# -*- coding: utf-8 -*-


def gramota_q(type, source, parameters):
    try:
        if len(parameters)>27:
            return
        if not parameters:
            return
        p=''
        adr='http://www.gramota.ru/slovari/dic/?lop=x&bts=x&word='
        z=urllib.quote(parameters.encode('cp1251'))
        page = urllib.urlopen(adr+z)
        r=page.read()
        r=unicode(r,'cp1251')
        f=re.findall('<div style="p[^>]*?>(.+)</',r)
        if len(f)<2:
            reply(type, source, u'Искомое слово отсутствует!')
            return
        p=u'Орфографический словарь:\n'+f[0]+u' Большой толковый словарь:\n'+f[1]#"\n".join(f)
        try:
            p=decode_log(p)
        except:
            p=decode(p)
        if p=='':
            reply(type, source, u'Нет результатов!')
            return
        reply(type, source, p)#unicode(p,'cp1251'))
    except Exception, err:
        reply(type, source, u'Произошла ошибка!')

def hnd_zhargon(t, s, p):
    rep=''
    try: db = read_file('dynamic/zhargon.txt').decode('utf8').splitlines()
    except:
        reply(t, s, u'Что-то с базой dynamic/zhargon.txt')
        return
    if not p:
        reply(t, s, random.choice(db))
        return
    for x in db:
        r=x.split('-')
        if r and r[0].strip().lower()==p.lower():
            rep+=x
    if not rep or rep.isspace():
        reply(t, s, u'Ничего не найдено!')
        return
    reply(t, s, rep)
    
    
register_command_handler(hnd_zhargon, 'жаргон', ['все'], 0, 'Толкование слова из воровского жаргона.\nБез параметров выдаст случайное слово.', 'жаргон <слово>', ['жаргон гастролеры'])
register_command_handler(gramota_q, '!словарь', ['все'], 0, 'Проверка слова в грамматическом словаре, поиск слова в большом толковом словаре http://gramota.ru', '!словарь <слово>', ['!словарь чес*ный'])

