#===istalismanplugin===
# /* coding: utf8 */

Langs = {'en': u'Английский',
			'ja': u'Японский', 
			'ru': u'Русский', 
			'auto': u'Авто', 
			'sq': u'Албанский', 
			'ar': u'Арабский', 
			'af': u'Африкаанс', 
			'be': u'Белорусский', 
			'bg': u'Болгарский', 
			'cy': u'Валлийский', 
			'hu': u'Венгерский', 
			'vi': u'Вьетнамский', 
			'gl': u'Галисийский', 
			'nl': u'Голландский', 
			'el': u'Греческий', 
			'da': u'Датский', 
			'iw': u'Иврит', 
			'yi': u'Идиш', 
			'id': u'Индонезийский', 
			'ga': u'Ирландский', 
			'is': u'Исландский', 
			'es': u'Испанский', 
			'it': u'Итальянский', 
			'ca': u'Каталанский', 
			'zh-CN': u'Китайский', 
			'ko': u'Корейский', 
			'lv': u'Латышский', 
			'lt': u'Литовский', 
			'mk': u'Македонский', 
			'ms': u'Малайский', 
			'mt': u'мальтийский', 
			'de': u'Немецкий', 
			'no': u'Норвежский', 
			'fa': u'Персидский', 
			'pl': u'Польский', 
			'pt': u'Португальский', 
			'ro': u'Румынский', 
		 	'sr': u'Сербский', 
		 	'sk': u'Словацкий', 
		 	'sl': u'Словенский',
		 	'sw': u'Суахили', 
		 	'tl': u'Тагальский', 
		 	'th': u'Тайский', 
		 	'tr': u'Турецкий', 
		 	'uk': u'Украинский', 
		 	'fi': u'Финский', 
		 	'fr': u'Французский', 
		 	'hi': u'Хинди', 
		 	'hr': u'Хорватский', 
		 	'cs': u'Чешский', 
		 	'sv': u'Шведский', 
		 	'et': u'Эстонский'}

from goslate import goslate

def babla_hnd(t, s, p):
        if p:
                p = p.replace(' ','-')
                z = urllib.urlopen('http://www.babla.ru/английский-русский/'+p.encode('utf8','replace')).read()
                page = re.findall('Краткое содержание(.*?)полное описание', z)
                page2 = re.findall('варианты переводов в англо-русском словаре(.*?)</section>',z,re.DOTALL|re.IGNORECASE)
                if not page:
                        if not page2:
                                reply(t, s, u'Ничего не найдено')
                                return
                        page = page2
                page = page[0]
                page = page.replace('&nbsp',' ').replace('</a></p>','\n')
                page = decode(page)
                page = page.replace('\n\n','\n')
                reply(t, s, page)

register_command_handler(babla_hnd, 'en', ['инфо','все'], 0, 'Просмотр слова в английском словаре www.babla.ru', 'en <текст>', ['en fart'])

def gTrans(tLang, text):
        gs = goslate.Goslate()
	try:
		return gs.translate(text, tLang)
	except Exception, e:
		return "%s: %s" % (e.__class__.__name__, e.message)

def gAutoTrans(mType, source, text):
        gs = goslate.Goslate()
	if text:
		try:
                        i = gs.detect(text)
                except:
                        i = 'en'
		
		
		if i == u'ru':
                        repl = Langs.get(i,u'Неизвестно')+u' -> Английский: \n'+gTrans("en", text)
		else:
			repl = Langs[i]+u' -> Русский: \n'+gTrans("ru", text)
	else:
		repl = u"Недостаточно параметров."
	reply(mType, source, repl)

def gTransHandler(mType, source, args):
	if args and len(args.split()) > 2:
                reply(mType, source, u'Используйте команду <!>:\n! you word')
		#(fLang, tLang, text) = args.split(None, 2)
		#reply(mType, source, u"Перевод %s => %s:\n%s" % (fLang, tLang, gTrans(fLang, tLang, text).decode("utf-8")))
	else:
		answer = u"\nДоступные языки:\n"
		for a, b in enumerate(sorted([x + u" — " + y for x, y in Langs.iteritems()])):
			answer += u"%i. %s.\n" % (a + 1, b)
		reply(mType, source, answer.encode("utf-8"))

register_command_handler(gTransHandler, 'перевод', ['инфо','все'], 0, 'Переводчик.\nПеревод с одного языка на другой. Используется Google Translate.', 'перевод <исходный_язык> <нужный_язык> <текст>', ['перевод en ru hello world', 'перевод ru en привет, мир'])
register_command_handler(gAutoTrans, '!', ['инфо','все'], 0, 'Перевод с одного языка на другой с автоопределением. Используется Google Translate.', '! <текст>', ['! hello', '! привет'])
