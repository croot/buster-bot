#===istalismanplugin===
# -*- coding: utf-8 -*-

""" Quiz plugin """

import os.path
import thread
ZAGADKI_FILENAME = 'static/zagadki.txt'
ZAGADKI_SCORES_DIR = 'dynamic/zagadki/'

ZAGADKI_TOTAL_LINES = 3248
ZAGADKI_TIME_LIMIT = 120
ZAGADKI_IDLE_LIMIT = 2

ZAGADKI_RECURSIVE_MAX = 20
ZAGADKI_FILE = {}
ZAGADKI_SCORES = {}
ZAGADKI_CURRENT_ANSWER = {}
ZAGADKI_CURRENT_HINT = {}
ZAGADKI_CURRENT_TIME = {}
ZAGADKI_IDLENESS = {}


def sectomin(time):
        m = 0
        s = 0
        if time >= 60:
                m = time / 60
                
                if (m * 60) != 0:
                        s = time - (m * 60)
                else:
                        s = 0
        else:
                m = 0
                s = time
                

        return str(m)+u'мин. и '+str(s)+u'сек.'

def handler_zagadki_start(type, source, parameters):
    groupchat = source[1]
    if not source[1] in GROUPCHATS:
        reply(type, source, 'Только в конференции.')
        return
    if ZAGADKI_CURRENT_ANSWER.has_key(groupchat):
        reply(type, source, 'Игра уже запущена.')
        return
    ZAGADKI_SCORES[groupchat] = zagadki_load_score_file(groupchat)
    if ZAGADKI_IDLENESS.has_key(groupchat):
        del ZAGADKI_IDLENESS[groupchat]
    msg(source[3],groupchat, 'Загрущаю счёт...\nВнимание, игра в загадки началась. ')
    msg(source[3],groupchat, u'Загрузил')
    zagadki_ask_question(source)

def handler_zagadki_stop(type, source, parameters):
    groupchat = get_groupchat(source)
    if not groupchat:
        reply(type, source, 'Только в конференции.')
        return
    if ZAGADKI_CURRENT_ANSWER.has_key(groupchat):
        del ZAGADKI_CURRENT_ANSWER[groupchat]
        #msg(groupchat, source[2]+u' Игра остановлена.')
        msg(source[3],groupchat, u'Сохраняю счёт...')
        zagadki_save_score_file(groupchat)
        zagadki_list_scores(source)
        msg(source[3],groupchat, u'Сохранил')
        msg(source[3],groupchat, source[2]+u' Игра остановлена.')
    else:
        reply(type, source, u'Игра в загадки не запущена,для запуска напишите .вкл')

def handler_zagadki_hint(type, source, parameters):
    groupchat = source[1]
    if not source[1] in GROUPCHATS:
        reply(type, source, 'Только в конференции.')
        return
    if ZAGADKI_CURRENT_ANSWER.has_key(groupchat):
        if ZAGADKI_IDLENESS.has_key(groupchat):
            del ZAGADKI_IDLENESS[groupchat]
        if ZAGADKI_CURRENT_HINT[groupchat] == None:
            ZAGADKI_CURRENT_HINT[groupchat] = 0
        pol = len(ZAGADKI_CURRENT_ANSWER[groupchat])
#        if pol <4: stroka = u' Буквы.'
#        else: stroka = u' Букв.'
#        msg(groupchat, u'В ответе ' + str(len(ZAGADKI_CURRENT_ANSWER[groupchat])) + stroka)
        ZAGADKI_CURRENT_HINT[groupchat] += 1
        if ZAGADKI_CURRENT_HINT[groupchat] == len(ZAGADKI_CURRENT_ANSWER[groupchat]): # - 1:
            msg(source[3], groupchat, u'Никто не угадал эту загадку. Ответ был: ' + ZAGADKI_CURRENT_ANSWER[groupchat])
            zagadki_ask_question(source)
        curans = ZAGADKI_CURRENT_ANSWER[groupchat]
        curcnt = ZAGADKI_CURRENT_HINT[groupchat]
