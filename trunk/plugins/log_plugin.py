#===istalismanplugin===
# -*- coding: utf-8 -*-

import re, os, math, time

SUBJECT_D = {}

LOG_CACHE_FILE = 'dynamic/logcache.txt'
LOG_WORK_FILE = 'dynamic/logwork.txt'

initialize_file(LOG_CACHE_FILE, '{}')
initialize_file(LOG_WORK_FILE, '{}')

LOG_WORK_DB = {}

try: LOG_WORK_DB = eval(read_file(LOG_WORK_FILE))
except: write_file(LOG_WORK_FILE, '{}')

try:
        if not os.path.exists(LOG_CACHE_FILE) or not isinstance(eval(read_file(LOG_CACHE_FILE)),dict):
                new=open(LOG_CACHE_FILE,'w')
                new.write('{}')
                new.close()
        LOG_FILENAME_CACHE = eval(read_file(LOG_CACHE_FILE))
except:
        write_file(LOG_CACHE_FILE, '{}')
        LOG_FILENAME_CACHE = eval(read_file(LOG_CACHE_FILE))


def log_write_header(fp, source, sub, (year, month, day, hour, minute, second, weekday, yearday, daylightsavings)):
        #print source
        try: log_write_header_(fp, source, sub, (year, month, day, hour, minute, second, weekday, yearday, daylightsavings))
        except: raise#!!!!!!+


def log_write_header_(fp, source, sub, (year, month, day, hour, minute, second, weekday, yearday, daylightsavings)):
    Months = ("", u"Января", u"Февраля", u"Марта", u"Апреля", u"Мая", u"Июня", u"Июля", u"Августа", u"Сентября", u"Октября", u"Ноября", u"Декабря")
    Days = (u"Понедельник", u"Вторник", u"Среда", u"Четверг", u"Пятница", u"Суббота", u"Воскресенье", u"")
    try:
            f='dynamic/'+source+'/backup_roomf.txt'
            db=eval(read_file(f))[source]['subject']
            db=db.replace('\n','<br />')
    except: db=u'Без темы'
    dn = Days[time.localtime()[6]]
    mn = Months[time.localtime()[1]]
    date = dn+', '+str(time.localtime()[2])+' '+mn
    #z = open(fName,'w')
    fp.write("""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dt">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<title>%s</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<style type="text/css">
<!--
.presence {color: #D0D0D0; font-style: italic; font-weight: bold}
.timestamp {color: #FFFFFF;}
.newacc {color: #E6D929; font-style: italic; font-weight: bold}
.timestamp a {color: #000000; text-decoration: none;}
.system {color: #BDB76B; font-weight: bold;}
.emote {color: #800080;}
.self {color: #0000AA;}
.selfmoder {color: #DC143C;}
.normal {color: #483d8b;}
.subject {color: #5aaed4;}
#mark { color: #aaa; text-align: right; font-family: monospace; letter-spacing: 3px }
h1 { color: #D0D0D0; font-family: sans-serif; border-bottom: #246 solid 3pt; letter-spacing: 3px; margin-left: 20pt;}
h2 { color: #ADFF2F; font-family: sans-serif; letter-spacing: 2px; text-align: center }
h3 { color: #FFFFFF; font-family: sans-serif; letter-spacing: 2px; text-align: center }
a.h1 {text-decoration: none;color: #369;}
h4 {
 border-width: 4px;
 border-style: double;
 border-color: #EB36BE;
 }
 h5 {
 border-width: 1px;
 border-style: double;
 border-color: #000000
 }
#//-->
</style>
</head>
<!-- <body bgcolor="#FFDEAD"> -->
<body>
<div>
<h4>
<span class="presence">%s<br />
%s</span><br />
<span class="subject">Тема: %s</span><br />
%s<tt>
""" % (source.encode('utf-8'),date.encode('utf-8'),source.encode('utf-8'),db.encode('utf-8'),('' if not source in GROUPCHATS or not GROUPCHATS[source]  else u'<span class="system">Список участников: '+', '.join([x for x in GROUPCHATS[source].keys() if GROUPCHATS[source][x].get('ishere',0) ])+'</span><br />').encode('utf8')))
    #z.close()


