#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  admin_plugin.py

# Gigabyte
# www: http://jabbrik.ru - новые плагины, разработки и прочее!

##############################################################
## Настройка плагина #########################################
QUIZ_FILE = 'static/questions.txt' # путь к БД ###############
QUIZ_TOTAL_LINES = 33693 # количество вопросов в БД ##########
QUIZ_TIME_LIMIT = 200 # таймаут в секундах ###################
QUIZ_IDLE_LIMIT = 3 # количество таймаутов до OFF ############
##############################################################
QUIZ_RECURSIVE_MAX = 20 # empty ##############################
QUIZ_CURRENT_ANSWER = {} #####################################
QUIZ_CURRENT_HINT = {} #######################################
QUIZ_CURRENT_HINT_NEW = {} ###################################
QUIZ_CURRENT_TIME = {} #######################################
QUIZ_IDLENESS = {} ###########################################
QUIZ_IDLE_ANSWER = {}
QUIZ_START = {}
QUIZ_IDLE_ANSWER_FIRSR = {}
QUIZ_NOWORD = '*' # символ заменяет "не открытые буквы" ######
##############################################################
MODE = 'M1' # ХИНТЫ. M1 - новый вих хинтов, M2 - старый вид ##
PTS = 'P2'  # Начисление очков: ##############################
ACC = 'A2'  # Уровень доступа к !сл: A1 - все, A2 - ток стар##
############# товавший викторину или модератор              ##
## P1 - таймаут / время_ответа / 3+1 / кол-во открытых букв ##
## P2 - (таймаут / время_ответа) / (прцнт_откр._слова / 10) ##
## * Первая формула рубит балы в пределах 0 - 5 в основном ###
## * Вторая формула даёт более широкую оценку ответу, размах #
##   баллов при этом от 0 до 50 (может кому то показаться не #
##   не честным, но мне это более нравится чем 1) ############
##############################################################
###%%%%%%###%%%%%%#####%%%%%%#################################
##%%####%%####%%######%%####%%################################
##%%##########%%######%%######################################
##%%##%%%%####%%######%%##%%%%################################
##%%##%%%%####%%######%%##%%%%################################
##%%####%%####%%######%%####%%################################
###%%%%%%###%%%%%%#####%%%%%%#################################
##############################################################

import threading

HELP = u'помощь по командам > "!викторина"'


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


def quiz_getbotjid(g):# THIS FUNCTION HAS USED ONLY IN BUSTER-BOT
        if g in GROUPCHATS:
                n=get_bot_nick(g)
                if n in GROUPCHATS[g]:
                        try: bj = GROUPCHATS[g][n]['jid'].split('/')[0]
                        except: pass
                        if bj in CLIENTS.keys():
                                return bj
        return JABBER_ID


def quiz_timer(groupchat, start_time):
        global QUIZ_TIME_LIMIT
        global QUIZ_CURRENT_TIME
        
	time.sleep(QUIZ_TIME_LIMIT)
	if QUIZ_CURRENT_TIME.has_key(groupchat) and QUIZ_CURRENT_ANSWER.has_key(groupchat) and start_time == QUIZ_CURRENT_TIME[groupchat]:
		QUIZ_CURRENT_ANSWER[groupchat]
		msg(quiz_getbotjid(groupchat), groupchat, u'(!) Время вышло! ' + sectomin(QUIZ_TIME_LIMIT) + u' прошло. Правильный ответ: ' + QUIZ_CURRENT_ANSWER[groupchat])
		if QUIZ_IDLENESS.has_key(groupchat):
			QUIZ_IDLENESS[groupchat] += 1
		else:
			QUIZ_IDLENESS[groupchat] = 1
		if QUIZ_IDLENESS[groupchat] >= QUIZ_IDLE_LIMIT:
			msg(quiz_getbotjid(groupchat), groupchat, u'(!) Викторина автоматичеки заверщена по бездействию! ' + str(QUIZ_IDLE_LIMIT) + ' вопросов без ответа.')
			del QUIZ_CURRENT_ANSWER[groupchat]
			quiz_list_scores(groupchat)
		else:
			quiz_ask_question(groupchat)

