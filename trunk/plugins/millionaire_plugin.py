#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Endless bot plugin v1.0

# Coded by: Avinar (avinar@xmpp.ru)
# http://avinar.net.ru

# licence show in another plugins ;)

# формат базы: каталог static/millionaire/
# в нем 15 файлов (1-15) в формате:

# вопрос|-ответ#+правильный_ответ#-ответ#-ответ

# MILLIONAIRE[groupchat][jid] =	{'questions':[[],[],[]...[]],
#								'stage':n,
#								'current':m,
#								'answer':x,
#								'summary':y,
#								'hints':[1,1,1]}

MILLIONAIRE={}

MILLIONAIRE_MONEY={	0:100,
					1:200,
					2:300,
					3:500,
					4:1000,
					5:2000,
					6:4000,
					7:8000,
					8:16000,
					9:32000,
					10:64000,
					11:125000,
					12:250000,
					13:500000,
					14:1000000}
					

def millionaire_load(groupchat,jid):
	global MILLIONAIRE
	if not MILLIONAIRE.has_key(groupchat):
		MILLIONAIRE[groupchat]={}
	DBPATH='dynamic/'+groupchat+'/millionaire.txt'
	if check_file(groupchat,'millionaire.txt'):
		localdb = eval(read_file(DBPATH))
		if localdb.has_key(jid):
			MILLIONAIRE[groupchat][jid]=localdb[jid]
		else:
			MILLIONAIRE[groupchat][jid]={}

def millionaire_write(groupchat,jid):
	global MILLIONAIRE
	if check_file(groupchat,'millionaire.txt'):
		localdb = eval(read_file('dynamic/'+groupchat+'/millionaire.txt'))
		localdb[jid]=MILLIONAIRE[groupchat][jid]
		write_file('dynamic/'+groupchat+'/millionaire.txt', str(localdb))
	else:
		print 'error writing millionaire base'

def millionaire_call(type, source, parameters):
	global GROUPCHATS
	if not GROUPCHATS.has_key(source[1]):
		reply(type, source, u'Только для конференций!')
		return

	parameters=parameters.strip()
	if parameters.count(' '):
		arg=parameters.split(' ',1)[1]
		parameters=parameters.split(' ',1)[0]
	else:
		arg=None
	
	parameters=parameters.lower()
	if not parameters:
		reply(type, source, u'''Игра "О,счастливчик!\nПринцип игры аналогичен одноименной телепрограмме.
Некоторые нюансы:
  При игре в привате начисление очков идет на счет вашего JID, а в общем чате - на счет конфы.
Отвечать на вопросы необходимо цифрой!
  
Для запуска игры наберите:
  !миллионер старт
Закончить и забрать очки:
  !миллионер стоп
Для просмотра результатов:
  !миллионер счет
Для получния подсказки:
  !подсказка n 
[где n - число от 1 до 3. 1-помощь компьютера, 2-50:50, 3-помощь бота.]''')
		return
	elif parameters == u'счет':
		millionaire_summary(type, source, arg)
		return
	elif parameters == u'стоп':
		millionaire_stop(type, source, None)
		return
	elif parameters == u'старт':
		millionaire_start(type, source, None)
		return
	else:
		reply(type, source, u'Неизвестный параметр. Прочти помощь!')
		return


def millionaire_start(type, source, parameters):
	global MILLIONAIRE
	if type == 'private':
		jid = get_true_jid(source[1] + '/' + source[2])
	else:
		jid = 'all'
	groupchat = source[1]
	millionaire_load(groupchat,jid)
	if not MILLIONAIRE[groupchat][jid].has_key('stage'):
		MILLIONAIRE[groupchat][jid]['stage']=0
		MILLIONAIRE[groupchat][jid]['questions']=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
		MILLIONAIRE[source[1]][jid]['hints'] = [1,1,1]
		MILLIONAIRE[groupchat][jid]['summary']=0
		millionaire_get_new_question(type, source, jid)
	
	
	millionaire_make_question(type, source, jid)
		
