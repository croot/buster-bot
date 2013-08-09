#!/usr/bin/env python
# -*- coding: utf-8 -*-

RECALL_FILE = 'dynamic/recall.txt'

db_file(RECALL_FILE, dict)

GLOB_RECALL = {}

RECALL_THREAD = 0

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
                         try: msg(x.split()[1],x.split()[0],u'Напоминание:\n'+GLOB_RECALL[x][c])
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
     try:
          z = time.mktime(datetime.datetime.strptime(p, "%d/%m/%Y %H:%M").timetuple())
          t = time.time()
     except:
          reply(tt, s, u'Неверно указано время! Пример: напомни 09/08/2013 20:30 Смотреть телепузики')
          return
     if z<=t:
          reply(tt, s, u'Чо?')
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
     reply(tt, s, u'Сейчас '+str(datetime.datetime.fromtimestamp(time.time()))[:-7]+u', напоминание сработает через '+timeElapsed(z-t))
     recall_thread()

def recall_init(*n):
     global GLOB_RECALL
     if not GLOB_RECALL:
          GLOB_RECALL=eval(read_file(RECALL_FILE))
     recall_thread()

register_stage0_init(recall_init)
register_command_handler(recall_set, 'напомни', ['все'], 0, 'Устанавливает напоминание, которое в заданное время прийдет на ваш JID. Убедитесь, что бот есть у вас в ростере!', 'напомни <день/месяц/год часы:минуты> [текст]', ['напомни 12/12/2014 12:00 Новый год йопта!'])