def quiz_new_question():
        global QUIZ_RECURSIVE_MAX
        
	line_num = random.randrange(33693)
	fp = file(QUIZ_FILE)
	for n in range(line_num + 1):
		if n == line_num:
			(question, answer) = string.split(fp.readline().strip(), '|', 1)
			return (unicode(question, 'utf-8'), unicode(answer, 'utf-8'))
		else:
			fp.readline()

def quiz_ask_question(groupchat):
        global answer
        global QUIZ_CURRENT_TIME
        global question
        global QUIZ_IDLE_ANSWER
        global QUIZ_IDLE_ANSWER_FIRSR
        QUIZ_IDLE_ANSWER = {groupchat:{}}
	(question, answer) = quiz_new_question()
	QUIZ_CURRENT_ANSWER[groupchat] = answer
	QUIZ_CURRENT_HINT[groupchat] = None
	QUIZ_CURRENT_HINT_NEW[groupchat] = None
	QUIZ_CURRENT_TIME[groupchat] = time.time()
	threading.Thread(None, quiz_timer, 'gch'+str(random.randrange(0,9999)), (groupchat, QUIZ_CURRENT_TIME[groupchat])).start()
	msg(quiz_getbotjid(groupchat),groupchat, u'(?) Внимание вопрос: \n' + question)

def quiz_ask_new_question(groupchat, ans):
        global QUIZ_CURRENT_TIME
        global answer
        global question
        global QUIZ_IDLE_ANSWER
        global QUIZ_IDLE_ANSWER_FIRSR
        QUIZ_IDLE_ANSWER = {groupchat:{}}
	(question, answer) = quiz_new_question()
	QUIZ_CURRENT_ANSWER[groupchat] = answer
	QUIZ_CURRENT_HINT[groupchat] = None
	QUIZ_CURRENT_HINT_NEW[groupchat] = None
	QUIZ_CURRENT_TIME[groupchat] = time.time()
	threading.Thread(None, quiz_timer, 'gch'+str(random.randrange(0,9999)), (groupchat, QUIZ_CURRENT_TIME[groupchat])).start()
	msg(quiz_getbotjid(groupchat), groupchat, u'(!) Правильный ответ: '+ans+u', cмена вопроса: \n' + question)
	
def quiz_answer_question(groupchat, nick, answer):
        global QUIZ_IDLE_ANSWER
        global QUIZ_IDLE_ANSWER_FIRSR
        
	DBPATH='dynamic/'+groupchat+'/quiz.cfg'
	if check_file(groupchat,'quiz.cfg'):
		QUIZ_SCORES = eval(read_file(DBPATH))
	jid = get_true_jid(groupchat+'/'+nick)
	jid = jid.lower()
	
	if QUIZ_CURRENT_ANSWER.has_key(groupchat):
                answer1 = QUIZ_CURRENT_ANSWER[groupchat].lower()
                answer2 = answer.lower()
                if answer1 == answer2:
                        if QUIZ_IDLE_ANSWER.has_key(groupchat):
                                if len(QUIZ_IDLE_ANSWER[groupchat]) != 0:
                                        if QUIZ_IDLE_ANSWER[groupchat].has_key(jid):
                                                if QUIZ_IDLE_ANSWER[groupchat][jid][1] == '1':
                                                        msg(quiz_getbotjid(groupchat), groupchat, nick+u': Ты уже ответил верно!')
                                                else:
                                                        razn = QUIZ_IDLE_ANSWER[groupchat][jid][0] - QUIZ_IDLE_ANSWER_FIRSR[groupchat]
                                                        msg(quiz_getbotjid(groupchat), groupchat, nick+u': Ты уже ответил правильно, опоздав на %.3f сек' % razn)
                                        else:
                                                QUIZ_IDLE_ANSWER[groupchat][jid] = [time.time(), '0']
                                                
                                                razn = QUIZ_IDLE_ANSWER[groupchat][jid][0] - QUIZ_IDLE_ANSWER_FIRSR[groupchat]
                                                msg(quiz_getbotjid(groupchat), groupchat, nick+u': Ты ответил правильно, но опоздал на %.3f сек' % razn)
                                        return

			if QUIZ_IDLENESS.has_key(groupchat):
				del QUIZ_IDLENESS[groupchat]
			answer_time = int(time.time() - QUIZ_CURRENT_TIME[groupchat])
			try:
                                if MODE == 'M1':
                                        alen = len(QUIZ_CURRENT_HINT_NEW[groupchat])
                                        blen = QUIZ_CURRENT_HINT_NEW[groupchat].count('')
                                        a = alen - blen
                                if MODE == 'M2':
                                        a = 0
                                        a = a + QUIZ_CURRENT_HINT[groupchat]
                        except:
                                a = 1
                        if PTS == 'P1':
                                points = QUIZ_TIME_LIMIT / answer_time / 3 + 1 / a
                        if PTS == 'P2':
                                try:
                                        alen = len(QUIZ_CURRENT_HINT_NEW[groupchat])
                                        blen = QUIZ_CURRENT_HINT_NEW[groupchat].count('')
                                        a = alen - blen
                                        procent = a * 100 / alen
                                except:
                                        procent = 10
                                
                                points = (QUIZ_TIME_LIMIT / answer_time) / (procent / 10)

			if points == 0:
                                pts = '0'
                        else:
                                pts = '+'+str(points)
			msg(quiz_getbotjid(groupchat), groupchat, u'(!) ' + nick + u', поздравляю! Лови ' + pts + u' очка в банк! Верный ответ: ' + answer)			
			if not QUIZ_SCORES.has_key(groupchat):
				QUIZ_SCORES[groupchat] = {}
			if QUIZ_SCORES[groupchat].has_key(jid):
				QUIZ_SCORES[groupchat][jid][0] += points
				QUIZ_SCORES[groupchat][jid][1] += points
				QUIZ_SCORES[groupchat][jid][2] = nick
				QUIZ_SCORES[groupchat][jid][3] += 1
			else:
				QUIZ_SCORES[groupchat][jid] = [points, points, nick, 1]
			
