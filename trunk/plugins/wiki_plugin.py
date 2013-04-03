#===istalismanplugin===
# -*- coding: utf-8 -*-

import HTMLParser

def wiki_q(type, source, parameters):
    try:

        if not parameters or parameters.isspace():
            reply(type, source, 'и?')
            return

        jid, parameters = get_true_jid(source), parameters.replace(' ','_')

        adr = 'http://ru.wikipedia.org/w/index.php'
        values = {'search' : parameters.encode('utf8','replace'), 'title':'Служебная:Search'}
        data = urllib.urlencode(values)
        #req = urllib2.Request(adr+urllib.quote(parameters.encode('utf8','replace')))
        req = urllib2.Request(adr, data)
        req.add_header('User-Agent','Mozilla/5.0 (Linux; U; Android 2.2.1; sv-se; HTC Wildfire Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1')
        page = urllib2.urlopen(req)
        enc = page.headers.getparam('charset')
        page = page.read()

        page = re.compile(r'<script.*?>.*?</script>',re.DOTALL | re.IGNORECASE).sub('', page)
        page = re.compile(r'<style[^<>]*?>.*?</style>',re.DOTALL | re.IGNORECASE).sub('', page)
        page = re.compile(r'<--.*?-->',re.DOTALL | re.IGNORECASE).sub('', page)
        page = re.findall('<p>(.*)</p>',page)

        page = "\n".join(page)
        page = page.replace('&#160;','')
        h = HTMLParser.HTMLParser()

        page = h.unescape(page.decode(enc, 'replace'))

        try: p = decode_log(page)
        except: p = decode(page)

        p = p.replace('\n\n','')

        if len(p)<100:
            reply(type, source, u'Ничего не найдено!')
            return
        reply(type, source, p)
    except Exception, err:
        reply(type, source, u'Где-то случилась ошибка!')


    

register_command_handler(wiki_q, 'вики', ['все'], 0, 'показывает статью с http://ru.wikipedia.org/wiki/', 'вики слово', ['вики пиво'])