#        hint = ''.join([curans[i] if i < curcnt or curans[i] == ' ' else '*' for i in xrange(len(curans))])
        hint = ''.join([curans[i] if i < curcnt or curans[i] in (' ','-',',') else '*' for i in xrange(len(curans))])
        msg(source[3],groupchat, u'Подсказка: ' + hint)
    # else:
        # reply(type, source, u'Игра в загадки не запущена,для запуска напишите .вкл')

def handler_zagadki_next_question(type, source, parameters):
    groupchat = source[1]
    if not source[1] in GROUPCHATS:
        reply(type, source, 'Только в конференции.')
        return
    if ZAGADKI_CURRENT_ANSWER.has_key(groupchat):
        msg(source[3],groupchat, u'Правильный ответ: ' + ZAGADKI_CURRENT_ANSWER[groupchat])
        zagadki_ask_question(source)
    else:
        reply(type, source, u'Игра в загадки не запущена,для запуска напишите .вкл')

def get_groupchat(jid):
    if type(jid) is types.ListType:
        jid = jid[1]
    jid = string.split(unicode(jid), '/')[0] # str(jid)
    if GROUPCHATS.has_key(jid):
        return jid
    else:
        return None

def zagadki_save_score_file(groupchat):
   """ Saving current scores to the score file """
   global ZAGADKI_SCORES, ZAGADKI_SCORES_DIR

   filename = os.path.join( ZAGADKI_SCORES_DIR, groupchat+'.score'  )
   initialize_file(filename)

   write_file(filename, str(ZAGADKI_SCORES[groupchat]))

def zagadki_load_score_file(groupchat):
   """ Loading a score file for the current groupchat """
   global ZAGADKI_SCORES, ZAGADKI_SCORES_DIR

   filename = os.path.join( ZAGADKI_SCORES_DIR, groupchat+'.score' )
   initialize_file(filename, '{}')

   return eval(read_file(filename))

def zagadki_save_score_file_glob(groupchat):
   """ Saving current scores to the score file """
   global ZAGADKI_SCORES, ZAGADKI_SCORES_DIR

   filename = os.path.join( ZAGADKI_SCORES_DIR, 'glob.score'  )
   initialize_file(filename)

   write_file(filename, str(ZAGADKI_SCORES[groupchat]))   

def zagadki_load_score_file_glob(groupchat):
   """ Loading a score file for the current groupchat """
   global ZAGADKI_SCORES, ZAGADKI_SCORES_DIR

   filename = os.path.join( ZAGADKI_SCORES_DIR, 'glob.score' )
   initialize_file(filename, '{}')

   return eval(read_file(filename))

def zagadki_timer(s, groupchat, start_time):
        time.sleep(ZAGADKI_TIME_LIMIT)
        if ZAGADKI_CURRENT_TIME.has_key(groupchat) and \
            ZAGADKI_CURRENT_ANSWER.has_key(groupchat) and \
            start_time == ZAGADKI_CURRENT_TIME[groupchat]:
#            msg(groupchat, u'Время вышло! Прошло ' + str(ZAGADKI_TIME_LIMIT) + \
#                u' секунд. Правильный ответ: ' + ZAGADKI_CURRENT_ANSWER[groupchat])
            msg(s[3], groupchat, u'и так... время вышло! Прошло: ' + sectomin(ZAGADKI_TIME_LIMIT) + u'Правильный ответ: ' + ZAGADKI_CURRENT_ANSWER[groupchat])
            if ZAGADKI_IDLENESS.has_key(groupchat):
                ZAGADKI_IDLENESS[groupchat] += 1
            else:
                ZAGADKI_IDLENESS[groupchat] = 1
            if ZAGADKI_IDLENESS[groupchat] >= ZAGADKI_IDLE_LIMIT:
                msg(s[3], groupchat, u'Прошло 2 минуты и игра в загадки автоматически завершилась из-за бездействия,чтобы её запустить, напишите .вкл ')
                del ZAGADKI_CURRENT_ANSWER[groupchat]
                msg(s[3], groupchat, u'Сохраняю счёт...')
                zagadki_save_score_file(groupchat)
                zagadki_list_scores(s)
                msg(s[3], groupchat, u'Сохранил')
            else:
                zagadki_ask_question(s)

