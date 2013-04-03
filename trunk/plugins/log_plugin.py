#===istalismanplugin===
# -*- coding: utf-8 -*-

import re, os, math, time

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
        try: log_write_header_(fp, source, sub, (year, month, day, hour, minute, second, weekday, yearday, daylightsavings))
        except: pass
	

def log_write_header_(fp, source, sub, (year, month, day, hour, minute, second, weekday, yearday, daylightsavings)):
	date = time.strftime('%A, %B %d, %Y', (year, month, day, hour, minute, second, weekday, yearday, daylightsavings))
	fp.write("""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dt">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<title>%s</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<style type="text/css">
<!--
.userjoin {color: #FFFFFF; font-style: italic; font-weight: bold}
.userleave {color: #8B864E; font-style: italic; font-weight: bold}
.statuschange {color: #C48189; font-weight: bold}
.rachange {color: #0000FF; font-weight: bold}
.userkick {color: #FF7F50; font-weight: bold}
.userban {color: #DAA520; font-weight: bold}
.nickchange {color: #FF69B4; font-style: italic; font-weight: bold}
.timestamp {color: #05070A;}
.newacc {color: #008B00; font-style: italic; font-weight: bold}
.timestamp a {color: #000000; text-decoration: none;}
.system {color: #008B00; font-weight: bold;}
.emote {color: #8B864E;}
.self {color: #0000AA;}
.selfmoder {color: #8B8B83;}
.normal {color: #483d8b;}
#mark { color: #aaa; text-align: right; font-family: monospace; letter-spacing: 3px }
h1 { color: #000000; font-family: sans-serif; border-bottom: #000000 solid 3pt; letter-spacing: 3px; margin-left: 20pt;}
h2 { color: #000000; font-family: sans-serif; letter-spacing: 2px; text-align: center }
h3 { color: #FFFFFF; font-family: sans-serif; letter-spacing: 2px; text-align: center }
h4 { border-width: 1px; border-style: solid; border-color: black;}
a.h1 {text-decoration: none;color: #000000;}
#//-->
</style>
</head>
<body bgcolor="#BCEE68">
<body>
<b>%s - %s</b>
<div>
<h4>
<tt>
""" % (' - '.join([source, date]), source, date))

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
	if not body:
		return
	if log_fail():
                return
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
	if fp=='0' or fp==0:
                return
        fp.write('<span class="timestamp"><a id="t' + timestamp[1:-1] + '.' + decimal + '" href="#t' + timestamp[1:-1] + '.' + decimal + '">' + timestamp + '</a></span> ')
	if not nick:
		fp.write('<span class="system">' + body + '</span><br />\n')
	elif body[:3].lower() == '/me':
		fp.write('<span class="emote">* %s%s</span><br />\n' % (nick, body[3:]))
	elif type == 'public' or nick == DEFAULT_NICK:
		if nick=='@$$leave$$@':
			fp.write('<span class="userleave">' + body + '</span><br />\n')
		elif nick=='@$$join$$@':
			fp.write('<span class="userjoin">' + body + '</span><br />\n')
		elif nick=='@$$status$$@':
			fp.write('<span class="statuschange">' + body + '</span><br />\n')
		elif nick=='@$$ra$$@':
			fp.write('<span class="rachange">' + body + '</span><br />\n')
		elif nick=='@$$userkick$$@':
			fp.write('<span class="userkick">' + body + '</span><br />\n')
		elif nick=='@$$userban$$@':
			fp.write('<span class="userban">' + body + '</span><br />\n')
		elif nick=='@$$nickchange$$@':
			fp.write('<span class="nickchange">' + body + '</span><br />\n')
		elif nick=='@$$newacc$$@':
                        fp.write('<span class="newacc">' + body + '</span><br />\n')
		else:
			if ismoder:
				fp.write('<span class="selfmoder">&lt;%s&gt;</span><span class="timestamp"> %s</span><br />\n' % (nick, body))
			else:
				fp.write('<span class="self">&lt;%s&gt;</span><span class="timestamp"> %s</span><br />\n' % (nick, body))
	else:
		fp.write('<span class="normal">&lt;%s&gt;</span><span class="timestamp"> %s</span><br />\n' % (nick, body))
	fp.close()

LOG_AFL_ROLE = {}

def log_handler_join(groupchat, nick, aff, role, cljid):
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
			log_write('%s leaves the room (%s)' % (nick,reason), '@$$leave$$@', 'public', groupchat)
		else:
			log_write('%s leaves the room' % (nick), '@$$leave$$@', 'public', groupchat)

def log_handler_presence(prs, cljid):
        if log_fail():
                return
	stmsg,status,code,reason,newnick='','','','',''
	try: jid = prs['from'].split('/')
	except: return
        groupchat = jid[0]
        if not groupchat in GROUPCHATS:
                return
        if not groupchat.count('conference.') and not groupchat.count('.chat') and not groupchat.count('muc.'):
                return
        nick = prs['from'][len(groupchat)+1:]
	if nick and len(nick)>19: nick=nick[:19]+'..>>>'
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
		log_write('%s now is known as %s' % (nick,newnick), '@$$nickchange$$@', 'public', groupchat)
	else:
		if not type=='unavailable':
			try:
				stmsg = prs.getStatus()
			except:
				stmsg=''
			if stmsg:
                                if len(stmsg)>60:
                                        stmsg=u'Статус-флуд'
			try:
				status = prs.getShow()
			except:
				status = 'online'
			if not status:
				status = 'online'
			if groupchat in LOG_AFL_ROLE.keys():
                                if nick in LOG_AFL_ROLE[groupchat]:
                                        try:
                                                if ROLES[role]+AFFILIATIONS[afl]!=LOG_AFL_ROLE[groupchat][nick]:
                                                        LOG_AFL_ROLE[groupchat][nick]=ROLES[role]+AFFILIATIONS[afl]
                                                        log_write('%s has new access %s and %s ( reason: %s )' % (nick,role,afl,reason),'@$$newacc$$@','public',groupchat)
                                                        return
                                        except:
                                                pass
			if stmsg:
				log_write('%s is now %s (%s)' % (nick,status,stmsg), '@$$status$$@', 'public', groupchat)
			else:
				log_write('%s is now %s' % (nick,status), '@$$status$$@', 'public', groupchat)


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

register_command_handler(log_on_off, '!логи', ['все','игры'], 30, 'включает/отключает запись логов в конфе', '!логи', ['!логи'])

	
if PUBLIC_LOG_DIR:
        register_stage1_init(log_make_dir)
	register_message_handler(log_handler_message)
	register_join_handler(log_handler_join)
	register_leave_handler(log_handler_leave)
	register_presence_handler(log_handler_presence)
if PRIVATE_LOG_DIR:
	register_outgoing_message_handler(log_handler_outgoing_message)
