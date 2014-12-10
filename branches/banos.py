# -*- coding: utf-8 -*-

BANOS = {}

BANOS_LIMIT = {}

BANOS_FILE = 'dynamic/banos.txt'

db_file(BANOS_FILE, dict)

try:
    BANOS = eval(read_file(BANOS_FILE))
except:
    pass

def banos_join(g, n, r, afl, cljid):
    global BANOS
    global BANOS_LIMIT
    if not g in BANOS or not BANOS[g].keys():
        return
    if n == get_bot_nick(g):
        return
    if not g in BANOS_LIMIT.keys():
        BANOS_LIMIT[g]={'t':time.time(),'n':1}
    else:
        if time.time() - BANOS_LIMIT[g]['t']<3:
            BANOS_LIMIT[g]['n']+=1
            BANOS_LIMIT[g]['t']= time.time()
            if BANOS_LIMIT[g]['n']>3:
                return
        else:
            BANOS_LIMIT[g]['t'] = time.time()
            BANOS_LIMIT[g]['n'] = 1
    #print 'swnd'
    packet = IQ(CLIENTS[cljid], 'get')
    q = packet.addElement('query', 'jabber:iq:version')
    packet.addCallback(version_result_banos, g, n, cljid)
    reactor.callFromThread(packet.send, g+'/'+n)


register_join_handler(banos_join)


def version_result_banos(g, n, cljid, x):
    #print x.toXml()
    if x['type'] == 'error':
        pass
    else:
        query = element2dict(x)['query']
        r = element2dict(query)
        os = str(r.get('os').children[0])
        if os in BANOS[g].keys():
            #print 'true++'
            room_access(cljid, g, 'affiliation', 'outcast', 'jid', get_true_jid(g+'/'+n))


def hnd_banos(t, s, p):
    z = ''
    if not s[1] in GROUPCHATS:
        return
    if not s[1] in BANOS:
        BANOS[s[1]]={}
    if not p:
        z = ', '.join(BANOS[s[1]].keys())
        reply(t, s, (z if not z.isspace() else 'empty list'))
    else:
        if not p in BANOS[s[1]].keys():
            BANOS[s[1]][p]={}
            reply(t, s, 'Added!')
        else:
            del BANOS[s[1]][p]
            reply(t, s, 'Removed!')
        write_file(BANOS_FILE, str(BANOS))
       
        
register_command_handler(hnd_banos, 'banos', ['все'], 0, 'Add os to muc ban. Empty parameters return list.', 'banos', ['banos any'])
