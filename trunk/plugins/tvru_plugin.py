#===istalismanplugin===
# -*- coding: utf-8 -*-


def prog_grabru(code, n='1'):
	import urllib2
	import re
	import time

	kod=code.lower()
	kod=kod.strip()
	if kod == '' or not kod.isdecimal():
		program = u'И какой канал мне показывать? Номер канала можно узнать, дав команду боту "тв_лист"'
		return program
	req = urllib2.Request('http://m.tv.yandex.ru/?channel='+kod+'&when='+n+'&day='+prog_listru()[0])
	req.add_header('User-Agent','Mozilla/5.0 (Linux; U; Android 2.2.1; sv-se; HTC Wildfire Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1')
        r = urllib2.urlopen(req).read()
        r = re.findall('<th class="channel">(.*?)Выбор каналов', r, re.DOTALL | re.IGNORECASE)
        if not r:
            program = u'Нет программы на сегодня.'
        else:
            r = r[0]
            r = r.replace('</tr>','\n').replace('</a>',' ')
            r = re.compile(r'<[^<>]*>').sub('', r)
            program = r
	return program

def prog_grabru2(code):
    return prog_grabru(code, n='2')

def prog_listru():
    req = urllib2.Request('http://m.tv.yandex.ru/')
    req.add_header('User-Agent','Mozilla/5.0 (Linux; U; Android 2.2.1; sv-se; HTC Wildfire Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1')

    r = urllib2.urlopen(req).read()
    day = re.findall('<input type="hidden" name="day" value="(.*?)"', r, re.DOTALL | re.IGNORECASE)
    if day: day = day[0]

    try: r = r.split('Все настроенные')[1]
    except: pass

    r = re.findall('<option value="(.*?)">(.*?)</option>', r, re.DOTALL | re.IGNORECASE)

    program=''
    
    r = filter(lambda x : x[0].isdigit(), r)
    r.sort(key = lambda x : int(x[0]))
    for x in r:
        program+=x[0]+' -'+x[1]+',  '
    return day, program

def handler_TVru_get(type, source, parameters):
	reply(type,source, prog_grabru(parameters))

def handler_TVru_get2(type, source, parameters):
	if type == 'public':
		reply(type,source,u'смотри приват!')
	reply('private',source, prog_grabru2(parameters))

def handler_TVru_list(type, source, parameters):
	if type == 'public':
		reply(type,source,u'смотри приват!')
	rep=''
	f=prog_listru()[1]
	reply('private',source, f)

def tv_sort(a, b):
        a=a[:5]
        b=b[:5]
        a=a[-1:]
        b=b[-1:]
        if a>b:
                return 1
        if a<b:
                return -1
        return 0

def handler_TVru_search(type, source, parameters):
        if not parameters or parameters.isspace():
                return
        parameters=parameters.lower()
	if type == 'public':
		reply(type,source,u'смотри приват!')
	rep=''
	f=prog_listru()[1].split(',')
	for x in f:
                x=x.decode('utf-8','replace')
                x=x.lower()
                if x.count('-'):
                        c=x.split('-')[1]
                        if c.count(parameters):
                                rep+=x+'\n'
        if not rep or rep.isspace():
                reply('private', source, u'Ничего не найдено!')
                return
	reply('private',source, rep)

register_command_handler(handler_TVru_search, 'тв_найти', ['фан','все'], 0, 'Ищет код по названию канала или по совпадению', 'тв_найти канал', ['тв_найти Discovery'])	
register_command_handler(handler_TVru_get2, 'тв_полностью', ['фан','все'], 11, 'Показать телепрограму для определенного канала. Каналы можно просмотреть в команде "тв_лист"', 'тв_полностью [номер канала]', ['тв_полностью 144'])
register_command_handler(handler_TVru_get, 'тв', ['фан','все'], 0, 'Показать телепрограму для определенного канала. Каналы можно просмотреть в команде "тв_лист"', 'тв [номер канала]', ['тв 144'])
register_command_handler(handler_TVru_list, 'тв_лист', ['фан','все'], 0, 'Просмотреть номера каналов чтобы потом узнать телепрограму', 'тв_лист', ['тв_лист'])
