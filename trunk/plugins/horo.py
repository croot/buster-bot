# -*- coding: utf-8 -*-


if not 'DIGIT_MENU' in globals().keys():
        DIGIT_MENU = {}

HORO_FILE = 'dynamic/horo.txt'

db_file(HORO_FILE, dict)

HOROS = eval(read_file(HORO_FILE))

HORO_RES = {}

def hnd_horoscope(t, s, p):
    jid = get_true_jid(s)
    w = True
    if jid in HOROS.keys() and not p:
        w = False
        p = HOROS[jid]
    if not jid in HOROS.keys() and not p or p.lower()==u'все' or p and not p.isdigit():
        fn = inspect.stack()[0][3]
        DIGIT_MENU[jid]=fn
        url = 'http://2yxa.ru/goroskop/0/'
        try: page = urllib.urlopen(url).read()
        except:
            reply(t, s, u'Немогу открыть URL')
            return
        name = re.findall('<a href=\"/goroskop/\d{1}/\d{1,2}/\">(.*?)</a>',page)
        urls = re.findall('<a href=\"(/goroskop/\d{1}/\d{1,2}/)\">.*?</a>',page)
        d = {}
        n = 0
        rep = ''
        for (a, b) in zip(name, urls):
            a = a.lower()
            d[a]=b
            n+=1
            rep+=str(n)+') '+a+'\n'
        if not d:
            reply(t, s, u'Гороскоп недоступен!')
            return
        reply(t, s, rep)
    if p and p.isdigit():
        url = 'http://2yxa.ru/goroskop/0/'+p
        page = universal_html_parser(urllib.urlopen(url).read())
        page = re.compile(r'\d{2}:\d{2}:\d{2}',re.DOTALL | re.IGNORECASE).sub('', page)
        reply(t, s, page)
        if w:
            HOROS[jid] = p
            write_file(HORO_FILE, str(HOROS))
            reply(t, s, u'Запомнил ваш знак! Можете использовать команду без параметров!')


register_command_handler(hnd_horoscope, 'гороскоп', ['все'], 0, 'Гороскоп. Ключ <все> покажет выбор из знаков.', 'гороскоп', ['гороскоп'])
