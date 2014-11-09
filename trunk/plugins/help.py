# -*- coding: utf-8 -*-

GLSRCINFO = {}
CLSRCINFO_FILE = 'dynamic/glscrinfo_chats.txt'

db_file(CLSRCINFO_FILE, dict)

import operator
import unicodedata

searchbyinfo_con, searchbyinfo_cl, searchbyinfo_factory, searchbyinfo_bot = None, None, None, 0

def searchbyinfo_pass(xs):
        pass

def iqinfo_muc_body(t, s, p):#testing function
        db=eval(read_file(CLSRCINFO_FILE))
        list = []
        rep=''
        for x in db.keys():
                if db[x] and len(db[x])>2:
                        try: list.extend([c.lower() for c in db[x].split() if len(c)>2])
                        except: pass
        D = {}
        for x in list:
                D[x]=list.count(x)
        sr = sorted(D.iteritems(), key=operator.itemgetter(1))
        sr.reverse()
        for x in sr:
                for c in sr[sr.index(x)][0]:
                        try:
                                if unicodedata.category(c) in ['Lo']:
                                        continue
                        except: pass
                if sr.index(x)>99: continue
                rep+=sr[sr.index(x)][0]+' '+str(sr[sr.index(x)][1])+'\n'
        reply(t, s, rep)

###register_command_handler(iqinfo_muc_body, 'мукобзор', ['хелп','инфо','все'], 0, 'Самые часто встречаемые слова в описании конф.', 'мукобзор', ['мукобзор'])
                        

def chat_disco_info(typ, ss, p):
        global GLSRCINFO
        global CLSRCINFO_FILE
        global searchbyinfo_bot

        if p.count(' ')>2: return
        if not p or len(p)<3:
                reply(typ, ss, u'Напиши не менее трех букав!')
                return
        
        p, rep, db = p.lower(), str(), eval(read_file(CLSRCINFO_FILE))
        
        if not db or len(db)<400 or time.time()-os.path.getmtime(CLSRCINFO_FILE)>(86400*2):
                reply(typ, ss, u'База обновляется, подождите пару минут..')
                i=searchbyinfo_con()
                tim = time.time()
                while not searchbyinfo_bot and time.time()-tim<26:
                        time.sleep(1)
                        pass
                if not searchbyinfo_bot:
                        try: searchbyinfo_d()
                        except: pass
                        reply(typ, ss, u'Поиск остановлен из-за неудачной попытки подключения! Попробуйте позже!')
                        return
                for x in ['conference.jabber.ru','conference.xmpp.ru','conference.qip.ru','conference.jabbrik.ru','conference.ya.ru','conference.mafiozo.in','conference.jabber.ua']:
                        hnd_glsrcinfo_disco(ss, x)
                time.sleep(180)
                if GLSRCINFO and len(GLSRCINFO)>400:
                        write_file(CLSRCINFO_FILE, str(GLSRCINFO))
                        db = eval(read_file(CLSRCINFO_FILE))
                        
        for x in db.keys():
                if db[x].lower().count(p):
                        inf = db[x]
                        if len(inf)>50:
                                inf = inf[:50]+'...'
                        rep+=x+' - '+inf+'\n'
        if not rep or rep.isspace():
                reply(typ, ss, u'Совпадений нет!')
        else:
                reply(typ, ss, u'База '+str(len(GLSRCINFO))+u' конференций, совпадения:\n'+rep)
        searchbyinfo_bot = 0
        searchbyinfo_d()
        GLSRCINFO = None
        GLSRCINFO = {}

def hnd_glsrcinfo_quest(ss, chat):
    packet = IQ(searchbyinfo_cl, 'get')
    packet.addElement('query', 'http://jabber.org/protocol/disco#info')
    packet.addCallback(chat_items_result_handler, chat)
    reactor.callFromThread(packet.send, chat)


def hnd_glsrcinfo_disco(ss, x):
        packet = IQ(searchbyinfo_cl, 'get')
        packet.addElement('query', 'http://jabber.org/protocol/disco#items')
        packet.addCallback(glsrcinfo_disco_result_handler, ss)
        reactor.callFromThread(packet.send, x)

def glsrcinfo_disco_result_handler(ss, x):
    if x['type'] == 'result':
        query = element2dict(x)['query']
        query = [i.attributes for i in query.children if i.__class__==domish.Element]
        r = [i['jid'] for i in query]
        lim = 350
        if x['from'] in ['conference.qip.ru']:
                lim = 100
        l = []
        for i in query:
                try: g = re.search('^(.+)\(([0-9]+)\)$', i['name']).groups()
                except: g = (i['name'], '0')
                if int(g[1]) < 99: l.append((g[0], i['jid'], g[1]))
        l.sort(lambda x, y: cmp(int(y[2]), int(x[2])))
        l = [i[1] for i in l]
        try: r = l[:lim]
        except: r = l
        for n in r:
                hnd_glsrcinfo_quest(ss, n)

