# -*- coding: utf-8 -*-

GLOBACCESS_FILE = 'dynamic/globaccess.cfg'
ACCBYCONF_FILE = 'dynamic/accbyconf.cfg'

def change_access_temp(gch, source, level=0):
	global ACCBYCONF
	jid = get_true_jid(source)
	try:
		level = int(level)
	except:
		level = 0
	if not ACCBYCONF.has_key(gch):
		ACCBYCONF[gch] = gch
		ACCBYCONF[gch] = {}
	if not ACCBYCONF[gch].has_key(jid):
		ACCBYCONF[gch][jid]=jid
	ACCBYCONF[gch][jid]=level

def change_access_perm(gch, source, level=None):
	global ACCBYCONF
	jid = get_true_jid(source)
	try:
		level = int(level)
	except:
		pass
	temp_access = eval(read_file(ACCBYCONF_FILE))
	if not temp_access.has_key(gch):
		temp_access[gch] = gch
		temp_access[gch] = {}
	if not temp_access[gch].has_key(jid):
		temp_access[gch][jid]=jid
	if level:
		temp_access[gch][jid]=level
	else:
		del temp_access[gch][jid]
	write_file(ACCBYCONF_FILE, str(temp_access))
	if not ACCBYCONF.has_key(gch):
		ACCBYCONF[gch] = gch
		ACCBYCONF[gch] = {}
	if not ACCBYCONF[gch].has_key(jid):
		ACCBYCONF[gch][jid]=jid
	if level:
		ACCBYCONF[gch][jid]=level
	else:
		del ACCBYCONF[gch][jid]
	get_access_levels(source[3])

def change_access_perm_glob(source, level=0):
	global GLOBACCESS
	jid = get_true_jid(source)
	temp_access = eval(read_file(GLOBACCESS_FILE))
	if level:
		temp_access[jid] = level
	else:
		del temp_access[jid]
	write_file(GLOBACCESS_FILE, str(temp_access))
	get_access_levels(source[3])

def change_access_temp_glob(source, level=0):
	global GLOBACCESS
	jid = get_true_jid(source)
	if level:
		GLOBACCESS[jid] = level
	else:
		del GLOBACCESS[jid]


def handler_access_view_access(type, source, parameters):
	accdesc={'-100':u'(полный игнор)','-1':u'(заблокирован)','0':u'(никто)','1':u'(пасхалка :) )','10':u'(юзер)','11':u'(мембер)','15':u'(модер)','16':u'(модер)','20':u'(админ)','30':u'(овнер)','40':u'(джойнер)','100':u'(админ бота)'}
	if not parameters:
		level=str(user_level(source[1]+'/'+source[2], source[1]))
		if level in accdesc.keys():
			levdesc=accdesc[level]
		else:
			levdesc=''
		reply(type, source, level+u' '+levdesc)
	else:
                if len(parameters)>21: return
		if not source[1] in GROUPCHATS:
			reply(type, source, u'это возможно только в конференции')
			return
		nicks = GROUPCHATS[source[1]].keys()
		if parameters.strip() in nicks:
			level=str(user_level(source[1]+'/'+parameters.strip(),source[1]))
			if level in accdesc.keys():
				levdesc=accdesc[level]
			else:
				levdesc=''
			reply(type, source, level+' '+levdesc)
		else:
			reply(type, source, u'а он тут?')

def handler_access_set_access(type, source, parameters):
	if not source[1] in GROUPCHATS:
		reply(type, source, u'это возможно только в конференции')
		return
	splitdata = string.split(parameters)
	if len(splitdata) > 1:
		try:
			int(splitdata[1].strip())
		except:
			reply(type, source, u'ошибочный запрос. прочитай помощь по использованию команды')
			return
		if int(splitdata[1].strip())>100 or int(splitdata[1].strip())<-100:
			reply(type, source, u'ошибочный запрос. прочитай помощь по использованию команды')
			return
	nicks=GROUPCHATS[source[1]]
	tjidto=get_true_jid(source[1]+'/'+splitdata[0].strip())
	us=splitdata[0].strip()
	if not splitdata[0].strip() in nicks and us.count('@'):
                tjidto=splitdata[0].strip()
	tjidto=get_true_jid(source[1]+'/'+splitdata[0].strip())
	tjidsource=get_true_jid(source)
	groupchat=source[1]
	jidacc=user_level(source, groupchat)
	toacc=user_level(tjidto, groupchat)

	if len(splitdata) > 1:
		if tjidsource in ADMINS:
			pass
		else:
			if tjidto==tjidsource:
				if int(splitdata[1]) > int(jidacc):
					reply(type, source, u'недостаточно прав')
					return
			elif int(toacc) > int(jidacc):
				reply(type, source, u'недостаточно прав')
				return
			elif int(splitdata[1]) >= int(jidacc):
				reply(type, source, u'недостаточно прав')
				return
	else:
		if tjidsource in ADMINS:
			pass
		else:
			if tjidto==tjidsource:
				pass
			elif int(toacc) > int(jidacc):
				reply(type, source, u'недостаточно прав')
				return

	if len(splitdata) == 1:
		change_access_perm(source[1], tjidto)
		if splitdata[0].strip()==source[2]:
			reply(type, source, u'постоянный доступ снят. тебе необходимо перезайти в конференцию')
		else:
			reply(type, source, u'постоянный доступ снят. %s, перезайди в конференцию' % splitdata[0].strip())
	elif len(splitdata) == 2:
		change_access_temp(source[1], tjidto, splitdata[1].strip())
		reply(type, source, u'доступ выдан до выхода из конференции')
	elif len(splitdata) == 3:
		change_access_perm(source[1], tjidto, splitdata[1].strip())
		reply(type, source, u'выдан постоянный доступ')

