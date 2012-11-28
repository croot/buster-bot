# -*- coding: utf-8 -*-

def hnd_www(type, source, parameters):
    if not parameters: return
    
    if not parameters.count('.'):
        reply(type, source, u'Неверный адрес!')
        return
    if parameters.count('http://'):
        parameters=parameters.replace('http://','')
    try:
        page, url = str(), 'http://'+parameters.encode('utf8')
        
        req = urllib2.Request(url)
        try: req = urllib2.urlopen(req, timeout = 3)
        except urllib2.URLError, e:
            reply(type, source, u'Невозможно открыть указанный адрес!')
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
        page = re.compile(r'<[^<>]*>').sub('', data)
        page = page.replace('\n\n','').replace('&nbsp;','').replace('&gt;','')
        page = '\n'.join([x for x in page.splitlines() if not x.isspace()])
        #page = ''.join(map(lambda x: x.strip(), page.splitlines()))
        reply(type, source, (remove_space(page) if 'remove_space' in globals().keys() else page))
    except:
        #traceback.print_exc()
        reply(type, source, u'Произошла ошибка при обработке страницы')

register_command_handler(hnd_www, 'www', ['все'], 0, 'Получить содержимое веб страницы', 'www url', ['www mail.ru'])