def zagadki_ask_question(s):
    global question
    groupchat = s[1]
    (question, answer) = zagadki_new_question()
    ZAGADKI_CURRENT_ANSWER[groupchat] = answer
    ZAGADKI_CURRENT_HINT[groupchat] = None
    ZAGADKI_CURRENT_TIME[groupchat] = time.time()
    #thread.start_new(zagadki_timer, (s, groupchat, ZAGADKI_CURRENT_TIME[groupchat]))
    threading.Thread(None,zagadki_timer,'zagadki_timer'+str(INFO['thr']),(s, groupchat, ZAGADKI_CURRENT_TIME[groupchat],)).start()
    pol = len(ZAGADKI_CURRENT_ANSWER[groupchat])
    if pol <4: stroka = u' Буквы.'
    else: stroka = u' Букв.'
    msg(s[3],groupchat, u'Загадка №' + question + '\n' +u'В ответе ' + str(len(ZAGADKI_CURRENT_ANSWER[groupchat])) + stroka)

def zagadki_answer_question(source, answer):
    if ZAGADKI_CURRENT_ANSWER.has_key(source[1]):
        answer1 = ZAGADKI_CURRENT_ANSWER[source[1]].lower()
        answer2 = answer.lower()
        if answer1 == answer2:
#        if ZAGADKI_CURRENT_ANSWER[groupchat] == answer:
            if ZAGADKI_IDLENESS.has_key(source[1]):
                del ZAGADKI_IDLENESS[source[1]]
            answer_time = int(time.time() - ZAGADKI_CURRENT_TIME[source[1]])
            points = ZAGADKI_TIME_LIMIT / answer_time / 3 + 1
            vremya = sectomin(int(time.time() - ZAGADKI_CURRENT_TIME[source[1]]))
            
            if not ZAGADKI_SCORES.has_key(source[1]):
                ZAGADKI_SCORES[source[1]] = {}
            if ZAGADKI_SCORES[source[1]].has_key(source[2]):
                ZAGADKI_SCORES[source[1]][source[2]] += points
            else:
                ZAGADKI_SCORES[source[1]][source[2]] = points
            
            your_points = ZAGADKI_SCORES[source[1]][source[2]]
            place = 1 + len(filter(lambda x: x > your_points, ZAGADKI_SCORES[source[1]].values()))
#            msg(groupchat, u'%s получает +%d баллов, и занимает %d место! Правильный ответ: %s' %\
            msg(source[3], source[1], u'%s получает +%d баллов, и занимает %d место! \nПравильный ответ был дан за %s И ответ был: %s' %\
                (source[2], points, place, vremya, answer))
            
            zagadki_ask_question(source)
       
def zagadki_list_scores(s):
    if ZAGADKI_SCORES.has_key(s[1]):
        if ZAGADKI_SCORES[s[1]]:
            if ZAGADKI_IDLENESS.has_key(s[1]):
                del ZAGADKI_IDLENESS[s[1]]
            result = []
            for nick in ZAGADKI_SCORES[s[1]]:
                result.append((ZAGADKI_SCORES[s[1]][nick], nick))
            result.sort()
            result.reverse() 
#            msg(groupchat, u'Текущий счёт '+groupchat+ u':\n' + \
#                u'\n'.join([u"%d) %s: %d баллов" % (i+1,  result[i][1], result[i][0]) \
#                for i in xrange(len(result))][:10]))
            msg(s[3], s[1], u'Текущий счёт этой конференции'+ u':\n' + \
                u'\n'.join([u"%d) %s: %d баллов" % (i+1,  result[i][1], result[i][0]) \
                for i in xrange(len(result))][:10]))

def zagadki_me_list_scores(groupchat):
        if ZAGADKI_SCORES.has_key(groupchat):
                if ZAGADKI_SCORES[groupchat]:
                        if ZAGADKI_IDLENESS.has_key(groupchat):
                                del ZAGADKI_IDLENESS[groupchat]
                        result = []
                        for nick in ZAGADKI_SCORES[groupchat]:
                                result.append((ZAGADKI_SCORES[groupchat][nick], nick))
                        result.sort()
                        result.reverse()
                        your_points = ZAGADKI_SCORES[groupchat][nick]
                        source = nick
                        place = 1 + len(filter(lambda x: x > your_points, ZAGADKI_SCORES[groupchat].values()))
                        msg(groupchat, u'%s занимает %d место! Заработав %d очков' % (your_points, place))