#			quiz_list_scores(groupchat)


                        QUIZ_IDLE_ANSWER[groupchat][jid] = [time.time(), '1']
                        QUIZ_IDLE_ANSWER_FIRSR[groupchat] = time.time()

                        if QUIZ_IDLE_ANSWER.has_key(groupchat):
                                if len(QUIZ_IDLE_ANSWER[groupchat]) == 1:
                                        time.sleep(1.0)
                                        quiz_ask_question(groupchat)
	write_file(DBPATH, str(QUIZ_SCORES))

def swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]
 
def sort(groupchat, mas, sort=1, count=10):
        base = mas[groupchat]
        arr = []
        str1 = ''
        for a in base:
                asd = base[a][sort]
                arr += [asd]
        i = len(arr)
        while i > 1:
                for j in xrange(i - 1):
                        if arr[j] < arr[j + 1]:
                                swap(arr, j, j + 1)
                i -= 1
        top10 = 1
        prim = ''
        charcount = 0

        for z in arr:                       
                for x in base:
                        nick = base[x][2]
                        if len(nick) > charcount:
                                charcount = len(nick)
                        
        for z in arr:                       
                for x in base:
                        nick = base[x][2]
                        if len(nick) < charcount:
                                nick += ' ' * (charcount - len(nick))
                        nick += ' '
                                
                        if base[x][sort] == z:
                                str1 += str(top10)+'. '+nick+' '+str(base[x][0])+'-'+str(base[x][1])+'-'+str(base[x][3])+'\n'
                                if top10 < count:
                                        top10 += 1
                                else:
                                        str1 = prim + str1
                                        return str1
        str1 = prim + str1
        return str1



def quiz_list_scores(groupchat, sort_=1, count=10):
	DBPATH='dynamic/'+groupchat+'/quiz.cfg'
	if check_file(groupchat,'quiz.cfg'):
		QUIZ_SCORES = eval(read_file(DBPATH))

        if QUIZ_SCORES.has_key(groupchat):
                if QUIZ_SCORES[groupchat]:
                        if QUIZ_IDLENESS.has_key(groupchat):
                                del QUIZ_IDLENESS[groupchat]
                        if QUIZ_CURRENT_ANSWER.has_key(groupchat):
                                result = u'(*) Текущий счет:\n[Ник][Счет за игру][Общий счет][Кол-во ответов]\n'
                        else:
                                result = u'(*) Текущий счет:\n[Ник][Последний счет][Общий счет][Кол-во ответов]\n'
                        result = result+sort(groupchat, QUIZ_SCORES, sort_, count)

			msg(quiz_getbotjid(groupchat), groupchat, result)

