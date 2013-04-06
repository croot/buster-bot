#!/usr/bin/env python 
# -*- coding: utf8 -*-

#Edit 05.04.13

import random 
import threading 
import time 

RBOT = [u'mafia_bot@jabber.cz/JabberBot', u'mafiozo@worldskynet.net/pybot', u'mafia@oneteam.im/JabberBot','bot@oneteam.im/JabberBot']

MAFIA_REMOTE = {} 

MF_GET_RES = {}

CMD_MNAME = u'.mafia'

MAFIA_MEM = {}

def mafia_leave_handler(*n):
    item = ''
    if len(n)==3:
        item = n[0]
    if hasattr(item, 'realjid') and item.realjid in MAFIA_REMOTE.keys():
        mf_send_iq(MAFIA_REMOTE[item.realjid]['bot'], 'off', 'off', item.realjid, 'public')

bot.register_leave_handler(mafia_leave_handler)

def mf_send_iq(botjid = None, body = None, id = None, jid = None, typ = None, nick = None):
    iq = domish.Element(('jabber:client', 'iq'))
    iq['type'] = 'set'
    iq['id'] = id
    iq['to'] = botjid
    query = iq.addElement('query', 'xmpp:iq:mafia')
    if jid: query['jid'] = jid
    if typ: query['typ'] = typ
    if nick: query['nick'] = nick
    query.addContent(body)
    reactor.callFromThread(bot.wrapper.x.send, iq)
 

def mafia_get_info():
    global RBOT
    if RBOT:
        for x in RBOT:
            mf_send_iq(x, u'info', u'info')

def mafia_url_get_jid():
    time.sleep(1.5) 
    for x in [u'http://mafiozo.in/mafia.txt',u'http://talisman.wen.ru/mafia.txt']:
        try:
            import urllib2 
            req = urllib2.Request(x) 
            r = urllib2.urlopen(req) 
            page = r.read().splitlines() 
            if page:
                for c in page:
                    c=c.strip() 
                    if not c in RBOT and c.count('@'):
                        RBOT.append(c) 
        except: pass 

      
def hnd_mafia(t, s, p):
    global MAFIA_REMOTE 
    global RBOT 
    global MF_GET_RES

    jid = s.realjid 
    nick = s.nick 
    rep = str()
    JOIN = '1234'
      
    if not nick:
        nick = jid.split('@')[0] 
      
    if jid in MAFIA_REMOTE.keys() and not p:
        if 'spec' in MAFIA_REMOTE[jid] and MAFIA_REMOTE[jid]['spec']:
            
            mf_send_iq(MAFIA_REMOTE[jid]['bot'], 'off', 'off', jid, 'public')

            del MAFIA_REMOTE[jid]
            #s.msg(t, u'Ок. Вы вышли из Игры!')
            return
        
    if p.isdigit():

        n = int(p)
        
        if n in MF_GET_RES: 
            private = s.jid
            
            MAFIA_REMOTE[jid] = {'bot':MF_GET_RES[n]['jid'], 'private':private, 'spec':None}
            
            mf_send_iq(MF_GET_RES[n]['jid'], JOIN, str(), jid, 'public', nick)

            return
        
        else:
            s.msg(t, u'Партия с таким номером не найденa!')
            return

    MF_GET_RES.clear() 

    mafia_get_info() 

    tt = time.time() 
      
    while not MF_GET_RES and time.time() - tt<5.5: 
        time.sleep(1) 
        pass

    if not MF_GET_RES:
        s.msg(t, u'Извините, на данный момент сервер недоступен!')
        return

    SP=[]
    cid = []
    for x in MF_GET_RES.keys():
        try:
            if MF_GET_RES[x].get('id',None):
                if MF_GET_RES[x].get('id',None) in cid:
                    continue
                else: cid.append(MF_GET_RES[x].get('id',None))
            if not MF_GET_RES[x]['jid'] in SP:
                SP.append(MF_GET_RES[x]['jid'])
            else:
                continue
            rep+=str(x)+'. '+MF_GET_RES[x]['body']+'\n'
        except:
            pass
      
    s.msg(t, u'Вот че я нашел:\n'+rep+u'\nВыберите номер партии, например:\n '+CMD_MNAME+' 1') 
     
      