def handler_access_set_access_glob(type, source, parameters):
	#if not source[1] in GROUPCHATS:
	#	reply(type, source, u'это возможно только в конференции')
	#	return
	if parameters:
		splitdata = parameters.strip().split()
		if len(splitdata)<1 or len(splitdata)>2:
			reply(type, source, u'ошибочный запрос. прочитай помощь по использованию команды')
			return
		nicks=''
		if source[1] in GROUPCHATS:
                        nicks=GROUPCHATS[source[1]].keys()
		tjidto=get_true_jid(source[1]+'/'+splitdata[0])
		if not splitdata[0].strip() in nicks:
                        if splitdata[0].count('@'):
                                tjidto=splitdata[0]
                        else:
                                reply(type,source,u'ник либо содержит пробелы,либо юзера нет в чате!')
                                return
		if len(splitdata)==2:
			change_access_perm_glob(tjidto, int(splitdata[1]))
			reply(type, source, u'дал')
		else:
			change_access_perm_glob(tjidto)
			reply(type, source, u'снял')

def get_access_levels(cljid):
	global GLOBACCESS
	global ACCBYCONFFILE
	GLOBACCESS = eval(read_file(GLOBACCESS_FILE))
	for jid in ADMINS:
		GLOBACCESS[jid] = 100
		write_file(GLOBACCESS_FILE, str(GLOBACCESS))
	ACCBYCONFFILE = eval(read_file(ACCBYCONF_FILE))

register_stage0_init(get_access_levels)
register_command_handler(handler_access_set_access, 'локдоступ', ['доступ','админ','все'], 15, 'Устанавливает или снимает (если ник писать без уровня, после снятия доступа нужно обязательно перезайти в конференцию) уровень доступа для определённого ника на определённый уровень. Поддерживаются только ники без пробела. Если указываеться третий параметр, то изменение происходит навсегда, иначе установленный уровень будет действовать до выхода бота или пользователя из конференции.\n-100 - абсолютное игнорирование, все сообщения от пользователя с таким доступом будут пропускатся на уровне ядра бота\n-1 - не сможет сделать ничего\n0 - очень ограниченное кол-во команд и макросов, автоматически присваивается гостям (visitor)\n10 - стандартный набор команд и макросов, автоматически присваивается пользователям (participant)\n11 - расширенный набор команд и макросов, автоматически присваивается участникам (member)\n15 (16) - набор команд для модераторов, автоматически присваивается модераторам (moderator)\n20 - набор команд и макросов для администраторов, автоматически присваивается администраторам конференции (admin)\n30 - набор команд и макросов для владельца, автоматически присваиватся владельцам конференции (owner)\n40 - не реализовано сейчсас толком, позволяет пользователю с этим доступом заводить и выводить бота из конференций + все возможности доступа 30\n100 - администратор бота, может всё.', 'локдоступ <ник> [уровень] [навсегда]', ['локдоступ guy 100', 'локдоступ guy 100 что-нибудь'])
register_command_handler(handler_access_set_access_glob, 'глобдоступ', ['доступ','суперадмин','все'], 100, 'Устанавливает или снимает (если ник писать без уровня) уровень доступа для определённого ника на определённый уровень ГЛОБАЛЬНО. Поддерживаются только ники без пробела.', 'глобдоступ <ник|jid> [уровень]', ['глобдоступ guy 100','глобдоступ guy'])
register_command_handler(handler_access_view_access, 'доступ', ['админ','все'], 0, 'Показывает уровень доступа определённого ника.\n-100 - абсолютное игнорирование, все сообщения от пользователя с таким доступом будут пропускатся на уровне ядра бота\n-1 - не сможет сделать ничего\n0 - очень ограниченное кол-во команд и макросов, автоматически присваивается гостям (visitor)\n10 - стандартный набор команд и макросов, автоматически присваивается пользователям (participant)\n11 - расширенный набор команд и макросов, автоматически присваивается участникам (member)\n15 (16) - набор команд и макросов для модераторов, автоматически присваивается модераторам (moderator)\n20 - набор команд и макросов для администраторов, автоматически присваивается администраторам конференции (admin)\n30 - набор команд и макросов для владельца, автоматически присваиватся владельцам конференции (owner)\n40 - не реализовано сейчсас толком, позволяет пользователю с этим доступом заводить и выводить бота из конференций + все возможности доступа 30\n100 - администратор бота, может всё.', 'доступ [ник]', ['доступ', 'доступ guy'])