def handler_quiz_start(type, source, parameters):
	groupchat = source[1]
	DBPATH='dynamic/'+groupchat+'/quiz.cfg'
	if check_file(groupchat,'quiz.cfg'):
		QUIZ_SCORES = eval(read_file(DBPATH))
        jid = get_true_jid(source[1]+'/'+source[2])
        jid = jid.lower()
        try:
                if jid in MAFIA.keys():
                        reply(type, source, u'Для игры в викторину вам необходимо выйти из игры мафия!')
                        return
        except: pass
	if not groupchat:
		reply(type, source, u'Не в чате')
		return
	if QUIZ_CURRENT_ANSWER.has_key(groupchat):
		reply(type, source, u'Викторина уже существует! '+HELP)
		return
	
	if not QUIZ_SCORES.has_key(groupchat):
                QUIZ_SCORES[groupchat] = {}
                write_file(DBPATH, str(QUIZ_SCORES))
        if QUIZ_SCORES.has_key(groupchat):
                if QUIZ_SCORES[groupchat].has_key(jid):
                        for kjid in QUIZ_SCORES[groupchat]:
                                QUIZ_SCORES[groupchat][kjid][0] = 0
                        
                        write_file(DBPATH, str(QUIZ_SCORES))
        QUIZ_START[groupchat] = jid
        
	if QUIZ_IDLENESS.has_key(groupchat):
		del QUIZ_IDLENESS[groupchat]
#	msg(groupchat, u'[Викторина] Викторина начата! Очки обнулены.')
	quiz_ask_question(groupchat)

def handler_quiz_stop(type, source, parameters):
	groupchat = source[1]
	if QUIZ_CURRENT_ANSWER.has_key(groupchat):
		del QUIZ_CURRENT_ANSWER[groupchat]
		msg(quiz_getbotjid(groupchat), groupchat, u'(!) Викторина остановлена.')
		time.sleep(1.0)
		quiz_list_scores(groupchat, 0, 10)
	else:
		reply(type, source, u'Нет викторины, '+HELP)

def handler_quiz_next(type, source, parameters):
        if QUIZ_CURRENT_ANSWER.has_key(source[1]):
                jid = get_true_jid(source[1]+'/'+source[2])
                if ACC == 'A1':
                        quiz_ask_new_question(source[1], QUIZ_CURRENT_ANSWER[source[1]])
                if ACC == 'A2':
                        if (jid == QUIZ_START[source[1]]) | (user_level(source[1]+'/'+source[2], source[1]) >= 16):
                                quiz_ask_new_question(source[1], QUIZ_CURRENT_ANSWER[source[1]])
                        else:
                                reply(type, source, u'Настройкой плагина запрещено пользование этой командой членам, '+HELP)
        else:
                reply(type, source, u'Нет викторины, '+HELP)

def handler_quiz_hint(type, source, parameters):
        global ans
	groupchat = source[1]
        ans = QUIZ_CURRENT_ANSWER[groupchat]
	if QUIZ_CURRENT_ANSWER.has_key(groupchat):
		if QUIZ_IDLENESS.has_key(groupchat):
			del QUIZ_IDLENESS[groupchat]
		if QUIZ_CURRENT_HINT[groupchat] == None:
			QUIZ_CURRENT_HINT[groupchat] = 0
		if MODE == 'M1':
                        if QUIZ_CURRENT_HINT_NEW[groupchat] == None:
                                ms = ['']
                                QUIZ_CURRENT_HINT_NEW[groupchat] = []
                                for r in range(0, len(QUIZ_CURRENT_ANSWER[groupchat])):
                                        QUIZ_CURRENT_HINT_NEW[groupchat] += ms

                        ex = 1
                        while ex == 1:
                                a = random.choice(QUIZ_CURRENT_ANSWER[groupchat])
                                if not a in QUIZ_CURRENT_HINT_NEW[groupchat]:
                                        for t in range(0, len(QUIZ_CURRENT_ANSWER[groupchat])):
                                                if QUIZ_CURRENT_ANSWER[groupchat][t] == a:
                                                        QUIZ_CURRENT_HINT_NEW[groupchat][t] = a
                                                        ex = 0
                                hint = '' 
                        for hnt in QUIZ_CURRENT_HINT_NEW[groupchat]:
                                if hnt == '':
                                        hint += QUIZ_NOWORD
                                else:
                                        hint += hnt
                        if not '' in QUIZ_CURRENT_HINT_NEW[groupchat]:
                                quiz_ask_new_question(source[1], ans)
                        else:
                                msg(quiz_getbotjid(groupchat), groupchat, u'(*) Подсказка: ' + hint)
                if MODE == 'M2':
                        QUIZ_CURRENT_HINT[groupchat] += 1
                        hint = QUIZ_CURRENT_ANSWER[groupchat][0:QUIZ_CURRENT_HINT[groupchat]]
                        hint += ' *' * (len(QUIZ_CURRENT_ANSWER[groupchat]) - QUIZ_CURRENT_HINT[groupchat])
                        msg(quiz_getbotjid(groupchat), groupchat, u'(*) Подсказка: ' + hint)
                        if (len(QUIZ_CURRENT_ANSWER[groupchat]) - QUIZ_CURRENT_HINT[groupchat]) == 0:
                                quiz_ask_new_question(source[1], ans)
	else:
		reply(type, source, u'Нет викторины, '+HELP)