#            msg(groupchat, u'Текущий счёт '+groupchat+ u':\n' + \
#                u'\n'.join([u"%d) %s: %d баллов" % (i+1,  result[i][1], result[i][0]) \
#                for i in xrange(len(result))][:1]))

def zagadki_new_question():
    global ZAGADKI_RECURSIVE_MAX
    line_num = random.randrange(3248)
    fp = file(ZAGADKI_FILENAME)
    for n in range(line_num + 1):
        if n == line_num:
            try:
                (question, answer) = string.split(fp.readline().strip(), '|', 1)
                return (unicode(question,"UTF-8"), unicode(answer,"UTF-8"))
            except:
                ZAGADKI_RECURSIVE_MAX -= 1
                if ZAGADKI_RECURSIVE_MAX:
                    return zagadki_new_question()
                else:
                    ZAGADKI_RECURSIVE_MAX = 20
                    return ('Parsing Error: Line ' + str(n), '')

        else:
            fp.readline()
""" Loading a score file for the current groupchat """
#global ZAGADKI_SCORES, ZAGADKI_SCORES_DIR

filename = os.path.join( ZAGADKI_SCORES_DIR, '.score' )
initialize_file(filename, '{}')

#return eval(read_file(filename))

def handler_zagadki_message(raw, type, source, body):
    groupchat = get_groupchat(source)
    if groupchat and ZAGADKI_CURRENT_ANSWER.has_key(groupchat):
        zagadki_answer_question(source, body.strip())
"""
def handler_zagadki_restart(type, source, parameters):
    handler_zagadki_stop(type, source, parameters)
    time.sleep(1.3)
    handler_zagadki_start(type, source, parameters)
"""

def handler_zagadki_restart(type, source, parameters):
    groupchat = source[1]
    s = source
    if not s[1] in GROUPCHATS:
        reply(type, source, 'Только в конференции.')
        return
    if ZAGADKI_CURRENT_ANSWER.has_key(groupchat):
        del ZAGADKI_CURRENT_ANSWER[groupchat]
        msg(s[3], groupchat, u'Внимание, перазавкл игры.')
        zagadki_save_score_file(groupchat)
        zagadki_list_scores(source)
    else:
        reply(type, source, u'Перезапускаю игру')
    time.sleep(1.3)
    if not groupchat:
        reply(type, source, 'Not in groupchat.')
        return
    if ZAGADKI_CURRENT_ANSWER.has_key(groupchat):
        reply(type, source, 'Игра уже запущена.')
        return
    ZAGADKI_SCORES[groupchat] = zagadki_load_score_file(groupchat)
    if ZAGADKI_IDLENESS.has_key(groupchat):
        del ZAGADKI_IDLENESS[groupchat]
    msg(s[3], groupchat, 'Загрущаю счёт...\nВнимание, игра в загадки началась. ')
    zagadki_ask_question(s)

def handler_zagadki_otvet(type, source, parameters):
    groupchat = get_groupchat(source)
    if not groupchat:
        reply(type, source, 'Только в конференции.')
        return
    if ZAGADKI_CURRENT_ANSWER.has_key(groupchat):
        msg(source[3], groupchat, u'Правильный ответ: ' + ZAGADKI_CURRENT_ANSWER[groupchat])
    else:
        reply(type, source, u'Игра в загадки не запущена, для запуска напишите .вкл')


def handler_zagadki_scores(type, source, parameters):
    groupchat = get_groupchat(source)
    if not groupchat:
        reply(type, source, 'Только в конференции.')
        return
    
    if not ZAGADKI_SCORES.has_key(groupchat):
        ZAGADKI_SCORES[groupchat] = zagadki_load_score_file(groupchat)
    
    zagadki_list_scores(source)

def handler_zagadki_me_scores(type, source, parameters):
    groupchat = get_groupchat(source)
    if not groupchat:
        reply(type, source, 'Только в конференции.')
        return
    
    if not ZAGADKI_SCORES.has_key(groupchat):
        ZAGADKI_SCORES[groupchat] = zagadki_load_score_file(groupchat)
    
    zagadki_me_list_scores(source)

