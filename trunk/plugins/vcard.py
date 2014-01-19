# -*- coding: utf8 -*-

#get from http://cvs.berlios.de/svnroot/repos/freq-dev/trunk/
#Copyright (c) 2008 Burdakov Daniel <kreved@kreved.org>

def vcard_handler(t, s, p):
    jid=get_true_jid(s[1]+'/'+s[2])
    if p:
        if s[1] in GROUPCHATS and p in GROUPCHATS[s[1]]:
            jid=get_true_jid(s[1]+'/'+p)
        else:
            jid=p
    r=u'FN,BDAY,DESC,URL'
    packet = IQ(CLIENTS[s[3]], 'get')
    packet.addElement('vCard', 'vcard-temp')
    packet.addCallback(vcard_result_handler, t, s, p, r)
    reactor.callFromThread(packet.send, jid)

def vcard_result_handler(t, s, p, r, x):
    if x['type'] == 'result':
        try: vcard = parse_vcard(element2dict(x)['vCard'])
        except KeyError:
            reply(t, s, u'Ошибка парсинга vCard!')
            return
        for i in vcard.keys():
            q = i.split('/')
            q = [j for j in q if j in r]
            if (not q and not('*' in r)) or i.count('BINVAL'): vcard.pop(i)
        res = [u'%s: %s' % (vcard_describe(i, 'ru'), vcard[i]) for i in vcard.keys() if vcard[i].strip()]
        if res: reply(t, s, 'vCard:\n' + '\n'.join(res))
        else: reply(t, s, u'vCard не заполнен!')
    else:
        reply(t, s, u'Его клиент не поддерживает vCard!')

VCARD_FIELDS = {
'ru::vCard/FN'          : u'Полное имя', 
'ru::vCard/URL'         : u'Сайт',
'ru::vCard/BDAY'        : u'День рождения',
'ru::vCard/DESC'        : u'О себе',
'ru::vCard/PHOTO/TYPE'  : u'Фото',
'ru::vCard/ORG/ORGNAME' : u'Организация',
'ru::vCard/TITLE'       : u'Роль',
'ru::vCard/ADR/CTRY'    : u'Государство',
'ru::vCard/EMAIL/USERID': u'Мыло',
'ru::vCard/NICKNAME'    : u'Ник',
'ru::vCard/TEL/NUMBER'  : u'Телефон',
'ru::vCard/ADR/REGION'  : u'Регион',
'ru::vCard/ADR/LOCALITY': u'Город'}

def vcard_describe(field, lang):
 field = field[:len(field)-1]
 m = lang + '::' + field
 if m in VCARD_FIELDS.keys(): return VCARD_FIELDS[m]
 else: return field

def parse_vcard(x):
 r = {}
 if type(x) == domish.Element:
  for i in x.children:
   q = parse_vcard(i)
   for j in q.keys():
    r['%s/%s' % (x.name, j)] = q[j]
 else: r[''] = x
 return r

from twisted.words.xish import domish
def element2dict(element, p=0):
 r = {}
 for i in element.children:
  if i.__class__ == domish.Element:
   r[i.name] = i
  else:
   if p: r[''] = i
 return r


register_command_handler(vcard_handler, 'визитка', ['мук','инфо','все'], 0, 'Показывает vCard указанного пользователя.', 'визитка [ник]', ['визитка guy','визитка'])

import base64

def hnd_vcard_edit(t, s, p):
    file = 'dynamic/vcard.txt'
    db_file(file, dict)
    db = eval(read_file(file))
    VC = {'DESC':u'Комментарии(о себе)','ORGNAME':u'Организация','NICKNAME':u'Ник','TITLE':u'Род занятий','URL':u'Сайт'}
    
    if not p:
        if db:
            logo = ''
            if os.path.exists('vc.jpg') and os.path.getsize('vc.jpg')<=60000:
                logo+= u'Ава: vc.jpg ('+byteString(os.path.getsize('vc.jpg'))+')\n'
            reply(t, s, u'Информация из базы:\n'+logo+'\n'.join([VC[x]+': '+db[x] for x in db.keys()]))
        return
    if p.lower() == u'update':
        if not db:
            reply(t, s, u'База пуста')
            return
        vcard_set_(db)
        reply(t, s, u'ok')
        return
    if not p.count(' '):
        return
    if not p.split()[0].upper() in VC.keys():
        reply(t, s, u'Доступны ключи '+', '.join(VC.keys()))
        return
    db[p.split()[0].upper()] = ' '.join(p.split()[1:])
    write_file(file, str(db))
    reply(t, s, u'Сохранено. Чтобы изменения вступили в силу наберите botvc update')

register_command_handler(hnd_vcard_edit, 'botvc', ['все'], 100, 'Редактор визитки бота глобально на всех активных jid-ах. Доступны ключи для редактирования: DESC, URL, NICKNAME, TITLE, ORGNAME. Без параметров отобразит изменения в базе.', 'botvc <key> <text>', ['botvc nickname buster+'])

def vcard_set_(dict):
    FIRST = {'ORGNAME':'ORG'}
    for x in CLIENTS.keys():
        iq = IQ(CLIENTS[x], 'set')
        vcard = iq.addElement('vCard', 'vcard-temp')
        if os.path.exists('vc.jpg') and os.path.getsize('vc.jpg')<=60000:
            img = base64.encodestring(open("vc.jpg","rb").read())
            photo = vcard.addElement('PHOTO')
            photo.addElement('BINVAL', content = img)
            photo.addElement('TYPE', content = 'image/jpeg')
        for c in dict:
            if c in FIRST.keys():
                el = vcard.addElement(FIRST[c])
                el.addElement(c, content = dict[c])
            else:
                el = vcard.addElement(c, content = dict[c])
        reactor.callFromThread(iq.send, x)


