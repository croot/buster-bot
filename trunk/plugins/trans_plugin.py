#===istalismanplugin===
# /* coding: utf8 */


Langs = {'en': u'Английский',
			'ja': u'Японский',
         'kk': u'Казахский',
         'ka': u'Грузинский',
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

try:
        from xmltodict import xmltodict
except:
        pass



def yatr_hnd(t, s, p):
        if not p:
                reply(t, s, u'Что переводить будем?')
                return
        err = {'401':u'Неправильный ключ API','402':u'Ключ API заблокирован','403':u'Превышено суточное ограничение на количество запросов','404':u'Превышено суточное ограничение на объем переведенного текста','422':u'Текст не может быть переведен'}
        i = 'ru'
        key = 'trnsl.1.1.20130421T140201Z.323e508a33e9d84b.f1e0d9ca9bcd0a00b0ef71d82e6cf4158183d09e'
        
        if [x for x in p if ord(x) in range(1040,1103)]:
                i = 'en'
        lc = re.findall('[a-z]{2,}-[a-z]{2,}', p)
        if lc:
                li = lc[0].split('-')
                if li[0] in Langs and li[1] in Langs:
                        i = lc[0]
                        p = p.replace(lc[0],'')
        p = p.encode('utf8','replace')
        p = urllib2.quote(p)
        page = urllib.urlopen('https://translate.yandex.net/api/v1.5/tr/translate?key='+key+'&text='+p+'&lang='+i).read()
        try:
                page = xmltodict.parse(page)
        except NameError:
                reply(t, s, u'Модуль xmltodict не найден!')
                return
        if page.get(u'Translation', None):
                body = page[u'Translation']['text']
        else:
                reply(t, s, err[page[u'Error']['@code']])
                return
        reply(t, s, page[u'Translation']['@lang']+':\n'+body)
        
register_command_handler(yatr_hnd, 'yat', ['инфо','все'], 0, 'Перевод с одного языка на другой с автоопределением. Используется Yandex Translate.', 'yat <текст>', ['yat hello', 'yat en-ar привет', 'yat привет'])       
register_command_handler(yatr_hnd, 'переведи', ['инфо','все'], 0, 'Перевод с одного языка на другой с автоопределением. Используется Yandex Translate.', 'переведи <текст>', ['переведи hello', 'переведи ru-fr мадам у вас прекрасная вагина', 'переведи привет'])       


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


def gTrans(t, s, tLang, text):
        gs = goslate.Goslate()
        print tLang
	try:
		return gs.translate(text, tLang)
	except Exception, e:
                yatr_hnd(t, s, text)
                return u'Внимание! Сервис Google недоступен, используйте след. команды для перевода: yat, en'
		#return "%s: %s" % (e.__class__.__name__, e.message)

def gAutoTrans(mType, source, text):
        gs = goslate.Goslate()
	if text:
		try:
                        i = gs.detect(text)
                        #if [x for x in text if ord(x) in range(1040,1103)]:
                        #        print 'YESSS'
                        #        i = 'ru'
                except:
                        i = 'en'
		
		
		if i == u'ru':
                        repl = Langs.get(i,u'Неизвестно')+u' -> Английский: \n'+gTrans(mType, source, "en", text)
		else:
			repl = Langs.get(i,i)+u' -> Русский: \n'+gTrans(mType, source, "ru", text)
	else:
		repl = u"Недостаточно параметров."
	reply(mType, source, repl)

def gTransHandler(mType, source, args):
	if args and len(args.split()) > 2:
		(fLang, tLang, text) = args.split(None, 2)
		reply(mType, source, u"Перевод %s => %s:\n%s" % (fLang, tLang, gTrans(mType, source, tLang, text)))
	else:
		answer = u"\nДоступные языки:\n"
		for a, b in enumerate(sorted([x + u" — " + y for x, y in Langs.iteritems()])):
			answer += u"%i. %s.\n" % (a + 1, b)
		reply(mType, source, answer.encode("utf-8"))

register_command_handler(gTransHandler, 'перевод', ['инфо','все'], 0, 'Переводчик.\nПеревод с одного языка на другой. Используется Google Translate.', 'перевод <исходный_язык> <нужный_язык> <текст>', ['перевод en ru hello world', 'перевод ru en привет, мир'])
register_command_handler(gAutoTrans, '!', ['инфо','все'], 0, 'Перевод с одного языка на другой с автоопределением. Используется Google Translate.', '! <текст>', ['! hello', '! привет'])