def handler_zagadki_povtori(type, source, parameters):
    global question 
    groupchat = get_groupchat(source)
    if not groupchat:
        reply(type, source, 'Только в конференции.')
        return
    if ZAGADKI_CURRENT_ANSWER.has_key(groupchat):
        reply(type, source, u'Повторяю загадку специально для тебя.\nЗагадка под номером '+question)
    else:
        reply(type, source, u'Игра в загадки не запущена, для запуска напишите .вкл')

def handler_zagadki_help(type, source, body):
        if ZAGADKI_CURRENT_ANSWER.has_key(source[1]):
                stat = u'запущена'
        else:
                stat = u'не запущена'
        res = u'\nИгра в загадки v2.1\n(с) Grand_Dizel\nИгра сейчас: '+stat+u'\nВ базе данных: '+str(ZAGADKI_TOTAL_LINES)+u' загадок\nКоманды...\nНе забудь перед командой написать префикс. Основние команды:\n-   .вкл - завкл игры\n-   .выкл - остановка игры\n-   .повтори - повторяет вопрос\n-   .п - вывод подсказки (снимает баллы)\n-   .сл - следущий вопрос\n-   .топ - вывод текущего счета\n-   .перезапусти - перезапускает игру\n-   .о - показывает правильный ответ на текущую загадку, доступно только владельцу бота'
        reply(type, source, res)

#register_command_handler(handler_zagadki_start, 'on', ['загадки','развлечения','Grand_Dizel','все'], 0, ' Завклает игру загадки', 'on', ['on'])
#register_command_handler(handler_zagadki_stop, 'off', ['загадки','развлечения','Grand_Dizel','все'], 0, ' Выключает игру загадки', 'off', ['off'])

#register_command_handler(handler_zagadki_start, 'он', ['загадки','развлечения','Grand_Dizel','все'], 0, ' Завклает игру загадки', 'он', ['он'])
#register_command_handler(handler_zagadki_stop, 'офф', ['загадки','развлечения','Grand_Dizel','все'], 0, ' Выключает игру загадки', 'офф', ['офф'])

#register_command_handler(handler_zagadki_start, 'пуск', ['загадки','развлечения','Grand_Dizel','все'], 0, ' Завклает игру загадки', 'пуск', ['пуск'])
#register_command_handler(handler_zagadki_stop, 'отмена', ['загадки','развлечения','Grand_Dizel','все'], 0, ' Выключает игру загадки', 'отмена', ['отмена'])

register_command_handler(handler_zagadki_help, '.загадки', ['загадки','развлечения','все'], 0, 'Вывод инструкции.', 'загадки', ['загадки'])
register_command_handler(handler_zagadki_start, '.вкл', ['загадки','развлечения','все'], 0, ' Завклает игру загадки', 'вкл', ['вкл'])
register_command_handler(handler_zagadki_restart, '.перезапусти', ['загадки','развлечения', 'все'], 100, ' Перезапускает игру в загадки, доступно только админу бота', 'перезапусти', ['перезапусти'])
register_command_handler(handler_zagadki_povtori, '.повтори', ['загадки','развлечения','все'], 0, ' Повторяет вопрос', 'п', ['п'])
register_command_handler(handler_zagadki_otvet, '.о', ['загадки','развлечения','все'], 100, ' Показывает правильный ответ на текущую загадку, доступно только владельцу бота', '.о', ['.о'])
register_command_handler(handler_zagadki_stop, '.выкл', ['загадки','развлечения','все'], 0, ' Выключает игру загадки', 'выкл', ['выкл'])
register_command_handler(handler_zagadki_hint, '.п', ['загадки','развлечения','все'], 0, ' Показывает подсказку', '.', ['.'])
register_command_handler(handler_zagadki_next_question, '.сл', ['загадки','развлечения','все'], 0, ' Следующая загадка', 'сл', ['сл'])
register_command_handler(handler_zagadki_scores, '.топ', ['загадки','развлечения','все'], 0, ' Выводит результаты игры в загадки независимо запущена ли игра', 'топ', ['топ'])
#register_command_handler(handler_zagadki_me_scores, 'мойтоп', ['загадки','развлечения','Grand_Dizel','все'], 0, ' Выводит ваш личный результат', 'мойтоп', ['мойтоп'])
register_message_handler(handler_zagadki_message)