def millionaire_stop(type, source, parameters):
	global MILLIONAIRE
	if type == 'private':
		jid = get_true_jid(source[1] + '/' + source[2])
	else:
		jid = 'all'
	if MILLIONAIRE.has_key(source[1]) and MILLIONAIRE[source[1]].has_key(jid):
		if MILLIONAIRE[source[1]][jid]['stage'] != 0:
			summ = MILLIONAIRE_MONEY[MILLIONAIRE[source[1]][jid]['stage']-1]
			MILLIONAIRE[source[1]][jid]['summary'] += summ
			MILLIONAIRE[source[1]][jid]['hints'] = [1,1,1]
			MILLIONAIRE[source[1]][jid]['stage'] = 0
			reply(type, source, u'Игра остановлена.\nПавильный ответ: %d\nВаш выигрыш: %dр, Всего: %dр' % (MILLIONAIRE[source[1]][jid]['answer'],summ,MILLIONAIRE[source[1]][jid]['summary']))
			millionaire_get_new_question(type, source, jid)
			millionaire_write(source[1],jid)
			del MILLIONAIRE[source[1]][jid]
		else:
			reply(type, source, u'Игра остановлена. Ваш общий выигрыш: %d рублей' % (MILLIONAIRE[source[1]][jid]['summary']))
			del MILLIONAIRE[source[1]][jid]
	else:
		reply(type, source, u'Игра не была начата.')
	
def millionaire_summary(type, source, parameters):
	global MILLIONAIRE, GROUPCHATS
	
	groupchat=source[1]
	
	if not MILLIONAIRE.has_key(groupchat):
		MILLIONAIRE[groupchat]={}
	
	if parameters:
		if GROUPCHATS[source[1]].has_key(parameters):
			jid = get_true_jid(source[1] + '/' + parameters)
		elif parameters.count('@') and parameters.count('.'):
			jid=parameters
		else:
			reply(type, source, u'Я такого не знаю.')
			return
		if not MILLIONAIRE[groupchat].has_key(jid):
			millionaire_load(source[1],jid)
		if MILLIONAIRE[groupchat][jid].has_key('summary'):
			reply(type, source, u'Пользователь %s заработал %d рублей.' % (parameters,MILLIONAIRE[groupchat][jid]['summary']) )
		else:
			reply(type, source, u'А он еще не играл.')

	else:
		if type == 'private':
			jid = get_true_jid(source[1] + '/' + source[2])
			millionaire_load(source[1],jid)
			if MILLIONAIRE[groupchat][jid].has_key('summary'):
				reply(type, source, u'Ты заработал %d рублей.' % (MILLIONAIRE[groupchat][jid]['summary']) )
			else:
				reply(type, source, u'А ты еще не играл.')
		else:
			jid = get_true_jid(source[1] + '/' + source[2])
			millionaire_load(source[1],jid)
			millionaire_load(source[1],'all')
			if MILLIONAIRE[groupchat][jid].has_key('summary') and MILLIONAIRE[groupchat]['all'].has_key('summary'):
				reply(type, source, u'Ты заработал %d рублей.\nНа счету конференции %d рублей.' % (MILLIONAIRE[groupchat][jid]['summary'],MILLIONAIRE[groupchat]['all']['summary']) )
			elif MILLIONAIRE[groupchat][jid].has_key('summary'):
				reply(type, source, u'Ты заработал %d рублей, а на счету конференции пусто.' % (MILLIONAIRE[groupchat][jid]['summary']) )
			elif MILLIONAIRE[groupchat]['all'].has_key('summary'):
				reply(type, source, u'Конференция заработала %d рублей, а ты еще не играл.' % (MILLIONAIRE[groupchat]['all']['summary']) )
			else:
				reply(type, source, u'Тут еще никто не играл.')
	
def	millionaire_get_new_question(type, source, jid):
	stage = MILLIONAIRE[source[1]][jid]['stage']
	if not len(MILLIONAIRE[source[1]][jid]['questions'][stage]):
		fp = file('static/millionaire/'+str(MILLIONAIRE[source[1]][jid]['stage']+1)+'.txt')
		lines=fp.readlines()
		fp.close()
		MILLIONAIRE[source[1]][jid]['questions'][stage]=range(0,len(lines))
	MILLIONAIRE[source[1]][jid]['current']=random.choice(MILLIONAIRE[source[1]][jid]['questions'][stage])
	MILLIONAIRE[source[1]][jid]['questions'][stage].remove(MILLIONAIRE[source[1]][jid]['current'])
	return
		
	
