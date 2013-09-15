# -*- coding: utf-8 -*-

from busterapi import opener

###############

def hnd_www(type, source, parameters):
    
    if not parameters: return

    if parameters.count('localhost') or parameters.count('file://'):
        reply(type, source, u'Куй те в рот!')
        return
    
    if not parameters.count('.'):
        reply(type, source, u'Неверный адрес!')
        return
    opener_ = opener.MyURLOpener()
    onlyt = 0
    if parameters.count('http://'):
        parameters=parameters.replace('http://','')
    if parameters.count(' '):
        ss = parameters.split()
        parameters = ss[0]
        if ss[1].lower() == u'-t':
            onlyt = 1
    try:

        try:
            ctype = opener_.open('http://'+parameters.encode('utf8'), method='HEAD').headers['content-type']
            if ctype[:9] != 'text/html' and (ctype[:17] if len(ctype)>=17 else 'text/html')!='application/xhtml':
                reply(type, source, u'Недопустимый формат '+ctype)
                return
        except: pass
        
        page, url = str(), 'http://'+parameters.encode('utf8')
        
        req = urllib2.Request(url)
        try: req = urllib2.urlopen(req, timeout = 3)
        except urllib2.URLError, e:
            reply(type, source, u'Невозможно открыть указанный адрес ('+str(e.reason)+')')
            return
        except Exception as err:
            reply(type, source, err.message)
            return
        data = req.read()
        cod = chardet.detect(data)['encoding']
        data = unicode(data, cod)
        data = re.compile(r'<style[^<>]*?>.*?</style>',re.DOTALL | re.IGNORECASE).sub('', data)
        data = re.compile(r'<script.*?>.*?</script>',re.DOTALL | re.IGNORECASE).sub('', data)
        if data.count('</style>'):
            data = ''.join(data.split('style')[2:])
        if onlyt and 'remove_link' in globals().keys():
            data = remove_link(data)
        page = page.replace('</a>','\n').replace('<br/>','\n')
        page = re.compile(r'<[^<>]*>').sub(' ', data)
        #page = page.replace('\n\n','').replace('&nbsp;','').replace('&gt;','')
        page = '\n'.join([x for x in page.splitlines() if not x.isspace()])
        #page = ''.join(map(lambda x: x.strip(), page.splitlines()))
        reply(type, source, (remove_space(page) if 'remove_space' in globals().keys() else page))
    except Exception as err:
        reply(type, source, u'Произошла ошибка при обработке страницы ('+err.message+')')

register_command_handler(hnd_www, 'www', ['все'], 0, 'Получить содержимое веб страницы. Ключи \' -t \' вернет только текстовое содержимое страницы исключая ссылки', 'www url <key>', ['www mail.ru'])
