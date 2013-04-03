# -*- coding: utf-8 -*-

CMDCOPY_FILE = 'dynamic/cmdcopy.txt'

def hnd_cmdcopy(t, sr, p):
    if not p: return
    db=eval(read_file(CMDCOPY_FILE))
    if p.lower() in db.values():
        for x in db.keys():
            if db[x]==p.lower():
                del db[x]
                write_file(CMDCOPY_FILE, str(db))
        try: del COMMANDS[p.lower()]
        except: pass
        reply(t, sr, p+u' удалена!')
        return
    p=p.lower()
    s=p.split()
    if not s[0] in COMMANDS.keys():
        reply(t, sr, s[0]+u' несуществует!')
        return
    if s[1] in COMMANDS.keys():
        reply(t, sr, u'команда '+s[1]+u' уже есть!')
        return
    db[s[0]]=s[1]
    write_file(CMDCOPY_FILE, str(db))
    cmdcopy_exec(s[0], s[1])
    reply(t, sr, u'Скопировал!')

def cmdcopy_exec(x, cmd):
    hnd=COMMAND_HANDLERS[x].__name__
    category=COMMANDS[x]['category']
    access=COMMANDS[x]['access']
    desc=COMMANDS[x]['desc']
    syntax=COMMANDS[x]['syntax']
    syntax=syntax.replace(x.encode('utf8'), cmd.encode('utf8'))
    examples=COMMANDS[x]['examples']
    for m in examples:
        examples.remove(m)
        m=m.replace(x.encode('utf8'), cmd.encode('utf8'))
        examples.append(m)
    c="register_command_handler(%s, '%s', %s, %s, '%s', '%s', %s)" % (hnd, cmd.encode('utf8'), category, access, desc, syntax, examples)
    exec c in globals()

def cmdcopy_init(cljid):
    if not os.path.exists(CMDCOPY_FILE):
        initialize_file(CMDCOPY_FILE, '{}')
    db=eval(read_file(CMDCOPY_FILE))
    if db:
        for x in db.keys():
            if db[x] in COMMANDS.keys() or x not in COMMANDS.keys():
                continue
            cmdcopy_exec(x, db[x])

register_stage0_init(cmdcopy_init)
            
register_command_handler(hnd_cmdcopy, 'cmdcopy', ['все'], 100, 'Создает копию команды с указанным названием.', 'cmdcopy <command> <copy name>', ['cmdcopy тест проверка'])        

