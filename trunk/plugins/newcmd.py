#===istalismanplugin===
# -*- coding: utf-8 -*-

CMD_HELP_MEM = {}

def newcmd_msg(r, t, s, p):
    if not p:
        return
    if p.count(' ')>1:
        return
    if s[1] in GROUPCHATS and t in ['public','groupchat']:
        bn = get_bot_nick(s[1])
        if not p.count(bn):
            return
        for x in [bn+x for x in [':',',','>']]:
            p=p.replace(x,'')
        #if not p.split()[0].lower() if COMMANDS.keys() and not 
            
    ss = p.split()
    if ss[0].lower() in COMMANDS:
        return
    if len(ss[0])<4 or len(ss[0])>30:
        return
    lenlike = [x for x in COMMANDS.keys() if len(ss[0])==len(x)]
    sp = []
    n = 0
    cmd = list(ss[0].lower())
    minlen = 2
    if len(cmd)<=5:
        minlen = 1
    for x in lenlike:
        a = list(x)
        notlike = 0
        ind = 0
        for c in a:
            if cmd[ind]==c:
                pass
            else:
                notlike+=1
            ind+=1
        if notlike!=0 and notlike <= minlen:
            sp.append(x)
    if not sp or len(sp)>1:
        return
    if sp[0].lower() in [u'свал',u'пшёл',u'рестарт']: return
    reply(t, s, u'Возможно, вы имели в виду -\n'+''.join(sp)+u' ?')
    time.sleep(1.5)
    rep = sp[0]
    c=''
    command=rep
    if len(ss)>1:
        c=ss[1]
    if s[1] in COMMOFF and command in COMMOFF[s[1]]:
        return
    else:
        call_command_handlers(command, t, s, unicode(c))
        INFO['cmd'] += 1
        


register_message_handler(newcmd_msg)

CMD_REPL={u' ':u' ',u'q':u'й',u'w':u'ц',u'e':u'у',u'r':u'к',u't':u'е',u'y':u'н',u'u':u'г',u'i':u'ш',u'o':u'щ',u'p':u'з',u'[':u'х',u']':u'ъ',u'a':u'ф',u's':u'ы',u'd':u'в',u'f':u'а',u'g':u'п',u'h':u'р',u'j':u'о',u'k':u'л',u'l':u'д',u';':u'ж',u'\'':u'э',u'z':u'я',u'x':u'ч',u'c':u'с',u'v':u'м',u'b':u'и',u'n':u'т',u'm':u'ь',u',':u'б',u'.':u'ю'}


def data_cmd_replace(data):
        global CMD_REPL
        rep=''
        for x in data:
                if x in CMD_REPL.keys():
                        rep+=CMD_REPL[x]
                else:
                        rep+=x
        return rep
                        
def cmd_repl(raw, type, source, parameters):
        try:
                if not parameters:
                        return
                if len(parameters)>50:
                        return
                parameters = parameters.lower()
                if parameters in COMMANDS.keys():
                        return
                if parameters.count(' '):
                        cmd=parameters.split()[0]
                        if cmd in COMMANDS.keys():
                                return
                if source[1] in GROUPCHATS:
                        if source[2]==get_bot_nick(source[1]):
                                return
                if source[2] and source[2]!=None:
                        cmd=data_cmd_replace(source[2])
                        if source[2].count(' '):
                                cmd=source[2].split()[0]
                                cmd=data_cmd_replace(cmd)
                        if cmd in COMMANDS.keys():
                                return
                rep=''
                c=''
                rep=data_cmd_replace(parameters)
                if not rep or rep.isspace():
                        return
                command=rep
                if rep.count(' '):
                        s=rep.split()
                        command=s[0]
                        c=' '.join(s[1:])
                if command in COMMANDS:
                        if source[1] in COMMOFF and command in COMMOFF[source[1]]:
                                return
                        else:
                                reply(type, source, u'Команду распознано как:\n'+rep)
                                time.sleep(1.5)
                                call_command_handlers(command, type, source, unicode(c))
                                INFO['cmd'] += 1

        except:
                pass

register_message_handler(cmd_repl)
    
