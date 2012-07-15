#===istalismanplugin===
# -*- coding: utf-8 -*-

import urllib2,re,urllib

from re import compile as re_compile

strip_tags = re_compile(r'<[^<>]+>')

def handler_bashorgru_get(type, source, parameters):
	if parameters.strip()=='':
		req = urllib2.Request('http://bash.org.ru/random')
	else:
		req = urllib2.Request('http://bash.org.ru/quote/'+parameters.strip())
		req.add_header = ('User-agent', 'Mozilla/5.0')
	try:
		r = urllib2.urlopen(req)
		target = r.read()
		target = re.compile(r'<script.*?>.*?</script>',re.DOTALL | re.IGNORECASE).sub('', target)
		"""link to the quote"""
		msg = re.findall('<div class=\"text\">(.*?)</div>', target)[0]
		msg = msg.replace('&quot;','\"').replace('&gt;',':').replace('<br>','\n')
		reply(type,source,unicode(msg,'windows-1251'))
	except:
		reply(type,source,u'очевидно, они опять сменили разметку')
            

def decode_s(text):
    return strip_tags.sub('', text.replace('<br />','\n').replace('<br>','\n')).replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('\t','').replace('||||:]','').replace('>[:\n','')

def decode(text):
    return strip_tags.sub('', text.replace('<br />','\n').replace('<br>','\n')).replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('\t','').replace('||||:]','').replace('>[:\n','')

def handler_prazdnik(type, source, parameters):
    try:
        req = urllib2.Request('http://wap.n-urengoy.ru/cgi-bin/wappr.pl')
        req.add_header = ('User-agent', 'Mozilla/5.0')
        r = urllib2.urlopen(req)
        target = r.read()
        od = re.search('<div class="title">',target)
        message = target[od.end():]
        message = message[:re.search('назад',message).start()]
        message = '\n' + message.strip()
        message = message.replace('<','').replace('.','').replace('>','').replace('/','\n').replace('_','').replace('a','').replace('s','').replace('d','').replace(':','').replace('f','').replace('g','').replace('h','').replace('=','').replace('-','').replace('j','').replace('k','').replace('l','').replace('q','').replace('%','').replace('w','').replace('e','').replace('r','').replace('t','').replace('y','').replace('u','').replace('i','').replace('"','').replace('o','').replace('p','').replace('z','').replace('x','').replace('c','').replace('v','').replace('#','').replace('b','').replace('n','').replace('m','').replace('A','').replace('S','').replace('D','').replace('F','').replace('G','').replace('H','').replace('K',' ').replace('L',' ').replace('Q',' ').replace('W',' ').replace('E','')
        message = message.replace('Y','').replace('<br/>','\n').replace('I','').replace('O','').replace('P','').replace('Z','').replace('X','').replace('C','').replace('V','').replace('B','').replace('N','').replace('M','').replace(';','').replace('[','').replace(']','')
        if message.isspace():
                reply(type,source,u'наверно разметку сменили')
                return
        reply(type, source, unicode(message,'UTF-8'))
    except:
            reply(type, source, u'неизвестная ошибка')

def handler_jc_show(type, source, parameters):
    try:
      if parameters:
        req = urllib2.Request('http://jc.jabber.ru/search.html?search='+parameters.encode('utf-8'))
        req.add_header = ('User-agent', 'Mozilla/5.0')
        r = urllib2.urlopen(req)
        target = r.read()
        od = re.search('<div align="left">',target)
        message = target[od.end():]
        message = message[:re.search('</ol>',message).start()]
        message = decode_s(message)
        message = '\n' + message.strip()
        message = message.replace('<a href="','').replace('\n\n','\n ').replace('" target="_blank">','').replace('</a>','').replace('</font>','').replace('<font color="gray">',' ').replace('&nbsp;','').replace('?join','').replace('<ol start=1>','').replace('<li>','').replace('<font color="blue">','').replace('</div>','').replace('<b>','').replace('</b>','').replace('<br/>',' ').replace('<br>',' ').replace('<div class="info">',' ').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"')
        reply(type, source, unicode(message,'UTF-8'))
      else:
        reply(type, source, u'а что искать то?')
    except:
        reply(type, source, u'По вашему запросу ничего не найдено')

def handler_lurk(type, source, parameters):
        try:
                if parameters:
                        req = urllib2.Request('http://lurkmore.to/'+parameters.encode('utf-8'))
                        req.add_header = ('User-agent', 'Opera')
                        i = urllib2.urlopen(req)
                        page = i.read()
                        target=''
                        t = re.findall('<p>.*.',page,re.DOTALL | re.IGNORECASE)
                        for x in t:
                                x=x.replace('</p>','\n')
                                if not x.count('.') and not x.isspace():
                                        if x!='':
                                                x+'.'
                                target+=x
                        target = target.replace('if (window.showTocToggle) { var tocShowText = "показать"; var tocHideText = "убрать"; showTocToggle(); }','').replace('<br /','')
                        target = decode_s(target)
                        if target.isspace():
                                reply(type, source, u'аблом!')
                                return
                        reply(type,source,target.replace('\n\n','\n'))
                else:
                        reply(type, source, u'лурк - это тема,только слово еще напиши!')
                        return
        except:
                reply(type, source, u'Ничего не найдено!')

