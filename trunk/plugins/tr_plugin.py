#===istalismanplugin===
# -*- coding: utf-8 -*-

#TR_EN = {u'sch':u'щ', u'yu':u'ю', u'yi':u'ы', u'ch':u'ч', u'zh':u'ж', u'ya':u'я', u'sh':u'ш', u'c':u'ц', u'a':u'а', u'b':u'б', u'v':u'в', u'g':u'г', u'd':u'д', u'e':u'е', u'z':u'з', u'i':u'и', u'j':u'й', u'k':'к', u'l':u'л', u'm':u'м', u'n':u'н', u'o':u'о', u'p':u'п', u'r':u'р', u's':u'с', u't':u'т', u'u':u'у', u'f':u'ф', u'h':u'х', u'\'':u'ь'}

TR_EN = ((u'sch',u'щ'),
         (u'yu',u'ю'),
         (u'yi',u'ы'),
         (u'ch',u'ч'),
         (u'zh',u'ж'),
         (u'ya',u'я'),
         (u'sh',u'ш'),
         (u'c',u'ц'),
         (u'a',u'а'),
         (u'b',u'б'),
         (u'v',u'в'),
         (u'g',u'г'),
         (u'd',u'д'),
         (u'e',u'е'),
         (u'z',u'з'),
         (u'i',u'и'),
         (u'j',u'й'),
         (u'k',u'к'),
         (u'l',u'л'),
         (u'm',u'м'),
         (u'n',u'н'),
         (u'o',u'о'),
         (u'p',u'п'),
         (u'r',u'р'),
         (u's',u'с'),
         (u't',u'т'),
         (u'u',u'у'),
         (u'f',u'ф'),
         (u'h',u'х'),
         (u'\'',u'ь'))

def translit_to_kiril(t, s, p):
    if not p: return
    ru = 0
    for x in p:
        if ord(x)>127:
            ru=1
            break
    if ru: return
    for c,b in TR_EN:
        try:
            p=p.replace(c, b)
        except: pass
    reply(t, s, p)

def kiril_to_translit(t, s, p):
    if not p: return
    ru = 0
    #for x in p:
    #    if ord(x)>127:
    #        ru=1
    #        break
    #if ru: return
    for c,b in TR_EN:
        try:
            p=p.replace(b, c)
        except: pass
    reply(t, s, p)

def translit_msg(raw, type, source, parameters):
    ru=0
    rep=''
    if source[2]==get_bot_nick(source[1]):
        return
    if parameters.lower() in COMMANDS:
        return
    if len(parameters.split())>1:
        s=parameters.split()[0]
        if s.lower() in COMMANDS:
            return
        z=s.replace(',','').replace(':','')
        if source[1] in GROUPCHATS and z in GROUPCHATS[source[1]]:
            if not z.count(get_bot_nick(source[1])):
                return
            parameters=parameters.replace(s,'')
            parameters=parameters.strip()
    parameters=parameters.lower()
    for x in parameters:
        if ord(x)>127:
            ru=1
            break
    if ru: return
    for c,b in TR_EN:
        try:
            parameters=parameters.replace(c, b)
        except: pass
    cmd=parameters.lower()
    pr=''
    if len(parameters.split())>1:
        args=parameters.split()
        cmd=parameters.split()[0]
        cmd=cmd.lower()
        pr=' '.join(args[1:])
    if COMMAND_HANDLERS.has_key(cmd):
        if source[1] in COMMOFF and cmd in COMMOFF[source[1]]:
            return
        call_command_handlers(cmd, type, source, pr)
    #else:
    #    msg(source[1], parameters)

def translit_table(t, s, p):
    z = ''
    for x in TR_EN: z+=x[0]+' - '+x[1]+'\n'
    reply(t, s, z)

def from_translit_eng(t, s, p):
    p = p.lower()
    for c,b in TR_EN:
        try: p = p.replace(c, b)
        except: pass
    if not 'gAutoTrans' in globals().keys():
        reply(t, s, u'Функция автоперевода не найдена! (gAutoTrans)')
        return
    gAutoTrans(t, s, p)

register_message_handler(translit_msg)#translit_to_kiril
register_command_handler(translit_to_kiril, 'detranslit', ['все','сервисы'], 0, 'Переводит транслит в кириллицу', 'detranslit <text>', ['detranslit puk'])
register_command_handler(kiril_to_translit, 'translit', ['все','сервисы'], 0, 'Переводит кириллицу в транслит', 'translit <text>', ['translit пук'])
register_command_handler(translit_table, 'tr_table', ['все','сервисы'], 0, 'Таблица транслита', 'tr_table', ['tr_table'])
register_command_handler(from_translit_eng, 'tr', ['все','сервисы'], 0, 'Перевод с транслита в англ.', 'tr <text>', ['tr privet'])