def log_write_footer(fp):
	fp.write('\n</tt>\n</div>\n</body>\n</html>')




def log_makelog_dir(logdir, source, str_year, str_month):
        if not os.path.exists(logdir):
                os.mkdir(logdir)
        if not os.path.exists(os.path.join(logdir,source)):
                os.mkdir(os.path.join(logdir,source))
        if not os.path.exists(os.path.join(logdir,source,str_year)):
                os.mkdir(os.path.join(logdir,source,str_year))
        if not os.path.exists(os.path.join(logdir,source,str_year,str_month)):
                os.mkdir(os.path.join(logdir,source,str_year,str_month))


def log_get_fp(type, source, sub,(year, month, day, hour, minute, second, weekday, yearday, daylightsavings)):
        fp=''
        fp_old=''
	if type == 'public':
		logdir = PUBLIC_LOG_DIR
	else:
		logdir = PRIVATE_LOG_DIR
		if source.count('/'): source=source.replace('/','_')
		try: i=os.path.exists(source)
		except UnicodeEncodeError:
                        enc=''
                        for x in source:
                                if ord(x)>127:
                                        enc+='?'
                                else:
                                        enc+=x
                        source=enc
	if logdir[-1] == '/':
		logdir = logdir[:-1]
	str_year = str(year)
	str_month = str(month)
	str_day = str(day)
	#source=source.encode('utf8','replace')
	log_dir = '/'.join([logdir, source, str_year, str_month])
	filename = logdir+'/'+source+'/'+str_year+'/'+str_month+'/'+str_day+'.html'
	alt_filename = '.'.join(['/'.join([logdir, source, str_year, str_month, str_day]), '_alt.html'])
	try:
                if not os.path.exists(log_dir):
                        if not os.path.exists(logdir):
                                os.mkdir(logdir)
                        if not os.path.exists(logdir+'/'+source):
                                os.mkdir(os.path.join(logdir,source))
                        if not os.path.exists(logdir+'/'+source+'/'+str_year):
                                os.mkdir(logdir+'/'+source+'/'+str_year)
                        if not os.path.exists(logdir+'/'+source+'/'+str_year+'/'+str_month):
                                os.mkdir(logdir+'/'+source+'/'+str_year+'/'+str_month)
        except: return 0
	if LOG_FILENAME_CACHE.has_key(source):
		if LOG_FILENAME_CACHE[source] != filename:
                        try:
                                fp_old = file(LOG_FILENAME_CACHE[source], 'a')
                        except:
                                write_file(LOG_CACHE_FILE, '{}')
                                s = LOG_FILENAME_CACHE[source].split('/')
                                if len(s)>3: log_makelog_dir(s[0],s[1],s[2],s[3])
                                fp_old = open(LOG_FILENAME_CACHE[source], 'w')
			log_write_footer(fp_old)
			fp_old.close()
		if os.path.exists(filename):
                        try:
                                fp = file(filename, 'a')
                                return fp
                        except:
                                return 0
		else:
			LOG_FILENAME_CACHE[source] = filename
			write_file(LOG_CACHE_FILE, str(LOG_FILENAME_CACHE))
			try:
                                fp = file(filename, 'w')
                        except:
                                return 0
			log_write_header(fp, source, sub, (year, month, day, hour, minute, second, weekday, yearday, daylightsavings))
			return fp
	else:
		if os.path.exists(filename):
			LOG_FILENAME_CACHE[source] = filename
			write_file(LOG_CACHE_FILE, str(LOG_FILENAME_CACHE))
			fp = file(alt_filename, 'a')
			return fp
		else:
			LOG_FILENAME_CACHE[source] = filename
			fp = file(filename, 'w')
			log_write_header(fp, source, sub, (year, month, day, hour, minute, second, weekday, yearday, daylightsavings))
			return fp

def log_regex_url(matchobj):
	# 06.03.05(Sun) slipstream@yandex.ru urls parser
	return '<a href="' + matchobj.group(0) + '">' + matchobj.group(0) + '</a>'