def handler_anek_s(type,source,parameters):
        reklama = [u'']
        try:
                u = urllib.urlopen('http://anekdot.odessa.ua/rand-anekdot.php')
                target = u.read()
                od = re.search('>',target)
                h1 = target[od.end():]
                h1 = h1[:re.search('<a href=',h1).start()]
                message = decode_s(h1)
                reply(type ,source, u'Анекдот: \n'+unicode(message,'windows-1251'))
        except:
                reply(type ,source, u'Упс.. Сайт упал..')

def clck_quest(type,source,parameters):
        if parameters:
                try:
                        fetcher = urllib2.urlopen('http://clck.ru/--?url='+parameters.encode('utf-8'))
                        rep=fetcher.read()
                        reply(type,source,rep)
                except:
                        reply(type,source,'что-то сломалось!')
                        pass

def hnd_fun_k(type,source,parameters):
        ALL=[]
        if type in ['private','icq','chat']:
                return
        NO=[u'дал па галаве веником',u'нехватило',u'не насыпал',u'плюнул в миску']
        if source[1] in GROUPCHATS:
                n=0
                for x in GROUPCHATS[source[1]]:
                        if GROUPCHATS[source[1]][x]['ishere']==1:
                                n+=1
                                ALL.append(x)
                if n<3:
                        reply(type,source,u'зови народ,тогда и зохаваем!')
                        return
                no=random.choice(ALL)
                yes=''
                for x in ALL:
                        if x!=no:
                                yes+=u'насыпал '+x+'\n'
                msg(source[3], source[1], yes)
                time.sleep(1.5)
                msg(source[3], source[1],u'a '+no+' '+random.choice(NO))

def hnd_lust_ru(type,source,parameters):
        #http://www.notproud.ru/lust/
        try:
                req = urllib2.Request('http://www.notproud.ru/random.html')
                req.add_header = ('User-agent', 'Mozilla/5.0')
                r = urllib2.urlopen(req)
                text = r.read()
                od = re.search('<td align="left" valign="top" class="font2">',text)
                rep = text[od.end():]
                rep = rep[:re.search('</tr>',rep).start()]
                rep=decode_s(rep)
                if rep=='':
                        return
                if rep.isspace():
                        reply(type,source,u'наверное разметку сменили')
                        return
                reply(type,source,unicode(rep,'windows-1251'))
        except:
                reply(type,source,u'')

def hnd_drem_talk(type,source,parameters):
        try:
                if not parameters:
                        return
                if parameters.count(' '):
                        parameters=parameters.replace(' ','+')
                page = urllib2.Request('http://2yxa.ru/pics/sonnik.php?poisk='+urllib.quote(parameters.encode('utf8')))
                s = urllib2.urlopen(page).read()
                s = s.replace('<br/>',' ')
                s = re.compile(r'<a href=".*?">.*?</a>',re.DOTALL | re.IGNORECASE).sub('', s)
                s = re.compile(r'<style[^<>]*?>.*?</style>',re.DOTALL | re.IGNORECASE).sub('', s)
                s = re.compile(r'<script.*?>.*?</script>',re.DOTALL | re.IGNORECASE).sub('', s)
                s = re.compile(r'<[^<>]*>').sub('', s)
                s = s.replace('|','').replace('\n\n','').replace('&nbsp;','').replace('&gt;','')
                if s=='' or s.isspace():
                        return
                reply(type,source,unicode(s,'utf-8'))
                
        except:
                reply(type,source,u'ooops! parser get some error!')

def hnd_darvin_p(type,source,parameters):
        try:
                n=str(random.randrange(1,700))
                page = urllib.urlopen('http://2yxa.ru/darwin/?st='+n.encode('utf-8'))
                s = page.read()
                od = re.search('<body>',s)
                message = s[od.end():]
                message = message[:re.search('<div class="b">',message).start()]
                message = message.replace('<br/>','\n').replace('\n\n','')
                message = decode_s(message)
                if message=='' or message.isspace():
                        return
                reply(type,source,unicode(message,'utf-8'))
        except:
                pass

def kill_me_quotes(type, source, parameters):
        try:
                tim=time.time()
                rep=''
                while not rep and time.time()-tim<3:
                        n=str(random.randrange(1, 7400))
                        url=urllib.urlopen('http://killmepls.ru/story/'+n).read()
                        rep = re.findall('<a href="/story/.*">.*</b>', url, re.DOTALL | re.IGNORECASE)
                if rep:
                        rep = rep[0]
                        txt = decode(rep)
                        txt = '\n'.join([x for x in txt.splitlines() if not x.isspace()])
                        txt = txt.replace('&#151;','')
                        reply(type, source, txt)
        except:
                reply(type, source, u'Рандомная цитата не найдена!')