def chat_items_result_handler(chat, x):
        if x['type']=='result':
                query = element2dict(x)['query']
                if query.children:
                        for x in query.children:
                                if x.uri == 'jabber:x:data':
                                        try: GLSRCINFO[chat] = unicode(getTag(x.children[1],'value'))
                                        except: pass

def authd_searchbyinfo(xmlstream):
    #presence = domish.Element(('jabber:client','presence'))
    #xmlstream.send(presence)
    global searchbyinfo_cl
    global searchbyinfo_bot
    searchbyinfo_cl = xmlstream
    searchbyinfo_bot = 1

def searchbyinfo_d():
    global searchbyinfo_cl
    global searchbyinfo_con
    global searchbyinfo_factory

    if hasattr(searchbyinfo_cl, 'transport') and hasattr(searchbyinfo_cl.transport, 'abortConnection'):
            try: searchbyinfo_cl.transport.abortConnection()
            except: pass
            
    if hasattr(searchbyinfo_con, 'transport') and hasattr(searchbyinfo_con.transport, 'abortConnection'):
            try: searchbyinfo_con.transport.abortConnection()
            except: pass

    if hasattr(searchbyinfo_factory, 'stopTrying'): searchbyinfo_factory.stopTrying()
    if hasattr(searchbyinfo_con, 'disconnect'): searchbyinfo_con.disconnect()
    searchbyinfo_con = None
    searchbyinfo_factory = None
    searchbyinfo_cl = None

def searchbyinfo_con():
    myJid = jid.JID(JABBER_ID+'/search+'+str(random.randrange(1,999)))
    global searchbyinfo_factory
    searchbyinfo_factory = client.basicClientFactory(myJid, JABBER_PASS)
    searchbyinfo_factory.addBootstrap('//event/stream/authd', authd_searchbyinfo)
    searchbyinfo_factory.addBootstrap('//event/client/basicauth/authfailed', searchbyinfo_pass)
    searchbyinfo_factory.addBootstrap('//event/client/basicauth/invaliduser', searchbyinfo_pass)
    searchbyinfo_factory.addBootstrap(xmlstream.STREAM_END_EVENT, searchbyinfo_pass)
    searchbyinfo_factory.addBootstrap(xmlstream.STREAM_ERROR_EVENT, searchbyinfo_pass)
    global searchbyinfo_con
    searchbyinfo_con = reactor.connectTCP(JABBER_ID.split('@')[1], 5222, searchbyinfo_factory)
                                        
                

register_command_handler(chat_disco_info, 'найтиконфу', ['хелп','инфо','все'], 0, 'Поиск конфы по совпадениям в описании', 'найтиконфу <тематика>', ['найтиконфу python'])

CMD_GUIDE = {}

def hnd_cmd_guide(t, s, p):
        fn = inspect.stack()[0][3]
        jid = get_true_jid(s)
        rep = str()
        n = 1
        if not p.isdigit():
                l = []; [l.extend(COMMANDS[x]['category']) for x in COMMANDS]
                #l = [x.decode('utf-8') for x in l]
                l = set(l)
                CMD_GUIDE[jid] = {}
                rep+=u'Выберите категорию интересующих вас команд:\n'
                for x in l:
                      CMD_GUIDE[jid][str(n)] = x
                      rep+=str(n)+') '+x.decode('utf8')+'\n'
                      n+=1
                      
                DIGIT_MENU[jid] = fn
                reply(t, s, rep)
                return
        else:
                if not jid in CMD_GUIDE:
                        return

        cat = CMD_GUIDE[jid][p]
        
        i = [x for x in COMMANDS.keys() if cat in COMMANDS[x]['category']]
        i.sort()
        for x in i:
                try:
                        if not user_level(s, s[1])>=COMMANDS[x]['access']:
                                continue
                        a = COMMANDS[x]['desc'].decode("utf-8")
                except: continue
                if len(a)>80:
                        a = a[:80]+'...'
                rep+= x+' - '+a+'\n'
        reply(t, s, u'Всего команд в данной категории '+str(len(i))+u':\n'+rep)
        del CMD_GUIDE[jid][p]

register_command_handler(hnd_cmd_guide, 'комгид', ['хелп','инфо','все'], 0, 'Выводит все команды и краткое описание к ним.', 'комгид', ['комгид'])

def handler_search_in_cmd(t, s, p):
        if not p: return
        if len(p)<2:
                reply(t, s, u'Что за запрос такой?')
                return
        p = p.lower()
        list = []
        for x in COMMANDS.keys():
                try:
                        desc = COMMANDS[x]['desc'].decode("utf-8","replace")
                        desc = desc.lower()
                        if (desc.count(p) or x.count(p)) and not x in list:
                                list.append(x)
                except: pass
        if list:
                rep = ''
                for x in list:
                        try: rep+=str(list.index(x)+1)+u') '+x+u':\n'+COMMANDS[x]['desc'].decode("utf-8")+'\n'
                        except: pass
                reply(t, s, rep)
        else:
                reply(t, s, u'Увы, ничего не нашел!')