def log_handler_message(raw, type, source, body):
        global SUBJECT_D
        
	if not body:
		return
	if log_fail():
                return
        try:
                for e in raw.elements():
                        if e.name == 'subject':
                                SUBJECT_D[source[1]]=body
                                return
        except: pass
        try: body=body.replace(ADMIN_PASSWORD,'********')
        except: pass
	if type in ['groupchat','public'] and PUBLIC_LOG_DIR:
                if not source[1] in GROUPCHATS:
                        return
                if not source[1].count('conference.') and not source[1].count('.chat') and not source[1].count('muc.'):
                        return
                type='public'
		groupchat = source[1]
		nick = source[2]
		if groupchat in GROUPCHATS and nick in GROUPCHATS[groupchat] and 'ismoder' in GROUPCHATS[groupchat][nick] and GROUPCHATS[groupchat][nick]['ismoder'] == 1:
			ismoder=1
		else:
			ismoder=0
		log_write(body, nick, type, groupchat, ismoder)
	elif type in ['icq','chat','private'] and PRIVATE_LOG_DIR:
                type='private'
		jid = get_true_jid(source[1]+'/'+source[2])
		log_write(body, jid.split('@')[0], type, jid)

def log_handler_outgoing_message(target, body, obody):
        if log_fail():
                return
	if GROUPCHATS.has_key(target) or not body:
		return
	log_write(body, DEFAULT_NICK, 'private', get_true_jid(target))

def log_smile(n):
        return "<img src=\"http://pipec.ru/engine/data/emoticons/smile_"+str(n)+".gif\" alt=\"smile\">"

def log_write(body, nick, type, jid, ismoder=0):
        if jid in LOG_WORK_DB.keys():
                return
        if not body or not isinstance(body, basestring):
                return
        (year, month, day, hour, minute, second, weekday, yearday, daylightsavings) = time.localtime()
	#if not jid in GROUPCHATS.keys():
	#	jid = get_true_jid(jid)
	sub=''
        #        if not os.path.exists(PUBLIC_LOG_DIR+'/'+jid+'/'+str(year)+'/'+str(month)+'/'+str(day)+'.html') and nick:
        #                return
	if not nick or nick=='':
                sub=body
	decimal = str(int(math.modf(time.time())[0]*100000))
	# 06.03.05(Sun) slipstream@yandex.ru urls parser & line ends
	body = body.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
	body = re.sub('(http|ftp)(\:\/\/[^\s<]+)', log_regex_url, body)
	body = body.replace('\n', '<br/>')
	body = body.replace(':)',log_smile(654)).replace(':-)',log_smile(654)).replace(':-*',log_smile(652)).replace(':D',log_smile(653)).replace('*ROFL*',log_smile(653)).replace(':P',log_smile(650)).replace(':-P',log_smile(650)).replace(':-[',log_smile(422)).replace(':-\\',log_smile(437)).replace('=-O',log_smile(421)).replace('@}->--',log_smile(645))
	body = body.encode('utf-8');
	nick = nick.encode('utf-8');
	timestamp = '[%.2i:%.2i:%.2i]' % (hour, minute, second)
	fp = log_get_fp(type, jid, sub, (year, month, day, hour, minute, second, weekday, yearday, daylightsavings))
	try:
                if int(fp)==0:
                        log_write(body, nick, type, jid, ismoder)
                        return
        except: pass
        fp.write('<span class="timestamp"><a id="t' + timestamp[1:-1] + '.' + decimal + '" href="#t' + timestamp[1:-1] + '.' + decimal + '">' + timestamp + '</a></span> ')
	if not nick:
		fp.write('<span class="system">' + body + '</span><br />\n')
	elif body[:3].lower() == '/me':
		fp.write('<span class="emote">* %s%s</span><br />\n' % (nick, body[3:]))
	elif type == 'public' or nick == DEFAULT_NICK:
		if nick=='@$$leave$$@':
			fp.write('<span class="presence">' + body + '</span><br />\n')
		elif nick=='@$$join$$@':
			fp.write('<span class="presence">' + body + '</span><br />\n')
		elif nick=='@$$status$$@':
			fp.write('<span class="presence">' + body + '</span><br />\n')
		elif nick=='@$$ra$$@':
			fp.write('<span class="presence">' + body + '</span><br />\n')
		elif nick=='@$$userkick$$@':
			fp.write('<span class="presence">' + body + '</span><br />\n')
		elif nick=='@$$userban$$@':
			fp.write('<span class="presence">' + body + '</span><br />\n')
		elif nick=='@$$nickchange$$@':
			fp.write('<span class="presence">' + body + '</span><br />\n')
		elif nick=='@$$newacc$$@':
                        fp.write('<span class="presence">' + body + '</span><br />\n')
		else:
			if ismoder:
                                fp.write('<font color="#%s"><u>&lt;%s&gt;</u></font> %s<br />\n' % (NICKS_M_COLOR.get(nick,'465e67').encode('utf8'), nick, body))
				#fp.write('<span class="selfmoder">&lt;%s&gt;</span><span class="timestamp"> %s</span><br />\n' % (nick, body))
			else:
                                fp.write('<font color="#%s">&lt;%s&gt;</font> %s<br />\n' % (NICKS_M_COLOR.get(nick,'465e67').encode('utf8'), nick, body))
				#fp.write('<span class="self">&lt;%s&gt;</span><span class="timestamp"> %s</span><br />\n' % (nick, body))
	else:
		fp.write('<span class="normal">&lt;%s&gt;</span> %s<br />\n' % (nick, body))
	fp.close()