def iq_maf(iq):
    global MAFIA_REMOTE
    global RBOT 
    global MF_GET_RES
    global MAFIA_MEM


    try: fromjid = iq['from']
    except: return

    sjid = config.USER+'@'+config.SERVER+'/'+config.RESOURCE

    if fromjid == sjid or not fromjid in RBOT:
        return

    nsuri = iq.firstChildElement().uri
    if nsuri!= 'xmpp:iq:mafia': return


    id = iq.getAttribute('id')

    if iq.getAttribute('type')=='result':
        
        if id in MAFIA_REMOTE and 'spec' in MAFIA_REMOTE[id]:# and MAFIA_REMOTE[id]['bot']==fromjid:
            MAFIA_REMOTE[id]['spec']=1
            return

    if iq.getAttribute('type')=='set':

        fromjid = iq.getAttribute('from')
        try: el = iq.children[0].attributes
        except: return

        try: body = iq.children[0].__dict__['children'][0]#element2dict(iq).get('query',None)#iq.firstChildElement()#(None if not hasattr(el,'children') else el.children)
        except: return
        if not body: return


        try:
            jid = el.get('jid','')
            typ = el.get('typ','')
            nick = el.get('nick', '')
            cityid = el.get('cityid', '')
        except:
            jid = str()
            typ = str()
            nick = str()
            cityid = str()
        try:
            if id == u'info':
                i = len(MF_GET_RES)+1
                MF_GET_RES[i] = {'jid':fromjid,'body':body,'id':cityid}
                return

            if id == u'game_over' or id.count('game_over'):
                for x in MAFIA_REMOTE.keys():
                    if 'private' in MAFIA_REMOTE[x]:
                        body = u'Для повторного входа в игру отправьте 1 или #'
                        bot.muc.msg('chat', MAFIA_REMOTE[x]['private'], body)
                        MAFIA_MEM[x] = MAFIA_REMOTE[x]['bot']
                MAFIA_REMOTE.clear()
                return
            
            if not typ or typ == 'public':
                for x in [c for c in MAFIA_REMOTE.keys() if MAFIA_REMOTE[c].get('bot')==fromjid]:
                    to = MAFIA_REMOTE[x]['private']
                    bot.muc.msg('chat', to, body)
                return

            if jid in MAFIA_REMOTE.keys():
                try:
                    if time.time()-MAFIA_REMOTE_CALC>60:
                        MAFIA_REMOTE_CALC = time.time()
                        write_file('dynamic/mrecovery.txt',str(MAFIA_REMOTE))
                except: pass

                to = MAFIA_REMOTE[jid]['private']
                bot.muc.msg('chat', to, body)
        except: print 'MAFIA exception'


      

def mafia_message(xs):

    global MAFIA_REMOTE
    
    p, jid, t, nick = str(), str(), 'public', str()

    for e in xs.elements():
        if e.name == "body":
            p = e.__str__()

    try:
        if not p or p.split()[0].lower() in [x[1] for x in bot.cmdhandlers]:
            return
    except:
        return
    
    try:
        jid = xs['from'].split('/')[0]
        nick = xs['from'].split('/')[1]
    except: pass

    #print jid

    if jid in bot.g.keys():
        if nick in bot.g[jid].items:
            jid = bot.g[jid].items[nick].realjid
      
    if jid in MAFIA_REMOTE.keys():
        mf_send_iq(MAFIA_REMOTE[jid]['bot'], p, str(random.randrange(0,222)), jid, t)
    else:
        if jid in MAFIA_MEM.keys() and p in [u'1',u'#']:
            if not nick:
                nick = jid.split('@')[0]
            botjid = MAFIA_MEM[jid]
            if not isinstance(botjid, basestring): return
            MAFIA_REMOTE[jid]={'bot':botjid, 'private':xs['from'], 'spec':0}
            mf_send_iq(MAFIA_REMOTE[jid]['bot'], '1234', str(), jid, 'public', nick)
    
      

bot.register_cmd_handler(hnd_mafia, CMD_MNAME) 

mafia_url_get_jid() 

def reg_handler_mafia_iq():
    while not hasattr(bot.wrapper.x,'addObserver'):
        time.sleep(1)
        pass
    time.sleep(1) 
    bot.wrapper.x.addObserver('/iq', iq_maf)
    bot.wrapper.x.addObserver('/message', mafia_message) 

threading.Thread(None, reg_handler_mafia_iq, 'reg_handler_mafia_iq'+str(random.randrange(1,10))).start() 

if not os.path.exists('doc/help/mafia-ru.txt'):
    try:
        fp=open('doc/help/mafia-ru.txt','w') 
        fp.write("""muc  
  Ролевая онлайн игра мафия, играть могут пользователи с разных конференций через приват бота.
  Статья об игре с ресурса wikipedia:
  http://ru.wikipedia.org/wiki/Мафия_(игра) """) 
        fp.close() 
    except: pass
