#!/usr/bin/env python
# -*- coding: utf-8 -*-

RECALL_FILE = 'dynamic/recall.txt'

db_file(RECALL_FILE, dict)

GLOB_RECALL = {}

RECALL_THREAD = 0
RECALL_IQ = {}

def recall_get_time(t, s, p):
     jid = s[1]+'/'+s[2]
     packet = IQ(CLIENTS[s[3]], 'get')
     packet.addElement('time', 'urn:xmpp:time')
     packet.addCallback(recall_result, t, s, p)
     reactor.callFromThread(packet.send, jid)

def recall_result(t, s, p, x):
        tzo, utc, dt2 = '','',0

        
        if x['type']=='error':
            RECALL_IQ[s[1]+'/'+s[2]]=False
            return
        
        fmt = '%Y-%m-%d %H:%M:%S'

        try:
            tzo = getTag(x.children[0],'tzo')
            utc = getTag(x.children[0],'utc')
        except:
            query = element2dict(x)['time']
            tzo = element2dict(query)['tzo']
            utc = element2dict(query)['utc']

        tzo, utc = tzo.children[0], utc.children[0]
        utc = utc.replace('T',' ').replace('Z','')
        if utc.count('.'): utc = utc.split('.')[0]
        ss = tzo[1:].split(':')
        h = int(ss[0])
        m = int(ss[1])
        
        if tzo[:1] in ['-']:
            try: dt2 = datetime.datetime(*time.strptime(utc, fmt)[:6])-datetime.timedelta(hours=h, minutes=m)
            except: dt2 = 0
        if tzo[:1] in ['+']:
            try: dt2 = datetime.datetime(*time.strptime(utc, fmt)[:6])+datetime.timedelta(hours=h, minutes=m)
            except: dt2 = 0
        try:
             z = time.mktime(datetime.datetime.strptime(str(dt2), "%Y-%m-%d %H:%M:%S").timetuple())
             RECALL_IQ[s[1]+'/'+s[2]]=z
        except:
             RECALL_IQ[s[1]+'/'+s[2]]=False

def recall_thread():
     global RECALL_THREAD
     if not RECALL_THREAD:
          RECALL_THREAD = 1
     else:
          return
     while GLOB_RECALL:
          time.sleep(60)
          for x in GLOB_RECALL.keys():
               for c in GLOB_RECALL[x].keys():
                    if time.time() >= c:
                         try:
                              jid = x.split()[0]
                              text = u'Напоминание '+(u'' if time.time()-c<300 else u'(запоздало на '+timeElapsed(time.time()-c)+')')+':\n'+GLOB_RECALL[x][c]
                              for ch in [r for r in GROUPCHATS.keys() if [m for m in GROUPCHATS[r] if GROUPCHATS[r][m]['ishere'] and GROUPCHATS[r][m]['jid'].split('/')[0]==jid]]:
                                   for us in GROUPCHATS[ch]:
                                        if GROUPCHATS[ch][us]['ishere'] and GROUPCHATS[ch][us]['jid'].split('/')[0]==jid:
                                             msg(GROUPCHATS[ch][get_bot_nick(ch)]['jid'].split('/')[0], ch, us+', '+text)
                              msg(x.split()[1], jid, text)
                         except: pass
                         try:
                              del GLOB_RECALL[x][c]
                              if not GLOB_RECALL[x]:
                                   del GLOB_RECALL[x]
                              write_file(RECALL_FILE, str(GLOB_RECALL))
                         except: pass
     RECALL_THREAD = 0

def recall_set(tt, s, p):
     global GLOB_RECALL
     global RECALL_FILE
     global RECALL_THREAD
     jid = get_true_jid(s)+' '+s[3]
     rep = str()
     lt = [str(x) for x in time.localtime()]; lt.reverse()
     if not p:
          if jid in GLOB_RECALL:
               for x in GLOB_RECALL[jid]:
                    rep+=str(datetime.datetime.fromtimestamp(x))+u' : '+GLOB_RECALL[jid][x]+'\n'
          reply(tt, s, rep)
          return
     if p.count(' ')<2:
          reply(tt, s, u'Читай помощь по команде!')
          return
     try:
          body = ' '.join(p.split()[2:])
          p = ' '.join(p.split()[:2])
     except:
          reply(tt, s, u'Ты спалил мне процессор!')
          return
     recall_get_time(tt, s, p)
     t1,t2, t = time.time(), 1, time.time()
     while not s[1]+'/'+s[2] in RECALL_IQ and time.time()-t1<3.5:
          time.sleep(1)
          pass
     if not s[1]+'/'+s[2] in RECALL_IQ or RECALL_IQ[s[1]+'/'+s[2]]==False:
          reply(tt, s, u'Время клиента не получено, будет использовано время сервера')
     else:
          t2 = RECALL_IQ[s[1]+'/'+s[2]]
          del RECALL_IQ[s[1]+'/'+s[2]]
          lt = [str(x) for x in time.localtime(t2)]; lt.reverse()
          t = t2
     if p.count(u'сегодня'):
          p=p.replace(u'сегодня', '/'.join(lt[-3:]))
     if p.count(u'завтра'):
          d = datetime.date.today() + datetime.timedelta(days=1)
          p=p.replace(u'завтра', '/'.join([str(d.day),str(d.month),str(d.year)]))
     try:
          z = time.mktime(datetime.datetime.strptime(p, "%d/%m/%Y %H:%M").timetuple())
          
     except:
          reply(tt, s, u'Неверно указано время! Пример: напомни 09/08/2013 20:30 Смотреть телепузики')
          return
     if z<=t:
          reply(tt, s, u'Указанное время меньше реального времени!')
          return
     if z-t<120:
          reply(tt, s, u'Меньше двух минут низзя!')
          return
     if z-t>2629743.83:
          reply(tt, s, u'Насяльника я за месяц и забуду!')
          return
     if not jid in GLOB_RECALL:
          GLOB_RECALL[jid]={}
     if len(GLOB_RECALL[jid])>10:
          reply(tt, s, u'У вас уже более десяти напоминаний!')
          return
     GLOB_RECALL[jid][z]=body
     try: write_file(RECALL_FILE, str(GLOB_RECALL))
     except: pass
     reply(tt, s, u'Сейчас '+time.ctime(t2)+u', напоминание сработает через '+timeElapsed(z-t))
     recall_thread()

def recall_init(*n):
     global GLOB_RECALL
     if not GLOB_RECALL:
          GLOB_RECALL=eval(read_file(RECALL_FILE))
     recall_thread()

register_stage0_init(recall_init)
register_command_handler(recall_set, 'напомни', ['все'], 0, 'Устанавливает напоминание, которое в заданное время прийдет на ваш JID. Убедитесь, что бот есть у вас в ростере!', 'напомни <день/месяц/год часы:минуты> [текст]', ['напомни 12/12/2014 12:00 Новый год йопта!','напомни завтра 5:30 Смотреть телепузики','напомни сегодня 10:20 Сделать пук'])