LOG_AFL_ROLE = {}

def log_handler_join(groupchat, nick, aff, role, cljid):
        return#######!!!+
        global LOG_AFL_ROLE
        if log_fail():
                return
        if not groupchat in GROUPCHATS:
                return
        if not groupchat.count('conference.') and not groupchat.count('.chat') and not groupchat.count('muc.'):
                return
        if len(nick)>19:
                nick=nick[:19]+'..>>>'
        if not groupchat in LOG_AFL_ROLE.keys():
                LOG_AFL_ROLE[groupchat]={}
        #if not nick in LOG_AFL_ROLE[groupchat].keys():
        #        LOG_AFL_ROLE[groupchat][nick]={}
        try:
                LOG_AFL_ROLE[groupchat][nick]=ROLES[role]+AFFILIATIONS[aff]
        except:
                pass
	log_write('%s joins the room as %s and %s' % (nick, role, aff), '@$$join$$@', 'public', groupchat)

def log_handler_leave(groupchat, nick, reason, code, cljid):
        if log_fail():
                return
        if not groupchat in GROUPCHATS:
                return
        if not groupchat.count('conference.') and not groupchat.count('.chat') and not groupchat.count('muc.'):
                return
        if len(nick)>19:
                nick=nick[:19]+'..>>>'
        if reason:
                if len(reason)>35:
                        reason=reason[:35]+'..>>>'
	if code:
		if code == '307':
			if reason:
				log_write('%s has been kicked (%s)' % (nick,reason), '@$$userkick$$@', 'public', groupchat)
			else:
				log_write('%s has been kicked' % (nick), '@$$userkick$$@', 'public', groupchat)
		elif code == '301':
			if reason:
				log_write('%s has been banned (%s)' % (nick,reason), '@$$userban$$@', 'public', groupchat)
			else:
				log_write('%s has been banned' % (nick), '@$$userban$$@', 'public', groupchat)
	else:
		if reason:
			log_write(u'%s вышел (%s)' % (nick,reason), '@$$leave$$@', 'public', groupchat)
		else:
			log_write(u'%s вышел' % (nick), '@$$leave$$@', 'public', groupchat)

LIST_OF_USER = {}