def millionaire_make_question(type, source, jid):
	fp = file('static/millionaire/'+str(MILLIONAIRE[source[1]][jid]['stage']+1)+'.txt')
	lines=fp.readlines()
	fp.close()
	line = lines[MILLIONAIRE[source[1]][jid]['current']].strip()
	rep=line.split('|')[0]
	answ=line.split('|')[1].split('#')
	
	ls=range(4)
	random.shuffle(ls)
	num=1
	for x in ls:
		a = answ[x]
		if a[0] == '+':
			MILLIONAIRE[source[1]][jid]['answer'] = num
		rep += '\n' + str(num) + ') ' + a[1:]
		num+=1
	millionaire_write(source[1],jid)
	reply(type, source, rep)
	return



def handler_millionaire_chat(raw, type, source, parameters):
	global MILLIONAIRE
	if type == 'private':
		jid = get_true_jid(source[1] + '/' + source[2])
	else:
		jid = 'all'
	parameters=parameters.strip()
	botnick=get_bot_nick(source[1])
	if parameters[:len(botnick)] == botnick and parameters[len(botnick):].count(' '):
		parameters=parameters.split(' ')[-1]
	if not parameters.isdigit():
		return
	if not MILLIONAIRE.has_key(source[1]):
		return
	if MILLIONAIRE[source[1]].has_key(jid) and MILLIONAIRE[source[1]][jid].has_key('answer'):
		parameters=int(parameters)
		if parameters == 7:
			millionaire_start(type, source, None)
			return
		elif parameters == 8:
			millionaire_stop(type, source, None)
			return
		if parameters < 1 or parameters > 4:
			return
			
		stage = MILLIONAIRE[source[1]][jid]['stage']
		
		
		if parameters == MILLIONAIRE[source[1]][jid]['answer']:
			if stage == 14:
				MILLIONAIRE[source[1]][jid]['summary'] += 1000000
				ans=random.choice([	u'Это фантастика!!! 1 миллион рублей зачислен на счет!',
									u'Невероятно! Это правильный ответ!!! 1 миллион рублей зачислен на счет!'])
				reply(type, source, u'%s\nВаш общий выигрыш: %dр' % (ans,MILLIONAIRE[source[1]][jid]['summary']))
				millionaire_get_new_question(type, source, jid)
				millionaire_write(source[1],jid)
				time.sleep(3)
				reply(type, source, u'Хотите сыграть еще?\n7) да!\n8) нет.')
				
			else:
				MILLIONAIRE[source[1]][jid]['stage'] += 1
				if stage > 8:
					summ = 32000
				elif stage > 3:
					summ = 1000
				else:
					summ = 0
				ans=random.choice([	u'Браво! Ответ верный!',
									u'Правильно!',
									u'Вы правы!',
									u'Правильно!',
									u'Верно!',
									u'Абсолютно точно!',
									u'Гениально!',
									u'Вы не ошиблись!',
									u'Да, действительно это так!',
									u'Вы ответили правильно!',
									u'Полностью с Вами согласен!',
									u'Молодец! Так держать.',
									u'Я полагаю, Вы правы!',
									u'Интуиция Вас не подвела!',
									u'Я тоже так думаю!',
									u'Наверное, Вы знали. Знание - сила!',
									u'Совершенно верно!',
									u'И это, без сомнений, правильный ответ!',
									u'Сегодня Вам везет!',
									u'Слушайте, как Вам везет!',
									u'Сегодня фортуна Вам улыбается!',
									u'Ну, конечно!',
									u'Завидую Вашей уверенности!',
									u'Угадали!!!',
									u'В яблочко!',
									u'Точно!!!',
									u'Так точно!',
									u'Ну правильно, правильно!',
									u'Как вы догадались?!',
									u'Как ни странно, но это правильно!'])
								
				reply(type, source, u'%s\nВаш текущий выигрыш: %dр, несгораемый: %dр' % (ans,MILLIONAIRE_MONEY[stage],summ))
				
				millionaire_get_new_question(type, source, jid)
				time.sleep(3)
				millionaire_make_question(type, source, jid)

			
		else:
			
			if stage > 9:
				summ = 32000
			elif stage > 4:
				summ = 1000
			else:
				summ = 0
			MILLIONAIRE[source[1]][jid]['summary'] += summ
			MILLIONAIRE[source[1]][jid]['hints'] = [1,1,1]
			MILLIONAIRE[source[1]][jid]['stage'] = 0
			ans=random.choice([	u'К сожалению, ответ не верный!',
								u'Увы, но это не верный ответ!',
								u'Вы не правы!',
								u'Вы ошиблись!'])
								
			reply(type, source, u'%s\nПавильный ответ: %d\nВаш выигрыш: %dр, Всего: %dр' % (ans,MILLIONAIRE[source[1]][jid]['answer'],summ,MILLIONAIRE[source[1]][jid]['summary']))
			millionaire_get_new_question(type, source, jid)
			millionaire_write(source[1],jid)
			time.sleep(3)
			reply(type, source, u'Хотите сыграть еще?\n7) да\n8) нет')			

			
			
