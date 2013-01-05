# -*- coding: utf8 -*-

LOG_FILES = {}

import os
import time

def log_data():
    Months = ("", u"Января", u"Февраля", u"Марта", u"Апреля", u"Мая", u"Июня", u"Июля", u"Августа", u"Сентября", u"Октября", u"Ноября", u"Декабря")
    Days = (u"Понедельник", u"Вторник", u"Среда", u"Четверг", u"Пятница", u"Суббота", u"Воскресенье", u"")
    dn = Days[time.localtime()[6]]
    mn = Months[time.localtime()[1]]
    date = dn+', '+str(time.localtime()[2])+' '+mn
    return date

def log_header(channel, data, topic):
    rep = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
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
#mark { color: #aaa; text-align: right; font-family: monospace; letter-spacing: 3px }
h1 { color: #D0D0D0; font-family: sans-serif; border-bottom: #246 solid 3pt; letter-spacing: 3px; margin-left: 20pt;}
h2 { color: #33CC66; font-family: sans-serif; letter-spacing: 2px; text-align: center }
h3 { color: #FFFFFF; font-family: sans-serif; letter-spacing: 2px; text-align: center }
a.h1 {text-decoration: none;color: #369;}
h4 {
 border-width: 4px;
 border-style: double;
 border-color: #33CC66;
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
<h2>The topic is "%s"</h2>
<h4>
<span class="presence">%s</span><br />

<tt>
""" % (channel, topic, data)
    return rep

def check_dir(s):
    if not os.access(s, os.F_OK): os.mkdir(s)

def close_log(fn):
    if os.access(fn, os.W_OK):
        fp = file(fn, 'a')
        fp.write(log_footer.encode('utf8', 'replace'))
        fp.close()

IRC_LOG_C = {}

def irc_log_join(*arg):
    if not arg[0] in IRC_CHAN:
        return
    text = '* '+ircn(arg[1])+' has join'
    write_to_log_(arg[0], text, 1)

register_join_handler(irc_log_join)

def irc_log_leave(*arg):
    if not arg[0] in IRC_CHAN:
        return
    text = '* '+ircn(arg[1])+' has left'+('('+arg[2]+')' if arg[2] else str())
    write_to_log_(arg[0], text, 1)

register_leave_handler(irc_log_join)
    

def irc_log_msg(r, t, s, p):
    if t != 'irc':
        return
    if not s[1] or s[1]==IRC_NICK or not isinstance(s[1],basestring) or len(s[1])==1:
        return
    if not s[0] in IRC_LOG_C:
        IRC_LOG_C[s[0]] = "".join([hex(random.randrange(0, 255))[2:] for i in range(3)])
    text = '<font color="#%s">&lt;%s&gt;</font> %s<br />\n' % (IRC_LOG_C[s[0]], ircn(s[0]), p)
    write_to_log_(s[1], text)

register_message_handler(irc_log_msg)

def write_to_log_(channel, text, syst = 0):
    (year, month, day, hour, minute, second, weekday, yearday, daylightsavings) = time.localtime()
    p1 = '%s/%s' % (PUBLIC_LOG_DIR, channel)
    p2 = '%s/%s' % (p1, time.strftime('%Y'))
    p3 = '%s/%s' % (p2, time.strftime('%m'))
    p4 = '%s/%s.html' % (p3, time.strftime('%d'))
    if not os.access(p4, os.F_OK):
        check_dir(p1)
        check_dir(p2)
        check_dir(p3)
        fp = file(p4, 'w')
        data = log_data()
        topic = IRC_TOPIC.get(channel)
        header = log_header(channel.decode('utf8','replace'), data, (topic.decode('utf8','replace') if topic else ''))
        fp.write(header.encode('utf8'))
        fp.close()
    
    decimal = str(int(math.modf(time.time())[0]*100000))
    timestamp = '[%.2i:%.2i:%.2i]' % (hour, minute, second)
    tsamp = '<a id="t'+timestamp[1:-1]+'.'+decimal+'" href="#t' + timestamp[1:-1] + '.'+decimal+'">'+timestamp+'</a>'
    if syst:
        text = '<span class="presence">'+timestamp+text+'</span><br />\n '
    else:
        tsamp = '<span class="timestamp">'+tsamp+'</span> '
        text = '%s %s' % (tsamp, text)
    try:
        fp = file(p4, 'a')
        fp.write(text.encode('utf8'))
    finally:
        fp.close()