def log_handler_presence(prs, cljid):
        global LIST_OF_USER
        
        if log_fail():
                return
        stw = {u'online':u'в сети',u'chat':u'готов поболтать',u'dnd':u'занят',u'away':u'отсутствую',u'xa':u'ушел надолго',u'':u'онлайн'}
        aflw = {u'participant':u'участник',u'visitor':u'без голоса',u'member':u'постоялец',u'moderator':u'модератор',u'admin':u'администратор',u'owner':u'владелец конференции',u'none':u'без полномочий',u'':u''}
	stmsg,status,code,reason,newnick,add='','','','','',False
	try: jid = prs['from'].split('/')
	except: return
        groupchat = jid[0]
        if not groupchat in GROUPCHATS:
                return
        if not groupchat.count('@conference.') and not groupchat.count('@chat.') and not groupchat.count('@muc.'):
                return
        nick = prs['from'][len(groupchat)+1:]
        if nick and len(nick)>19: nick=nick[:19]+'..>>>'
	try:
                if nick and not nick in NICKS_M_COLOR.keys():
                        NICKS_M_COLOR[nick]="".join([hex(random.randrange(0, 255))[2:] for i in range(3)])
        except: pass
        if not nick in GROUPCHATS[groupchat] or not GROUPCHATS[groupchat][nick].get('ishere',0) or time.time()-GROUPCHATS[groupchat][nick]['joined']<1:
                add = True
        #if not groupchat in LIST_OF_USER:
        #        LIST_OF_USER[groupchat]=time.time()
        #        time.sleep(3)
        #        lu = ','.join([x for x in GROUPCHATS[groupchat].keys() if GROUPCHATS[groupchat][x]['ishere']])
        #        if not lu or lu.isspace():
        #                return
        #        log_write(u'Список участников: %s' % (lu), '@$$status$$@', 'public', groupchat)
        #        return
        #else:
        #        try:
        #                if time.time()-LIST_OF_USER[groupchat]<1 and time.time()-GROUPCHATS[groupchat][get_bot_nick(groupchat)]['joined']<1:
        #                        return
        #        except: pass
	
	type=''
	try: type=prs['type']
        except: pass
        if type == 'error':
                list = [i['code'] for i in prs.children if (i.name=='error')]
                if list:
                        log_write(u'Get Presence Error Code: '+list[0], '', 'public', groupchat)
                        return
	code = ''
	reason = ''
	afl=''
	role=''
	try:
                _x = [i for i in prs.children if (i.name=='x') and (i.uri == 'http://jabber.org/protocol/muc#user')][0]
                _item = [i for i in _x.children if i.name=='item'][0]
                try: stmsg = [i for i in prs.children if i.name=='status'][0].children[0]
                except: pass
                try: status = [i for i in prs.children if i.name=='show'][0].children[0]
                except: pass
                try: afl = _item['affiliation']
                except: pass
                try: role = _item['role']
                except: pass
                try: code = ''.join([i['code'] for i in _x.children if i.name=='status'])
                except: pass
                try: reason = [i for i in _item.children if i.name=='reason'][0].children[0]
                except: pass
        except: pass
        if reason and len(reason)>35: reason=reason[:35]+'..>>>'
	if code == '303':
		newnick = nick
		if len(newnick)>19:
                        newnick=newnick[:19]+'..>>>'
		log_write(u'%s теперь известен как %s' % (nick,newnick), '@$$nickchange$$@', 'public', groupchat)
	else:
		if type!='unavailable':

			
			if stmsg:
                                if len(stmsg)>60:
                                        stmsg=stmsg[:60]+'..'
			
			if groupchat in LOG_AFL_ROLE.keys():
                                if nick in LOG_AFL_ROLE[groupchat]:
                                        try:
                                                if ROLES[role]+AFFILIATIONS[afl]!=LOG_AFL_ROLE[groupchat][nick]:
                                                        LOG_AFL_ROLE[groupchat][nick]=ROLES[role]+AFFILIATIONS[afl]
                                                        log_write(u'%s получил новые права %s и %s ( причина: %s )' % (nick,role,afl,reason),'@$$newacc$$@','public',groupchat)
                                                        return
                                        except:
                                                pass

                        if add:
                                log_write(u'%s зашел как %s %s, %s' % (nick,aflw[role],aflw[afl],stw[status]),'@$$status$$@', 'public', groupchat)
                                return
                        
			if stmsg:
				log_write(u'%s сейчас %s (%s)' % (nick,stw[status],stmsg), '@$$status$$@', 'public', groupchat)
			else:
				log_write(u'%s сейчас %s' % (nick,stw[status]), '@$$status$$@', 'public', groupchat)