def millionaire_hint(type, source, parameters):
	global GROUPCHATS
	if not GROUPCHATS.has_key(source[1]):
		reply(type, source, u'Только для конференций!')
		return

	parameters=parameters.lower().strip()
	if parameters:
		if type == 'private':
			jid = get_true_jid(source[1] + '/' + source[2])
		else:
			jid = 'all'
		if MILLIONAIRE.has_key(source[1]) and MILLIONAIRE[source[1]].has_key(jid):
			if parameters.isdigit():
				parameters=int(parameters)
				if parameters < 1 or parameters > 3:
					reply(type, source, u'Недопустимый параметр!')
				else:
					if MILLIONAIRE[source[1]][jid]['hints'][parameters-1]:
						MILLIONAIRE[source[1]][jid]['hints'][parameters-1]=0
						valid=MILLIONAIRE[source[1]][jid]['answer']
						notvalid=range(1,5)
						notvalid.remove(valid)
						
						if parameters == 1:
							if random.randrange(100) < 90:
								ans=valid
							else:
								ans=random.choice(notvalid)
							reply(type, source, u'Компьютер утверждает, что ответ %d!' % (ans))
						elif parameters == 2:
							tmp=[valid,random.choice(notvalid)]
							random.shuffle(tmp)
							reply(type, source, u'Правильный ответ %d или %d!' % tuple(tmp))
						else:
							if random.randrange(100) < 50:
								ans=valid
							else:
								ans=random.choice(notvalid)
							reply(type, source, u'Я предполагаю, что ответ %d!' % ans)
						millionaire_write(source[1],jid)
					else:
						reply(type, source, u'Подсказка уже использована!')
			else:
				reply(type, source, u'Необходимо число от 1 до 3!')
		else:
			reply(type, source, u'Игра не начата.')
	else:
		reply(type, source, u'''Игра "О,счастливчик!"
Доступные подсказки: 
  1) помощь компьютера
  2) 50:50
  3) помощь бота
Для получния подсказки:
  !подсказка n 
[где n - число от 1 до 3]''')


register_command_handler(millionaire_call, '!миллионер', ['игры','все'], 0, 'Игра "О,счастливчик! \n(При игре в привате начисление очков идет на счет вашего JID, а в общем чате - на счет конфы.)\nПодробности в самой команде. \nОтвечать на вопросы нужно цифрой!\nP.S.: деньги не выплчиваются, не перечисляются и вобще они не существуют ;)', '!миллионер [<параметр>]', ['!миллионер','!миллионер старт','!подсказка 2'])
register_command_handler(millionaire_hint, '!подсказка', ['игры','все'], 0, 'Подсказки для игры "О,счастливчик!', '!подсказка <число>', ['!подсказка','!подсказка 1'])

register_message_handler(handler_millionaire_chat)

#register_stage1_init(acmd_init)


