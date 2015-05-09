#===istalismanplugin===
# -*- coding: utf-8 -*-

import HTMLParser
from copy import deepcopy

WIKI = {}

KJ = ''

def wiki_msg(raw, type, source, p):
    global WIKI
    jid = get_true_jid(source)
    if jid in WIKI and p.isdigit():
        if len(WIKI[jid])>=int(p):
            wiki_q(type, source, WIKI[jid][int(p)-1][0])
            

register_message_handler(wiki_msg)

def wiki_q(type, source, parameters):
    global WIKI
    jid = get_true_jid(source)
    if jid in WIKI:
        del WIKI[jid]
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
        c = page
        page = re.findall('<p>(.*)</p>',page)

        page = "\n".join(page)
        page = page.replace('&#160;','')
        h = HTMLParser.HTMLParser()

        page = h.unescape(page.decode(enc, 'replace'))
        c = h.unescape(c.decode(enc, 'replace'))

        try: p = decode_log(page)
        except: p = decode(page)

        p = p.replace('\n\n','')

        global KJ

        KJ = c

        if len(p)<100:
            zz = re.findall('<li>.*?<a href=\"/wiki/.*?\" title=\"(.*?)\">.*?</a>(.*?)</li>', c, re.DOTALL | re.IGNORECASE)
            if not zz or len(zz)==1:
                reply(type, source, u'Ничего не найдено!')
                return
            zz = zz[1:]
            WIKI[jid]=zz
            rep = u'Выберите из списка:\n'
            for x in zz:
                rep+=str(zz.index(x)+1)+') '+x[0]+x[1]+'\n'
            try: rep = decode_log(rep)
            except: rep = decode(rep)
            reply(type, source, rep)
            return
        reply(type, source, p)
    except Exception, err:
        reply(type, source, u'Где-то случилась ошибка!')


    

register_command_handler(wiki_q, 'вики', ['все'], 0, 'показывает статью с http://ru.wikipedia.org/wiki/', 'вики слово', ['вики пиво'])