def handler_quiz_answer(type, source, parameters):
        global answer
        reply(type, source, answer)



def handler_quiz_scores(type, source, parameters):
	groupchat = source[1]
	
	DBPATH='dynamic/'+groupchat+'/quiz.cfg'
	if check_file(groupchat,'quiz.cfg'):
		QUIZ_SCORES = eval(read_file(DBPATH))

	if QUIZ_SCORES.has_key(groupchat):
                if QUIZ_SCORES[groupchat]:
                        if QUIZ_CURRENT_ANSWER.has_key(source[1]):
                                quiz_list_scores(groupchat, 0, 10)
                        else:
                                quiz_list_scores(groupchat, 1, 10)
                else:
                        reply(type, source, u'В БД пусто, '+HELP)
        else:
                reply(type, source, u'В БД пусто, '+HELP)

def handler_quiz_message(raw, type, source, body):
	groupchat = source[1]
	if groupchat and QUIZ_CURRENT_ANSWER.has_key(groupchat):
		quiz_answer_question(source[1], source[2], body.strip())

def handler_quiz_resend(type, source, body):
        global question
        groupchat = source[1]
        if QUIZ_CURRENT_ANSWER.has_key(groupchat):
                res = u'(*) Текущий вопрос: \n'+question
                reply(type, source, res)
        else:
                reply(type, source, u'Нет викторины, '+HELP)

def handler_quiz_help(type, source, body):
        if QUIZ_CURRENT_ANSWER.has_key(source[1]):
                stat = u'запущена'
        else:
                stat = u'не запущена'
        res = u'Викторина v3.0\n(с) Gigabyte\nВикторина сейчас: '+stat+u'\nВ базе данных: '+str(QUIZ_TOTAL_LINES)+u' вопросов\nКоманды:\n- !старт (игра, start) - запуск игры\n- !стоп (стой, stop) - остановка игры\n- !повтор (повтори, reply) - повторяет вопрос\n- !х (помоги, hint) - вывод подсказки (снимает баллы)\n- !сл (дальше, next) - следущий вопрос\n- !счет (счет, score) - вывод текущего счета и мини статистика\n- !base_del - удаление всей статистики для комнаты (без параметра), или для юзера (жид в параметре)\n+ сортировка статистики (во время игры по текущему счету, при окончании игры по текущему счету, вне игры по общему счету)\n+ форматирование статистики\n+ очистка статистики'
        if MODE == 'M1':
                m = u'* Новый тип хинтов (рандомный)'
        if MODE == 'M2':
                m = u'* Старый тип хинтов'
        if PTS == 'P1':
                p = u'* Старый тип начисления очков'
        if PTS == 'P2':
                p = u'* Новый тип начисления очков'
        if ACC == 'A1':
                a = u'* Доступ к !сл имеют все'
        if ACC == 'A2':
                a = u'* Доступ к !сл имеет только тот кто создал викторину и модераторы'
        res+= u'\nКонфигурация:\n'+m+'\n'+p+'\n'+a
        reply(type, source, res)