register_command_handler(handler_search_in_cmd, 'компоиск', ['хелп','инфо','все'], 0, 'Поиск команды по ключевым словам в описании.', 'компоиск [слово]', ['компоиск спам'])
                

def handler_help_help(type, source, parameters):
	ctglist = []
	rep = str()
	if not parameters:
                rep += u'Узнать мои команды можно написав <команды все>\n глянуть полный список команд с кратким описанием <комгид>,\n так же можете найти интересующую вас команду по ключевым фразам в описании <компоиск слово> - представляет собой гугль по командам бота.\n'
                rep += u'Детальная информация о боте - команда about'
                reply(type, source, rep)
                return
	if parameters and COMMANDS.has_key(parameters.strip()):
		rep = COMMANDS[parameters.strip()]['desc'].decode("utf-8") + u'\nКатегории: '
		for cat in COMMANDS[parameters.strip()]['category']:
			ctglist.append(cat)
		rep += ', '.join(ctglist).decode('utf-8')+u'\nИспользование: ' + COMMANDS[parameters.strip()]['syntax'].decode("utf-8") + u'\nПримеры:'
		for example in COMMANDS[parameters]['examples']:
			rep += u'\n  >>  ' + example.decode("utf-8")
		rep += u'\nНеобходимый уровень доступа: ' + str(COMMANDS[parameters.strip()]['access'])
	else:
		rep = u'Команда <'+parameters+u'> не найдена!'
	reply(type, source, rep)

def handler_help_commands(type, source, parameters):
	date=time.strftime('%d %b %Y (%a)', time.gmtime()).decode('utf-8')
	groupchat=source[1]
	if parameters:
		rep,dsbl = [],[]
		total = 0
		param=parameters.encode("utf-8")
		catcom=set([((param in COMMANDS[x]['category']) and x) or None for x in COMMANDS]) - set([None])
		if not catcom:
			reply(type,source,u'а есть и такая? :-O')
			return
		for cat in catcom:
			if has_access(source, COMMANDS[cat]['access'],groupchat):
				if source[1] in COMMOFF:
					if cat in COMMOFF[source[1]]:
						dsbl.append(cat)
					else:
						rep.append(cat)
						total = total + 1
				else:
					rep.append(cat)
					total = total + 1					
		if rep:
			if type == 'groupchat':
				reply(type,source,u'ушли')
			rep.sort()
			answ=str()
			if u'комгид' in COMMANDS.keys(): answ+=u'Для вывода списка всех команд и краткой информации о них используем команду < комгид >'
			answ+=u'Список команд в категории <'+parameters+u'> на '+date+u':\n\n' + u', '.join(rep) +u' - ('+str(total)+u' штук)'
			if dsbl:
				dsbl.sort()
				answ+=u'\n\nСледующие команды отключены в этой конференции:\n\n'+', '.join(dsbl)
			reply('chat', source,answ)
		else:
			reply(type,source,u'размечтался ]:->')
	else:
		cats = set()
		for x in [COMMANDS[x]['category'] for x in COMMANDS]:
			cats = cats | set(x)
		cats = ', '.join(cats).decode('utf-8')
		if type == 'groupchat':
			reply(type,source,u'ушли')
		reply('chat', source, u'Список категорий на '+date+u'\n'+ cats+u'\n\nДля просмотра списка команд содержащихся в категории наберите "команды категория" без кавычек, например "команды все"')


def hnd_about(t, s, p):
        reply(t, s, u'Я бот - Buster, а по-русски болван.\n Моей основой послужил всеми известный бот Talisman,\n с целью улучшить стабильность работы и выдержку больших нагрузок меня перевели на Twisted Framework. \nВ моем функционале есть много различных команд, в том числе игра мафия и поддержка многих других полезных и не очень функций.\nОсновной акцент делался на мою работу в сети Jabber, включая поддержку MUC, но я так же могу работать в ICQ, IRC, MMP(Mail Agent).\nМой исходный код на момент написания этого текста можно глянуть здесь: https://buster-bot.googlecode.com/svn/trunk')

register_command_handler(handler_help_help, 'помощь', ['хелп','инфо','все'], 0, 'Даёт основную справку или посылает информацию об определённой команде.', 'помощь [команда]', ['помощь', 'помощь пинг'])
register_command_handler(handler_help_commands, 'команды', ['хелп','инфо','все'], 0, 'Показывает список всех категорий команд. При запросе категории показывает список команд находящихся в ней.', 'команды [категория]', ['команды','команды все'])
register_command_handler(hnd_about, 'about', ['хелп','инфо','все'], 0, 'Основная информация о боте.', 'about', ['about'])