def log_make_dir(groupchat):
        (year, month, day, hour, minute, second, weekday, yearday, daylightsavings) = time.localtime()
        str_year = str(year)
	str_month = str(month)
	str_day = str(day)
	logdir = PUBLIC_LOG_DIR
	try:
                if not os.path.exists(logdir):
                        if not os.path.exists(logdir):
                                os.mkdir(logdir)
                        if not os.path.exists(logdir+'/'+groupchat):
                                os.mkdir(logdir+'/'+groupchat)
                        if not os.path.exists(logdir+'/'+groupchat+'/'+str_year):
                                os.mkdir(logdir+'/'+groupchat+'/'+str_year)
                        if not os.path.exists(logdir+'/'+groupchat+'/'+str_year+'/'+str_month):
                                os.mkdir(logdir+'/'+groupchat+'/'+str_year+'/'+str_month)
        except:
                pass

def log_fail():
        #t=len(threading.enumerate())
        #if t>30:
        #        return 1
        return 0

def log_on_off(t, s, p):
        if not s[1] in GROUPCHATS:
                return
        global LOG_WORK_FILE
        global LOG_WORK_DB
        txt=eval(read_file(LOG_WORK_FILE))
        if s[1] in txt:
                del txt[s[1]]
                LOG_WORK_DB=txt
                write_file(LOG_WORK_FILE, str(txt))
                reply(t, s, u'Логирование включено!')
                return
        else:
                txt[s[1]]={}
                LOG_WORK_DB=txt
                write_file(LOG_WORK_FILE, str(txt))
                reply(t, s, u'Логирование отключено!')

register_command_handler(log_on_off, '!логи', ['все'], 30, 'включает/отключает запись логов в конфе', '!логи', ['!логи'])

def set_log_pass(t, s, p):
        def my_quote(text, EscapeOnly=False):
                s = text.replace('\\', '\\\\').replace('"', '\\"').replace('`', '\\`')
                if not EscapeOnly: s = '"' + s + '"'
                return s
        if not s[1] in GROUPCHATS:
                return
        if not PUBLIC_LOG_DIR:
                return
        txt=eval(read_file(LOG_WORK_FILE))
        if s[1] in txt:
                reply(t, s, u'У вас логирование отключено!')
                return
        PATH = PUBLIC_LOG_DIR + '/' + s[1] + '/'
        if p in ['0','off','clear']:
                try: os.remove(PATH + '.htaccess')
                except OSError: pass
                try: os.remove(PATH + '.htpasswd')
                except OSError: pass
                reply(t, s, 'cleared')
                return
        p = p.split()
        if len(p) == 2:
                f = file(PATH + '.htaccess', 'w')
                f.write('AuthType Basic\nAuthName "Ask room owner for the username/password"\nAuthUserFile %s.htpasswd\nrequire valid-user' % (PATH.encode('utf8','replace'), ))
                f.close()
                user = my_quote(p[0])
                passwd = my_quote(p[1])
                PF = my_quote(PATH + '.htpasswd')
                cmd = u'sh -c \'htpasswd -bmc %s %s %s\' 2>&1' % (PF, user, passwd)
                cmd = cmd.encode('utf8')
                pipe = os.popen(cmd)
                time.sleep(1)
                m = pipe.read().decode('utf8', 'replace')
                reply(t, s, m)
        else: reply(t, s, u'Недостаточно параметров!')

register_command_handler(set_log_pass, '!логпасс', ['все'], 30, 'Стирает/устанавливает пароль на чтения публичных логов конфы', '!логпасс <userneme> <password>', ['!логпасс root secret','!логпасс 0'])
   
	
if PUBLIC_LOG_DIR:
        register_stage1_init(log_make_dir)
	register_message_handler(log_handler_message)
	#register_join_handler(log_handler_join)
	register_leave_handler(log_handler_leave)
	register_presence_handler(log_handler_presence)
if PRIVATE_LOG_DIR:
	register_outgoing_message_handler(log_handler_outgoing_message)