def handler_quiz_base_del(type, source, body):
	groupchat = source[1]
	
	DBPATH='dynamic/'+groupchat+'/quiz.cfg'
	if check_file(groupchat,'quiz.cfg'):
		QUIZ_SCORES = eval(read_file(DBPATH))

	if body == '':
                if QUIZ_SCORES.has_key(source[1]):
                        del QUIZ_SCORES[source[1]]
                        reply(type, source, u'<!> База данных была полностью очищена!')
                else:
                        reply(type, source, u'<!> База данных и так пустая!')
        else:
                if QUIZ_SCORES.has_key(source[1]):
                        if QUIZ_SCORES[source[1]].has_key(body):
                                del QUIZ_SCORES[source[1]][body]
                                reply(type, source, u'<!> Данные на указаный жид удалены')
                        else:
                                reply(type, source, u'<!> База данных и так пустая!')


                else:
                        reply(type, source, u'<!> База данных была полностью очищена!')
        write_file(DBPATH, str(QUIZ_SCORES))
        
        

register_command_handler(handler_quiz_start, '!старт', ['new','викторина','все'], 0, 'Запуск игры.', '!старт', ['!старт'])
register_command_handler(handler_quiz_help, '!викторина', ['new','викторина','все'], 0, 'Вывод хелпа.', '!викторина', ['!викторина'])
register_command_handler(handler_quiz_resend, '!повтор', ['new','викторина','все'], 0, 'Повтор текущего вопроса.', '!повтор', ['!повтор'])
register_command_handler(handler_quiz_stop, '!стоп', ['new','викторина','все'], 0, 'Остановка игры.', '!стоп', ['!стоп'])
register_command_handler(handler_quiz_hint, '!х', ['new','викторина','все'], 0, 'Показать подсказку (там русская ХЭ).', '!х', ['!х'])
register_command_handler(handler_quiz_scores, '!счет', ['new','викторина','все'], 0, 'Показывает статистику (выводит ник, очки за последнюю игру, общие очки).', '!счет', ['!счет'])
register_command_handler(handler_quiz_next, '!сл', ['new','викторина','все'], 0, 'Следущий вопрос.', '!сл', ['!сл'])
register_command_handler(handler_quiz_answer, '!ответ', ['new','викторина','все'], 100, 'Показывает правильный ответ <CHEAT>.', '!ответ', ['!ответ'])
register_command_handler(handler_quiz_base_del, '!base_del', ['new','викторина','все'], 100, 'Удаляет всю БД или определённую запись', '!base_del [жид]', ['!base_del foo@kabber.ru', '!base_del'])

register_command_handler(handler_quiz_start, '!игра', [], 0, 'Запуск игры.', '!игра', ['!игра'])

FNWQYI = {}
def hnd_nwqyi(t, s, p):
        global FNWQYI
        if not s in FNWQYI:
                FNWQYI[s]={}
                reply(t, s, u'/me из-за ложных срабатываний команда переименована в !игра')

register_command_handler(hnd_nwqyi, 'игра', [], 0, 'Запуск игры.', 'игра', ['игра'])
register_command_handler(handler_quiz_resend, 'повтори', [], 0, 'Повтор текущего вопроса.', 'повтори', ['повтори'])
register_command_handler(handler_quiz_stop, 'стой', [], 0, 'Остановка игры.', 'стой', ['стой'])
register_command_handler(handler_quiz_hint, 'помоги', [], 0, 'Показать подсказку (там русская ХЭ).', 'помоги', ['помоги'])
register_command_handler(handler_quiz_scores, 'счет', [], 0, 'Показывает статистику (выводит ник, очки за последнюю игру, общие очки).', 'счет', ['счет'])
register_command_handler(handler_quiz_next, 'дальше', [], 0, 'Следущий вопрос.', 'дальше', ['дальше'])

register_command_handler(handler_quiz_start, 'start', [], 0, 'Запуск игры.', 'start', ['start'])
register_command_handler(handler_quiz_resend, 'reply', [], 0, 'Повтор текущего вопроса.', 'reply', ['reply'])
register_command_handler(handler_quiz_stop, 'stop', [], 0, 'Остановка игры.', 'stop', ['stop'])
register_command_handler(handler_quiz_hint, 'hint', [], 0, 'Показать подсказку (там русская ХЭ).', 'hint', ['hint'])
register_command_handler(handler_quiz_scores, 'score', [], 0, 'Показывает статистику (выводит ник, очки за последнюю игру, общие очки).', 'score', ['score'])
register_command_handler(handler_quiz_next, 'next', [], 0, 'Следущий вопрос.', 'next', ['next'])

register_message_handler(handler_quiz_message)