def hnd_poem(type, source, parameters):
        a=[u"Я помню",u"Не помню",u"Забыть бы",u"Купите",u"Очкуеш",u"Какое",u"Угробил",u"Хреново",u"Открою",u"Ты чуешь?"]
        b=[u"чудное",u"странное",u"некое",u"вкусное",u"пьяное",u"свинское",u"чоткое",u"сраное",u"нужное",u"конское"]
        c=[u"мнгновенье",u"затменье",u"хотенье",u"варенье",u"творенье",u"везенье",u"рожденье",u"смущенье",u"печенье",u"ученье"]
        d=[u"передомной",u"под косячком",u"на кладбище",u"в моих мечтах",u"под скальпилем",u"в моих штанах",u"из-за угла",u"в моих ушах",u"в ночном горшке",u"из головы"]
        e=[u"явилась ты",u"добилась ты",u"торчат кресты",u"стихов листы",u"забилась ты",u"мои трусы",u"поют дрозды",u"из темноты",u"помылась ты",u"дают пизды"]
        f=u'как'
        g=[u"мимолётное",u"детородное",u"психотропное",u"кайфоломное",u"очевидное",u"у воробушков",u"эдакое вот",u"нам не чуждое",u"благородное",u"ябывдульское"]
        j=[u"виденье",u"сиденье",u"паренье",u"сужденье",u"вращенье",u"сношенье",u"смятенье",u"теченье",u"паденье",u"сплетенье"]
        h=[u"как гений",u"как сторож",u"как символ",u"как спарта",u"как правда",u"как ангел",u"как водка",u"как пиво","как ахтунг",u"как жопа"]
        i=[u"чистой",u"вечной",u"тухлой",u"просит",u"грязной",u"липкой",u"на хрен",u"в пене",u"женской",u"жаждет"]
        k=[u"красоты",u"мерзлоты",u"суеты",u"наркоты",u"срамоты",u"школоты",u"типа ты",u"простоты",u"хуиты",u"наготы"]
        reply(type, source, random.choice(a)+'\n'+random.choice(b)+'\n'+random.choice(c)+'\n'+random.choice(d)+'\n'+random.choice(e)+'\n'+f+' '+random.choice(g)+'\n'+random.choice(j)+'\n'+random.choice(h)+'\n'+random.choice(i)+'\n'+random.choice(k))

register_command_handler(hnd_poem, 'poem', ['все'], 0, 'random poem', 'poem', ['poem'])                                        
register_command_handler(kill_me_quotes, 'killme', ['все'], 0, 'http://killmepls.ru/', 'killme', ['killme'])                                        
register_command_handler(hnd_darvin_p, 'дарвин', ['все'], 0, 'премия дарвина', 'дарвин', ['дарвин'])                                        
register_command_handler(hnd_drem_talk, 'сон', ['все'], 0, 'толкование сна по ключевому слову', 'сон <слово>', ['сон деньги'])                                
register_command_handler(hnd_lust_ru, 'признание', ['фан','все'], 0, 'признание с http://www.notproud.ru/lust/', 'признание', ['признание'])                
register_command_handler(hnd_fun_k, 'каша', ['фан','все'], 0, 'раздача каши', 'каша', ['каша'])                
register_command_handler(clck_quest, 'clck', ['фан','все'], 0, 'Выдает короткую ссылку взамен введенного URL', 'clck <url>', ['clck http://40tman.ucoz.ru'])
register_command_handler(handler_anek_s, 'анекдот', ['фан','все'], 0, 'Случайный анекдот из http://wap.obas.ru/', 'анекдот', ['анекдот'])
register_command_handler(handler_lurk, 'лурк', ['инфо','фан','все'], 0, 'Показывает статью из http://lurkmore.ru/','лурк <слово>', ['лурк херка'])
register_command_handler(handler_jc_show, 'jc', ['все','mod','инфо'], 0, 'Поиск конференций в рейтинге jc.jabber.ru', 'jc <конфа>', ['jc goth'])
register_command_handler(handler_jc_show, 'рейтинг', ['все','mod','инфо'], 0, 'Поиск конференций в рейтинге jc.jabber.ru', 'рейтинг <конфа>', ['рейтинг goth'])
register_command_handler(handler_prazdnik, 'праздники', ['все','mod','инфо'], 0, 'Показывает праздники сегодня/завтра', 'праздники', ['праздники'])
register_command_handler(handler_bashorgru_get, 'бор', ['фан','инфо','все'], 0, 'Показывает случайную цитату из бора (bash.org.ru). Также может по заданному номеру вывести.', 'бор', ['бор 223344','бор'])
